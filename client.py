import requests
import json

data = json.dumps(
    {
        "query": "Who were the Frodo's companion to destroy the ring?"
    }
)

response = requests.post(url="http://localhost:8000/chat", data=data)
response = json.loads(response.content)
print(response)