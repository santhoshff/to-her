import requests
import json

try:
    response = requests.post(
        "http://localhost:5000/chat",
        headers={"Content-Type": "application/json"},
        data=json.dumps({"message": "Who are you?"})
    )
    print(response.text)
except Exception as e:
    print(e)
