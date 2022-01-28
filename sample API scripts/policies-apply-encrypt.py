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
# Parse command line options and prompt for input if needed
# ============================================================

parser = argparse.ArgumentParser(description='A sample python script to get DB connection information.')
parser.add_argument('--host', '-H', help='Data Controller host')
parser.add_argument('--user', '-u', help='API user')
parser.add_argument('--password', '-p', help='API user password')
parser.add_argument('--column', '-c', help='Column name to be matched')
parser.add_argument('--data', '-d', help='Data to be encrypted')

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

if args.column:
   column = args.column
else:
   column = input('Column name to be matched: ')

if args.data:
   data = args.data
else:
   data = input('Data to be encrypted: ')

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
print ('***** Response code {}'.format(response.status_code))
if response.status_code != 200:
   print('***** Request failed')
   sys.exit(1)

# ============================================================
# Encrypt a field
# ============================================================

print('***** Encrypt a field into EDO')
print(column)
print(data)
url = f"https://{hpdchost}:19443/policies/apply"
body = {"targetPersona":"TZ1","data":{column:data}}
response = s.post(url, headers=api_headers, json=body, verify=False)
print ('***** Response code {}'.format(response.status_code))
if response.status_code == 200:
   parsed = json.loads(response.content)
   print(json.dumps(parsed, indent=2, sort_keys=True))
else:
   print('***** Request failed')

# ============================================================
# Unregister the API user
# ============================================================

print('***** Unregister the API user')

url = f'https://{hpdchost}:19443/register'
body = {"username": username, "password": password}
response = s.delete(url, headers=api_headers, json=body, verify=False)
print ('***** Response code {}'.format(response.status_code))

sys.exit(0)
