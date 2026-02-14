from __future__ import annotations

from typing import List, Dict, Tuple
import logging

from django.db import connection
from flavours.models import Flavour
import numpy as np

logger = logging.getLogger(__name__)


def _cosine_similarity_1_to_many(vec_1d: np.ndarray, mat_2d: np.ndarray) -> np.ndarray:
    """
    Pure-numpy cosine similarity to avoid sklearn dependency (lighter for Render).
    vec_1d: shape (n_features,)
    mat_2d: shape (n_samples, n_features)
    returns: shape (n_samples,)
    """
    v = vec_1d.astype(np.float32)
    m = mat_2d.astype(np.float32)

    v_norm = float(np.linalg.norm(v) + 1e-9)
    m_norm = (np.linalg.norm(m, axis=1) + 1e-9).astype(np.float32)

    return (m @ v) / (m_norm * v_norm)


def _fetch_user_flavour_matrix() -> Tuple[np.ndarray, List[int], List[int]]:
    """
    Build a (num_users x num_flavours) matrix from orders_orderitem:
    value = total quantity purchased per flavour by customer.
    Returns: matrix, user_ids, flavour_ids
    """
    with connection.cursor() as cur:
        cur.execute(
            """
            SELECT o.customer_id, oi.flavour_id, SUM(oi.quantity) AS qty
            FROM orders_order o
            JOIN orders_orderitem oi ON oi.order_id = o.id
            GROUP BY o.customer_id, oi.flavour_id
            """
        )
        rows = cur.fetchall()

    if not rows:
        return np.zeros((0, 0), dtype=np.float32), [], []

    user_ids = sorted({r[0] for r in rows})
    flavour_ids = sorted({r[1] for r in rows})

    user_index = {uid: i for i, uid in enumerate(user_ids)}
    flavour_index = {fid: j for j, fid in enumerate(flavour_ids)}

    mat = np.zeros((len(user_ids), len(flavour_ids)), dtype=np.float32)
    for customer_id, flavour_id, qty in rows:
        mat[user_index[customer_id], flavour_index[flavour_id]] = float(qty)

    return mat, user_ids, flavour_ids


def recommend_flavours_for_customer(customer_id: int, k: int = 5) -> List[Dict]:
    """
    Recommend flavours for a customer using:
    - cosine similarity between customers based on historical purchases
    - weighted sum of neighbours’ flavour vectors

    Robustness:
    - If no history exists (or customer has no history), fall back to popular flavours
    - Avoids sklearn to reduce memory footprint on small instances (Render)
    """
    # Defensive k
    try:
        k = int(k)
    except (TypeError, ValueError):
        k = 5
    k = max(1, min(k, 50))

    mat, user_ids, flavour_ids = _fetch_user_flavour_matrix()

    # fallback: if no history exists, return most popular flavours
    if mat.size == 0 or customer_id not in user_ids:
        return _popular_flavours(k)

    uidx = user_ids.index(customer_id)
    user_vec = mat[uidx]  # shape (n_flavours,)

    # Similarities to other users (pure numpy)
    sims = _cosine_similarity_1_to_many(user_vec, mat)  # shape (n_users,)
    sims[uidx] = 0.0  # ignore self

    # Weighted preference score for each flavour
    scores = sims @ mat  # (n_flavours,)

    # Do not recommend flavours already bought
    already_bought = user_vec > 0
    scores = scores.astype(np.float32)
    scores[already_bought] = 0.0

    # pick top-k
    top_idx = np.argsort(scores)[::-1][:k]
    top = [(flavour_ids[i], float(scores[i])) for i in top_idx if float(scores[i]) > 0.0]

    if not top:
        return _popular_flavours(k)

    # attach names
    flavour_map = {
        f.id: f.name for f in Flavour.objects.filter(id__in=[fid for fid, _ in top])
    }
    return [
        {"flavour_id": fid, "name": flavour_map.get(fid, f"Flavour {fid}"), "score": sc}
        for fid, sc in top
    ]


def _popular_flavours(k: int) -> List[Dict]:
    """
    Simple non-personalized fallback: top flavours by total quantity sold.
    """
    try:
        k = int(k)
    except (TypeError, ValueError):
        k = 5
    k = max(1, min(k, 50))

    with connection.cursor() as cur:
        cur.execute(
            """
            SELECT oi.flavour_id, SUM(oi.quantity) AS qty
            FROM orders_orderitem oi
            GROUP BY oi.flavour_id
            ORDER BY qty DESC
            LIMIT %s
            """,
            [k],
        )
        rows = cur.fetchall()

    if not rows:
        return []

    ids = [r[0] for r in rows]
    flavour_map = {f.id: f.name for f in Flavour.objects.filter(id__in=ids)}

    max_qty = max([r[1] for r in rows], default=1) or 1
    return [
        {
            "flavour_id": fid,
            "name": flavour_map.get(fid, f"Flavour {fid}"),
            "score": float(qty) / float(max_qty),
        }
        for fid, qty in rows
    ]
