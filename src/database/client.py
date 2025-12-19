import os
import psycopg
import psycopg.types.json as js
from dotenv import load_dotenv

load_dotenv()

class PostgresClient:
    def __init__(self):
        self.connection_string = os.getenv("POSTGRES_URL")
        
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
            
    def get_pending_listings(self):
        """
        Fetch listings that are in 'raw_listings' but missing from 'listings'.
        This ensures we only process new data.
        """
        
        sql = """
        SELECT
            token, raw_data
        FROM
            raw_listings as rl
        WHERE
            rl.token not in (SELECT token FROM listings);
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
            
    def upsert_listings(self, data: dict):
        """
        Insert or Update a clean listing. 
        """
        
        sql = """
        INSERT INTO listings (
            token, title, district, city, area, rooms,
            price_sell, price_deposit, price_rent, is_urgent 
        )
        VALUES (
            %(token)s, %(title)s, %(district)s, %(city)s, %(area)s, %(rooms)s,
            %(price_sell)s, %(price_deposit)s, %(price_rent)s, %(is_urgent)s
            )
        ON CONFLICT (token) DO UPDATE SET
            price_sell = EXCLUDED.price_sell,
            price_deposit = EXCLUDED.price_deposit,
            price_rent = EXCLUDED.price_rent,
            last_updated = CURRENT_TIMESTAMP;
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, data)
            