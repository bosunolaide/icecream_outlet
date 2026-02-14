from typing import List, Dict, Tuple
from django.db import connection
from flavours.models import Flavour
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def _fetch_user_flavour_matrix() -> Tuple[np.ndarray, List[int], List[int]]:
    """
    Build a (num_users x num_flavours) matrix from orders_orderitem:
    value = total quantity purchased per flavour by customer.
    Returns: matrix, user_ids, flavour_ids
    """
    with connection.cursor() as cur:
        cur.execute("""
            SELECT o.customer_id, oi.flavour_id, SUM(oi.quantity) AS qty
            FROM orders_order o
            JOIN orders_orderitem oi ON oi.order_id = o.id
            GROUP BY o.customer_id, oi.flavour_id
        """)
        rows = cur.fetchall()

    if not rows:
        return np.zeros((0, 0)), [], []

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
    """
    mat, user_ids, flavour_ids = _fetch_user_flavour_matrix()

    # fallback: if no history exists, return most popular flavours
    if mat.size == 0 or customer_id not in user_ids:
        return _popular_flavours(k)

    uidx = user_ids.index(customer_id)
    user_vec = mat[uidx:uidx+1]  # shape (1, n_flavours)

    # Similarities to other users
    sims = cosine_similarity(user_vec, mat)[0]  # shape (n_users,)
    sims[uidx] = 0.0  # ignore self

    # Weighted preference score for each flavour
    scores = sims @ mat  # shape (n_flavours,)

    # Do not recommend flavours already bought
    already_bought = user_vec[0] > 0
    scores[already_bought] = 0.0

    # pick top-k
    top_idx = np.argsort(scores)[::-1][:k]
    top = [(flavour_ids[i], float(scores[i])) for i in top_idx if scores[i] > 0]

    # attach names
    flavour_map = {f.id: f.name for f in Flavour.objects.filter(id__in=[fid for fid, _ in top])}
    return [{"flavour_id": fid, "name": flavour_map.get(fid, f"Flavour {fid}"), "score": sc} for fid, sc in top]

def _popular_flavours(k: int) -> List[Dict]:
    """
    Simple non-personalized fallback: top flavours by total quantity sold.
    """
    with connection.cursor() as cur:
        cur.execute("""
            SELECT oi.flavour_id, SUM(oi.quantity) AS qty
            FROM orders_orderitem oi
            GROUP BY oi.flavour_id
            ORDER BY qty DESC
            LIMIT %s
        """, [k])
        rows = cur.fetchall()

    ids = [r[0] for r in rows]
    flavour_map = {f.id: f.name for f in Flavour.objects.filter(id__in=ids)}
    # normalize scores
    max_qty = max([r[1] for r in rows], default=1) or 1
    return [{"flavour_id": fid, "name": flavour_map.get(fid, f"Flavour {fid}"), "score": float(qty) / float(max_qty)} for fid, qty in rows]
