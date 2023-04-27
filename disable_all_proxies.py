import requests
import json

# Variables to change
AUTH_EMAIL = "email@haxor.no" # email used to login to cloudflare dashboard
AUTH_KEY = "your_global_API_key" # locate in profile -> API Tokens in cloudflare website
ZONE_ID = "zone_id" # locate in overview tab in cloudflare website


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_zone_records():
    url = "https://api.cloudflare.com/client/v4/zones/" + ZONE_ID + "/dns_records"
    headers = {
        "X-Auth-Email": AUTH_EMAIL,
        "X-Auth-Key": AUTH_KEY,
        "Content-Type": "application/json"
    }
    params = {
        'per_page': 50000
    }
    request = requests.get(url, headers=headers, params=params)
    data = request.json()

    if data['success']:
        return data['result']
    else:
        return None

 
def disable_proxy(record):
    headers = {
        "X-Auth-Email": AUTH_EMAIL,
        "X-Auth-Key": AUTH_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record['id']}"
    data = json.dumps({
        'content': record['content'],
        'name': record['name'],
        'type': record['type'],
        'proxied': False
    })

    request = requests.patch(url, headers=headers, data=data)
    data = request.json()

    if data['success']:
        return True
    else:
        return False


def disable_proxy_on_records(records):
    updated_records = 0
    for i, record in enumerate(records):
        print(f"{i+1}/{len(records)} - Updating {record['name']}",end="")

        if disable_proxy(record):
            updated_records += 1
            print(f" - {bcolors.OKGREEN}OK{bcolors.ENDC}")
        else:
            print(f" - {bcolors.FAIL}FAILED!{bcolors.ENDC}")
    
    return updated_records


records = get_zone_records()
if records:
    updated_records = disable_proxy_on_records(records)
    print(f"DONE - Updated {updated_records}/{len(records)} records")
else:
    print("No records found")
