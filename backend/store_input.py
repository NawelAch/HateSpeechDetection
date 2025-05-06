import psycopg2
from psycopg2 import sql

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "my_db"
DB_USER = "postgres"
DB_PASS = "password"

def store_user_input(user_input: str, predicted_label: bool):
    try:
        with psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO user_inputs (text, predicted_label)
                    VALUES (%s, %s)
                    ON CONFLICT (text) DO NOTHING;
                """, (user_input, predicted_label))
                conn.commit()
        print("✅ User input stored or skipped if already exists.")
    except Exception as e:
        print(f"❌ Error storing user input: {e}")

def store_report(user_input: str, predicted_label: bool):
    try:
        with psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO reports (user_input, predicted_label)
                    VALUES (%s, %s)
                    ON CONFLICT (user_input) DO NOTHING;
                """, (user_input, predicted_label))
                conn.commit()
        print("✅ Report stored or skipped if already exists.")
    except Exception as e:
        print(f"❌ Error storing report: {e}")