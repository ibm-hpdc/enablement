#!/usr/bin/env python

# ============================================================
# Import modules
# ============================================================

import argparse
import getpass
import requests
import json
import jsonschema
import sys
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
# function to wait for an asynchronous request to complet
# ============================================================

def api_wait(hpdchost, s, response, timeout, timewait):
    timer = 0
    print(response)
    while timer < timeout:
        if response.status_code == 200:
            parsed = json.loads(response.content)
            print(json.dumps(parsed, indent=2, sort_keys=True))
            break
        if response.status_code != 202:
            print("***** Request failed")
            print(response)
            break
        time.sleep(timewait)
        timer += timewait
        response_uuid = json.loads(response.content.decode('utf8')).get("uuid")
        status_url = f"https://{hpdchost}:19443/requests/{str(response_uuid)}"
        response = s.get(status_url, headers=api_headers, verify=False)
        print(response)

# ============================================================
# Parse command line options and prompt for input if needed
# ============================================================

parser = argparse.ArgumentParser(description='A sample python script to get DB connection information.')
parser.add_argument('--host', '-H', help='Data Controller host')
parser.add_argument('--user', '-u', help='API user')
parser.add_argument('--password', '-p', help='API user password')
parser.add_argument('--policy', '-P', help='Policy name')
parser.add_argument('--token', '-t', help='Token used to activate the policy')

args = parser.parse_args()
if args.host:
   hpdchost = args.host
else:
   hpdchost = input('HPDC host: ')

if args.user:
   username = args.user
else:
   username = input('API user: ')

if args.password:
   password = args.password
else:
   password = getpass.getpass(prompt='Password for the API user: ')

if args.policy:
   policy = args.policy
else:
   policy = input('Policy name: ')

if args.token:
   token = args.token
else:
   token = getpass.getpass(prompt='Token for activating the policy: ')

# ============================================================
# Set common REST API options
# ============================================================

api_headers = {"x-csrf-ibmhpdc-header":"1", "Content-Type":"application/json"}

# ============================================================
# Register the API user
# ============================================================

print('***** Register the API user')

s = requests.Session()
s.auth = (username, password)

url = f'https://{hpdchost}:19443/register'
body = {"username": username, "password": password}    
response = s.post(url, headers=api_headers, json=body, verify=False)
print ('*** Response code {}'.format(response.status_code))
if response.status_code != 200:
    print('*** Request failed')
    sys.exit(1)

# ============================================================
# Activate a policy
# ============================================================

print('***** Activate a policy')

url = f'https://{hpdchost}:19443/policies/{policy}/activate'
body = {"token": token}    
response = s.post(url, headers=api_headers, json=body, verify=False)
print ('*** Register response code {}'.format(response.status_code))
if response.status_code == 202:
   api_wait(hpdchost, s, response, 60, 10)
else:
   print('***** Request failed')

# ============================================================
# Unregister the API user
# ============================================================

print('*** Unregister the API user')

url = f'https://{hpdchost}:19443/register'
body = {"username": username, "password": password}
response = s.delete(url, headers=api_headers, json=body, verify=False)
print ('***** Register response code {}'.format(response.status_code))

sys.exit(0)
