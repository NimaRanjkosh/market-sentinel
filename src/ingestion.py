import os
import requests
import json
from dotenv import load_dotenv
from src.database.client import PostgresClient

load_dotenv()

API_URL= os.getenv("API_URL")
USER_AGENT=os.getenv("USER_AGENT")

HEADERS = {
    "User-Agent": USER_AGENT,
    "Content-Type":"application/json"
}

INITIAL_PAYLOAD = {
    "city_ids": ["1"],
    "search_data": {
        "form_data": {
            "data": {
                "category": {"str": {"value": "real-estate"}},
                "sort": {"str": {"value": "sort_date"}}
            }
        }
    }
}

def run_harvester():
    """
    Docstring for run_harvester
    """
    print("Starting Harvester...")
    
    db = PostgresClient()
    
    # sending request to the api
    response = requests.post(url=API_URL, headers=HEADERS, json=INITIAL_PAYLOAD)
    
    # security check for responses
    if response.status_code == 403:
        print("Error 403: Forbidden. Check your User-Agent")
        return
    if response.status_code != 200:
        print(f"Erorr {response.status_code}: {response.text}")
        return
    
    # storing data in variable
    data = response.json()
    widgets = data.get("list_widgets", [])
    print(f"Received {len(widgets)} widgets.")
    
    # processig data
    count = 0
    for widget in widgets:
        if widget.get("widget_type") != "POST_ROW":
            continue
        
        widget_data = widget.get("data", {})
        # extracting token
        action = widget_data.get("action")
        payload = action.get("payload")
        token = payload.get("token")
        
        if not token:
            continue
        
        # Insert data into raw_listings of the app
        try:
            db.insert_raw_listing(token=token, raw_data=widget_data)
            count += 1
            print(f"Saved: {token} - {widget_data.get("title")}")
        except Exception as e:
            print(f"Failed to save {token}: {e}")
        
    print(f"Harvest Complete. Saved {count} new listings.")
    

if __name__=="__main__":
    run_harvester()