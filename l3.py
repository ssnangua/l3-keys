from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
import requests
import json
import argparse

# Command Line Arguments
parser = argparse.ArgumentParser(description='Get Widevine L3 Decryption Keys')
parser.add_argument('-v', '--version', action='version', version='1.0.0')
parser.add_argument('-wvd', default=r'./l3.wvd', help='wvd File. Default by "./l3.wvd"')
parser.add_argument('-pssh', help='PSSH', required=True)
parser.add_argument('-lic_url', help='License URL', required=True)
parser.add_argument('-lic_headers', type=json.loads, help='License Headers')
args = parser.parse_args()

# Get Arguments
wvd, pssh, lic_url, lic_headers = args.wvd, args.pssh, args.lic_url, args.lic_headers

# Load Device
device = Device.load(wvd)

# Load CDM
cdm = Cdm.from_device(device)

# Open CDM
session_id = cdm.open()

# Get License Challenge
challenge = cdm.get_license_challenge(session_id, PSSH(pssh))

# Send License Challenge
licence = requests.post(lic_url, headers=lic_headers, data=challenge)
licence.raise_for_status()

# Parse License
cdm.parse_license(session_id, licence.content)

# Get Decryption Keys
keys = []
for key in cdm.get_keys(session_id):
    if key.type=='CONTENT':
        keys += [f'{key.kid.hex}:{key.key.hex()}']

# Close CDM
cdm.close(session_id) 

# Print Keys
print(json.dumps(keys))