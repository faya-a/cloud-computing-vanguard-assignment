import requests
import json

response = requests.get("https://api.myip.com")
print(response.status_code)

print(json.dumps(response.json(), indent=4))
