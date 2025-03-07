import os
import requests
from dotenv import load_dotenv

def test_coda_connection():
    """
    Test the connection to the Coda API using the credentials in the .env file.
    This helps verify that the API key and document/table IDs are correct.
    """
    # Load environment variables
    load_dotenv()
    
    # Get Coda API details
    CODA_API_KEY = os.getenv("CODA_API_KEY", "3e92f721-91d1-485e-aab9-b7d50e4fa4da")
    DOC_ID = os.getenv("CODA_DOC_ID", "dNYzN0H9At4")
    TABLE_ID = os.getenv("CODA_TABLE_ID", "tun7MrAA")
    
    print(f"Testing Coda API connection...")
    
    # Test connection by querying the table metadata
    url = f"https://coda.io/apis/v1/docs/{DOC_ID}/tables/{TABLE_ID}"
    headers = {
        "Authorization": f"Bearer {CODA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            table_info = response.json()
            print(f"✅ Successfully connected to Coda!")
            print(f"Table name: {table_info.get('name', 'Unknown')}")
            print(f"Table ID: {table_info.get('id', 'Unknown')}")
            return True
        else:
            print(f"❌ Failed to connect to Coda API. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Coda API: {str(e)}")
        return False

if __name__ == "__main__":
    test_coda_connection() 