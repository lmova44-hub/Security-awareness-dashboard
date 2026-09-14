import requests
import os

GOPHISH_API_KEY = os.environ.get("GOPHISH_API_KEY")
GOPHISH_URL = "https://127.0.0.1:3333"

headers = {
    "Authorization": GOPHISH_API_KEY
} 

response = requests.get(
    f"{GOPHISH_URL}/api/campaigns/",
    headers=headers,
    verify=False
)

print("Status:", response.status_code)
print(response.text)
