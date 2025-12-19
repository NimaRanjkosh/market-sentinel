import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.client import PostgresClient
from src.utils import clean_price

def run_pipeline():
    
    print("Starting the ETL pipeline")
    db = PostgresClient()
    
    # fetch pending rows in listings
    pending_rows = db.get_pending_listings()
    print(f"Found {len(pending_rows)} new raw listings in process")
    
    processed_count = 0
    
    for token, raw_data in pending_rows:
        action = raw_data.get("action", {})
        payload = action.get("payload", {})
        web_info = payload.get("web_info", {})
        
        title = web_info.get("title") or raw_data.get("title")
        district = web_info.get("district_persian")
        city = web_info.get("city_persian")
        
        top_text = raw_data.get("top_description_text", "")
        middle_text = raw_data.get("middle_description_text", "")
        
        price_sell = None
        price_deposit = None
        price_rent = None
        
        is_rental = "اجاره" in top_text or "اجاره" in middle_text or "ودیعه" in top_text
        
        if is_rental:
            # Usually: Top text is Deposit, Middle is Rent
            price_deposit = clean_price(top_text)
            price_rent = clean_price(middle_text)
        else:
            price_sell = clean_price(middle_text) # it's for sale
            
        
        clean_row = {
            "token": token,
            "title": title,
            "district": district,
            "city": city,
            "area": None, 
            #TODO: Extract '85' from '85متر' for area. It has a complex logic. 
            # The area stores in title but it may contain other integers like the number of parking or other numbers so it's not as simple as price processing
            "rooms": None,
            #TODO: It's like area. usually store in title with خواب or stores in top_description as اتاق
            "price_sell": price_sell,
            "price_deposit": price_deposit,
            "price_rent": price_rent,
            "is_urgent": False
        }
        
        try:
            db.upsert_listings(clean_row)
            processed_count +=1
        except Exception as e:
            print(f"Error processing \nTOKEN: {token}: {e}")
        
    print(f"Pipeline finished. Transformed {processed_count} records.")
    
if __name__=="__main__":
    run_pipeline()