# Get Widevine L3 Decryption Keys

## Requirements

You need a **wvd** file named `l3.wvd`, placed in the same directory as `l3.exe`.

You can try the **wvd** file [here](https://forum.videohelp.com/threads/413719-Ready-to-use-CDMs-available-here%21), or refer to [here](https://forum.videohelp.com/threads/408031-Dumping-Your-own-L3-CDM-with-Android-Studio) to learn how to get `client_id.bin` and `private_key.pem`, and then run the following commands to get the **wvd** file:

```bash
# Install `pywidevine`, `pyaml`
pip install pywidevine pyaml

# Create `wvd` File
pywidevine create-device -k private_key.pem -c client_id.bin -t "CHROME" -l 3 -o wvd
```

## Usage

```bash
l3.exe [-h] [-wvd WVD] -pssh PSSH -lic_url LIC_URL [-lic_headers LIC_HEADERS]
```

### Options

 - `-pssh <PSSH>`                *require* PSSH
 - `-lic_url <LIC_URL>`          *require* License URL
 - `-lic_headers <LIC_HEADERS>`  License Headers
 - `-wvd <WVD>`                  wvd File. Default by "./l3.wvd"
 - `-h`, `--help`                show help message
 - `-v`, `--version`             show program's version number

### Example

```bash
l3.exe -pssh AAAAW3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAADsIARIQ62dqu8s0Xpa7z2FmMPGj2hoNd2lkZXZpbmVfdGVzdCIQZmtqM2xqYVNkZmFsa3IzaioCSEQyAA== -lic_url https://cwip-shaka-proxy.appspot.com/no_auth

# with -lic_header
l3.exe -pssh AAAANHBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAABQIARIQnrQFDeRLSAKTLifXUIPiZg== -lic_url https://drm-widevine-licensing.axtest.net/AcquireLicense -lic_header "{ \"x-axdrm-message\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoxLCJjb21fa2V5X2lkIjoiYjMzNjRlYjUtNTFmNi00YWUzLThjOTgtMzNjZWQ1ZTMxYzc4IiwibWVzc2FnZSI6eyJ0eXBlIjoiZW50aXRsZW1lbnRfbWVzc2FnZSIsImtleXMiOlt7ImlkIjoiOWViNDA1MGQtZTQ0Yi00ODAyLTkzMmUtMjdkNzUwODNlMjY2IiwiZW5jcnlwdGVkX2tleSI6ImxLM09qSExZVzI0Y3Iya3RSNzRmbnc9PSJ9XX19.4lWwW46k-oWcah8oN18LPj5OLS5ZU-_AQv7fe0JhNjA\" }"
```

## Development

**Require:** Python 3

```bash
# Install
pip install -r requirements.txt

# Build
pyinstaller -F l3.py
```
