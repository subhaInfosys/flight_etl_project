import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('AVIATIONSTACK_API_KEY')

def extract_data():
    url = f"http://api.aviationstack.com/v1/flights?access_key="+api_key+"&limit=100"
    response = requests.get(url)
    data = response.json()
    
    #Optional debug:
    #print("Full API Response:", data)

    if 'data' in data:
        return data['data']
    else:
        raise Exception(f"'data' key not found in API response. Full response: {data}")

