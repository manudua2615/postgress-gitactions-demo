import os
import subprocess
import sys
from pathlib import Path

import pytest
from psycopg2 import connect

BASE_DIR = Path(__file__).parent
EXPECTED_COLUMNS = [
    "id", "user_name", "entry_date", "main_category",
    "sub_category", "description", "amount", "payment_method",
]

def conn():
    return connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "postgres"),
        dbname=os.getenv("PGDATABASE", "demodb"),
    )

def test_query_returns_expected_columns():
    with open(BASE_DIR / "1.sql", "r", encoding="utf-8") as f:
        query = f.read()
    with conn() as c, c.cursor() as cur:
        cur.execute(query)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
    assert cols == EXPECTED_COLUMNS
    assert len(rows) > 0

def test_query_filters_categories():
    allowed = {"salary", "utilities"}
    with conn() as c, c.cursor() as cur:
        cur.execute("SELECT main_category FROM public.finance_entry")
        all_rows = cur.fetchall()
        cur.execute(Path(BASE_DIR / "1.sql").read_text(encoding="utf-8"))
        filtered_rows = cur.fetchall()
    assert all(r[3] in allowed for r in filtered_rows)
    assert len(filtered_rows) < len(all_rows)

def test_run_query_script_exits_zero():
    env = os.environ.copy()
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "run_query.py"), str(BASE_DIR / "1.sql")],
        capture_output=True, text=True, env=env,
    )
    assert result.returncode == 0, result.stderr
    assert "row(s) returned" in result.stdout
