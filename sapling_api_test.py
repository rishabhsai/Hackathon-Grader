import requests

SAPLING_API_KEY = "AOM37012AEROXNPALYM7E6ZEX2CPZVEC"

text = input("Enter text to test Sapling AI Detector: ")

url = "https://api.sapling.ai/api/v1/aidetect"
headers = {"Content-Type": "application/json"}
data = {
    "key": SAPLING_API_KEY,
    "text": text,
    "sent_scores": True,
    "score_string": True
}

response = requests.post(url, headers=headers, json=data)
print(f"Status code: {response.status_code}")
print("Response:")
print(response.text) 