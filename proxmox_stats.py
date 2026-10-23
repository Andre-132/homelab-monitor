from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

prox_id = os.getenv("PROXMOX_TOKEN_ID")
prox_token = os.getenv("PROXMOX_TOKEN_SECRET")
prox_host = "https://192.168.1.4:8006/api2/json/nodes/pve/status"

# Build the URL
url = f"{prox_host}"
#print(url)

# Build the header
headers = {'authorization': f'{prox_id}{prox_token}'}
#print(headers)

# Send the request
response = requests.get(url, timeout=10, headers=headers, verify="pve-root-ca.pem")
# print(response.status_code)

# Convert response to python data
data = response.json()
readable_json = json.dumps(data, indent=2)
# print(readable_json)

#pull out raw values
node = data["data"]

memory_used = node.get("memory", {}).get("used")
memory_total = node.get("memory", {}).get("total")
cpu_used = node.get("cpu")
io_wait = node.get("wait")
cpu_cores = node.get("cpuinfo", {}).get("cpus")
uptime = node.get("uptime")
print(uptime)
