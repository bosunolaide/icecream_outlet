#!/usr/bin/env python3
"""
Wait for TCP services (DBs, Redis) to become available.
Used by start_web.sh/start_worker.sh to avoid race conditions on Render.
"""
import os
import socket
import sys
import time

DEFAULT_TIMEOUT = int(os.getenv("WAIT_TIMEOUT", "90"))

def wait_for(host: str, port: int, timeout: int = DEFAULT_TIMEOUT) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=3):
                return True
        except OSError:
            time.sleep(2)
    return False

def main():
    targets = []
    # Postgres from DATABASE_URL or POSTGRES_HOST/PORT
    db_url = os.getenv("DATABASE_URL", "")
    if db_url.startswith("postgres"):
        # rough parse: postgres://user:pass@host:port/db
        try:
            after_at = db_url.split("@", 1)[1]
            hostport = after_at.split("/", 1)[0]
            if ":" in hostport:
                host, port = hostport.split(":", 1)
                targets.append((host, int(port)))
            else:
                targets.append((hostport, 5432))
        except Exception:
            pass
    else:
        targets.append((os.getenv("POSTGRES_HOST", "db"), int(os.getenv("POSTGRES_PORT", "5432"))))

    # MySQL
    targets.append((os.getenv("MYSQL_HOST", "mysql"), int(os.getenv("MYSQL_PORT", "3306"))))

    # Redis (optional)
    broker = os.getenv("CELERY_BROKER_URL", "")
    if broker.startswith("redis://"):
        try:
            after = broker.split("redis://", 1)[1]
            hostport = after.split("/", 1)[0]
            if "@" in hostport:
                hostport = hostport.split("@", 1)[1]
            if ":" in hostport:
                h, p = hostport.split(":", 1)
                targets.append((h, int(p)))
            else:
                targets.append((hostport, 6379))
        except Exception:
            pass

    for host, port in targets:
        sys.stderr.write(f"[wait] Waiting for {host}:{port} ...\n")
        ok = wait_for(host, port)
        if not ok:
            sys.stderr.write(f"[wait] Timeout waiting for {host}:{port}\n")
            sys.exit(1)
        sys.stderr.write(f"[wait] {host}:{port} is up\n")

if __name__ == "__main__":
    main()
