from dotenv import load_dotenv
import os
import requests

load_dotenv()

prox_id = os.getenv("PROXMOX_TOKEN_ID")
prox_token = os.getenv("PROXMOX_TOKEN_SECRET")
prox_host = os.getenv("PROXMOX_HOST")

# Build the URL
url = f"{prox_host}"
#print(url)

# Build the header
headers = {'authorization': f'{prox_id}{prox_token}'}
#print(headers)

# Send the request
response = requests.get(url, timeout=10, headers=headers, verify="pve-root-ca.pem")
print(response.status_code)


