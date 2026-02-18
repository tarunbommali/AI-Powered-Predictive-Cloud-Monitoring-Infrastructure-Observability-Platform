import sqlite3
import os

for db_path in ['monitoring.db', '../monitoring.db']:
    full = os.path.abspath(db_path)
    if os.path.exists(db_path):
        print(f"\n=== DB: {full} (size: {os.path.getsize(db_path)} bytes) ===")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Tables: {[t[0] for t in tables]}")
        for table in tables:
            tname = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {tname}")
            count = cursor.fetchone()[0]
            print(f"  {tname}: {count} rows")
            if count > 0 and count < 20:
                cursor.execute(f"SELECT * FROM {tname}")
                for row in cursor.fetchall():
                    print(f"    {row}")
        conn.close()
    else:
        print(f"\n{full} - NOT FOUND")
