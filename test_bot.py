import requests

response = requests.post("http://127.0.0.1:8000/api/chat/text", json={"text": "say hello!"})
print(response.json())
