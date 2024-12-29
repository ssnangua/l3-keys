import json
import argparse
import l3

# Command line arguments
parser = argparse.ArgumentParser(description='Get Widevine L3 Decryption Keys')
parser.add_argument('-v', '--version', action='version', version='1.0.0')
parser.add_argument('-wvd', default=r'./l3.wvd', help='wvd File. Default by "./l3.wvd"')
parser.add_argument('-pssh', help='PSSH', required=True)
parser.add_argument('-lic_url', help='License URL', required=True)
parser.add_argument('-lic_headers', type=json.loads, help='License Headers')
args = parser.parse_args()

# Get arguments
wvd, pssh, lic_url, lic_headers = args.wvd, args.pssh, args.lic_url, args.lic_headers

# Get decryption keys
keys = l3.get_keys(wvd, pssh, lic_url, lic_headers)

# Print keys
print(json.dumps(keys))
