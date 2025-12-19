from src.database.client import PostgresClient

if __name__=="__main__":
    db = PostgresClient()
    
    fake_token = "FAKE_TOKEN"
    fake_json = {"title": "Test Apartment", "price":4235}
    
    print(f"Attempting to insert fake_token: {fake_token} and fake_json: {fake_json}")
    db.insert_raw_listing(fake_token, fake_json)
    print("Success! check your db.")