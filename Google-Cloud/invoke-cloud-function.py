import requests
import json

url = "https://region-project.cloudfunctions.net/my-function"
payload = {"event": "trigger"}

response = requests.post(url, json=payload)
print(response.status_code)
