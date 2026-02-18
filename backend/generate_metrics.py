import requests
import time

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiZXhwIjoxNzcwOTU4NTY0fQ.MPvWzV6FGwIMHkQonShcBbk7UIIWuBVnSnjhgcwz3QE"
INSTANCE_ID = "i-012ec6602feabebfb"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

url = f"http://localhost:8000/api/metrics/all/{INSTANCE_ID}"

for i in range(120):  # generate 120 samples
    r = requests.get(url, headers=headers)
    print(f"Sample {i+1}: {r.status_code}")
    time.sleep(1)
