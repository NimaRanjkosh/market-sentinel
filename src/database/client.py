import os
import psycopg
import psycopg.types.json as js
from dotenv import load_dotenv

load_dotenv()

class PostgresClient:
    def __init__(self):
        self.connection_string = os.getenv("POSTGRES_DB")
        
    def get_connection(self):
        return psycopg.connect(self.connection_string)
    
    def insert_raw_listing(self, token: str, raw_data: dict):
        """
        Inserts a record into raw_listings.
        MUST handle conflicts (Idempotency).
        """
        
        sql = """
        Insert into raw_listings (token, raw_data)
        Values (%s, %s)
        ON CONFLICT (token) DO NOTHING;
        """
        params = (token, js.Jsonb(raw_data))
        
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query=sql, params=params)
            conn.commit()