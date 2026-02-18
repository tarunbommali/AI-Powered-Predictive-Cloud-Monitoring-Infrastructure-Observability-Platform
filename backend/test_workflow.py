"""Test the complete API workflow"""
import requests
import json

BASE = "http://localhost:8000/api"

def pp(data):
    print(json.dumps(data, indent=2, default=str))

# 1. Login
print("=== 1. LOGIN ===")
r = requests.post(f"{BASE}/auth/login", data={"username": "disistarun", "password": "Test@1234"})
print(f"Status: {r.status_code}")
token = r.json().get("access_token", "")
print(f"Token received: {bool(token)}")
headers = {"Authorization": f"Bearer {token}"}

# 2. Get current user
print("\n=== 2. GET /auth/me ===")
r = requests.get(f"{BASE}/auth/me", headers=headers)
print(f"Status: {r.status_code}")
pp(r.json())

# 3. List instances
print("\n=== 3. LIST INSTANCES ===")
r = requests.get(f"{BASE}/instances/", headers=headers)
print(f"Status: {r.status_code}")
pp(r.json())

# 4. Get instance by string ID
print("\n=== 4. GET INSTANCE by 'i-0347ad6ae12bdb460' ===")
r = requests.get(f"{BASE}/instances/i-0347ad6ae12bdb460", headers=headers)
print(f"Status: {r.status_code}")
pp(r.json())

# 5. Get instance by string ID 'node-exporter'
print("\n=== 5. GET INSTANCE by 'node-exporter' ===")
r = requests.get(f"{BASE}/instances/node-exporter", headers=headers)
print(f"Status: {r.status_code}")
pp(r.json())

# 6. Get instance by numeric ID
print("\n=== 6. GET INSTANCE by numeric '1' ===")
r = requests.get(f"{BASE}/instances/1", headers=headers)
print(f"Status: {r.status_code}")
pp(r.json())

# 7. CPU metrics by instance_id string
print("\n=== 7. CPU METRICS by 'i-0347ad6ae12bdb460' ===")
r = requests.get(f"{BASE}/metrics/cpu/i-0347ad6ae12bdb460", headers=headers)
print(f"Status: {r.status_code}")
pp(r.json())

# 8. Memory metrics by instance_id string
print("\n=== 8. MEMORY METRICS by 'node-exporter' ===")
r = requests.get(f"{BASE}/metrics/memory/node-exporter", headers=headers)
print(f"Status: {r.status_code}")
pp(r.json())

# 9. All metrics by instance_id string
print("\n=== 9. ALL METRICS by 'i-0347ad6ae12bdb460' ===")
r = requests.get(f"{BASE}/metrics/all/i-0347ad6ae12bdb460", headers=headers)
print(f"Status: {r.status_code}")
pp(r.json())

# 10. Dashboard summary
print("\n=== 10. DASHBOARD SUMMARY ===")
r = requests.get(f"{BASE}/metrics/dashboard/summary", headers=headers)
print(f"Status: {r.status_code}")
pp(r.json())

# 11. Health score (ML)
print("\n=== 11. ML HEALTH SCORE by 'i-0347ad6ae12bdb460' ===")
r = requests.get(f"{BASE}/ml/health-score/i-0347ad6ae12bdb460", headers=headers)
print(f"Status: {r.status_code}")
pp(r.json())

print("\n=== ALL TESTS COMPLETE ===")
