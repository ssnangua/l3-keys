# Get Widevine L3 Decryption Keys

## Requirements

You need a **wvd** file named `l3.wvd`, placed in the same directory as `l3.py` or `l3.exe`.

You can refer to [here](https://forum.videohelp.com/threads/408031-Dumping-Your-own-L3-CDM-with-Android-Studio) to learn how to get `client_id.bin` and `private_key.pem`, and then run the following command to get the **wvd** file:

```bash
# Install `pywidevine`, `pyaml`
pip install pywidevine pyaml
# Create `wvd` File
pywidevine create-device -k private_key.pem -c client_id.bin -t "CHROME" -l 3 -o wvd
```

## Usage

```bash
py l3.py [-h] [-wvd WVD] -pssh PSSH -lic_url LIC_URL [-lic_headers LIC_HEADERS]

l3.exe [-h] [-wvd WVD] -pssh PSSH -lic_url LIC_URL [-lic_headers LIC_HEADERS]
```

## Example

```bash
l3.exe -pssh AAAANHBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAABQIARIQnrQFDeRLSAKTLifXUIPiZg== -lic_url https://drm-widevine-licensing.axtest.net/AcquireLicense -lic_header "{ \"x-axdrm-message\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoxLCJjb21fa2V5X2lkIjoiYjMzNjRlYjUtNTFmNi00YWUzLThjOTgtMzNjZWQ1ZTMxYzc4IiwibWVzc2FnZSI6eyJ0eXBlIjoiZW50aXRsZW1lbnRfbWVzc2FnZSIsImtleXMiOlt7ImlkIjoiOWViNDA1MGQtZTQ0Yi00ODAyLTkzMmUtMjdkNzUwODNlMjY2IiwiZW5jcnlwdGVkX2tleSI6ImxLM09qSExZVzI0Y3Iya3RSNzRmbnc9PSJ9XX19.4lWwW46k-oWcah8oN18LPj5OLS5ZU-_AQv7fe0JhNjA\" }"
```

## Development

```bash
# Install
pip3 install -r requirements.txt

# Build
pyinstaller -F l3.py
```
