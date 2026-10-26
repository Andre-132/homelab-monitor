from dotenv import load_dotenv
import os
import requests
import json

def bytes_to_gb(b):
    return round(b / (1024 * 1024 * 1024), 2)
# print(bytes_to_gb(21530423296))   

def fraction_to_percent(f):
    return round(f * 100, 2)
# print(fraction_to_percent(0.0571204967800347))

def seconds_to_days(s):
    return round(s / 86400, 2)
# print(seconds_to_days(5364363))

def memory_percent(used, total):
    try:
        return round(used / total * 100, 1)
    except ZeroDivisionError:
        return 0
# print(memory_percent(21530423296, 33631784960))

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
# print(memory_used, memory_total, cpu_used, io_wait, cpu_cores, uptime)

print(f"CPU: {fraction_to_percent(cpu_used)}% ({cpu_cores} cores)")
print(f"IO wait: {fraction_to_percent(io_wait)}%")
print(f"Memory: {bytes_to_gb(memory_used)} / {bytes_to_gb(memory_total)} GB ({memory_percent(memory_used, memory_total)}%)")
print(f"Uptime: {seconds_to_days(uptime)} days")