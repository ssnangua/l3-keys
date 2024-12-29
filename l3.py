from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.pssh import PSSH
import requests

# Get decryption keys
def get_keys(wvd, pssh, lic_url, lic_headers):

    # Load device
    device = Device.load(wvd)

    # Load CDM
    cdm = Cdm.from_device(device)

    # Open CDM
    session_id = cdm.open()

    # Get license challenge
    challenge = cdm.get_license_challenge(session_id, PSSH(pssh))

    # Send license challenge
    licence = requests.post(lic_url, headers=lic_headers, data=challenge)
    licence.raise_for_status()

    # Parse license
    cdm.parse_license(session_id, licence.content)

    # Get decryption keys
    keys = []
    for key in cdm.get_keys(session_id):
        if key.type=='CONTENT':
            keys += [f'{key.kid.hex}:{key.key.hex()}']

    # Close CDM
    cdm.close(session_id) 

    # Return keys
    return keys
