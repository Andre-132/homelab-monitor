from dotenv import load_dotenv
import os
import requests
import json
from requests.exceptions import Timeout, ConnectionError, RequestException, HTTPError
import sys

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
timeout_duration = (10)

# Build the header
headers = {'authorization': f'{prox_id}{prox_token}'}
#print(headers)

def get_node_status():
# Send the request

    try:
        response = requests.get(url, timeout=timeout_duration, headers=headers, verify="pve-root-ca.pem")
        response.raise_for_status()
    except Timeout:
        print("Error: The request timed out while connecting or reading the response.")
        sys.exit(1)
    except ConnectionError:
        print(f"Error: failed to connect to server at {prox_host}")
        sys.exit(1)
    except HTTPError:
        print(f"Error: Proxmox returned {response.status_code}. Check your API token in .env and its permissions.")
        sys.exit(1)
    except RequestException as e:
        print(f"Error: unexpected problem with the request: {e}")
        sys.exit(1)
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

    return {
    "cpu_percent": fraction_to_percent(cpu_used),
    "io_wait_percent": fraction_to_percent(io_wait),
    "cores": cpu_cores,
    "memory_used_gb": bytes_to_gb(memory_used),
    "memory_total_gb": bytes_to_gb(memory_total),
    "memory_percent": memory_percent(memory_used, memory_total),
    "uptime_days": seconds_to_days(uptime)
}

if __name__ == "__main__":
    status = get_node_status()

# print(memory_used, memory_total, cpu_used, io_wait, cpu_cores, uptime)
print(f"CPU: {status['cpu_percent']}% ({status['cores']} cores)")
print(f"IO wait: {status['io_wait_percent']}%")
print(f"Memory: {status['memory_used_gb']} / ({status['memory_total_gb']}) Percentage Used: ({status['memory_percent']}%)")
print(f"Uptime: {status['uptime_days']} days")