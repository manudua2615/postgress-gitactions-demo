import os
import sys

try:
    from dotenv import load_dotenv
    from psycopg2 import connect, extras
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install python-dotenv psycopg2-binary")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def main():
    sql_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE_DIR, "1.sql")
    with open(sql_path, "r", encoding="utf-8") as f:
        query = f.read()

    conn = connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        dbname=os.getenv("PGDATABASE"),
    )
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            if cur.description is not None:
                rows = cur.fetchall()
                cols = [d[0] for d in cur.description]
                print("\t".join(cols))
                for row in rows:
                    print("\t".join(str(v) if v is not None else "NULL" for v in row))
                print(f"\n{len(rows)} row(s) returned")
            else:
                print(f"Query executed successfully. {cur.rowcount} row(s) affected.")
            conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
