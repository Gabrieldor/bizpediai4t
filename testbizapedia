import requests
import json 


def quote():
    with open("json.json", 'r') as f:
        r = requests.post("http://localhost:8000/api/v1/bizapedia/quote", json={"state_code" : "Mississippi", "company_name": "CURTIS AND INGRAM TRUCKING LLC"})
        print(r.content)
            
quote()
