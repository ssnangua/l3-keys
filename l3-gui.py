from tkinter import *
import ctypes
import os
import tkinter.filedialog as filedialog
import json
import l3
import webbrowser

version = '1.0.0'

def update_wvd(wvd_path):
    wvd_entry.config(state='normal')
    wvd_entry.delete(0, 'end')
    wvd_entry.insert('end', wvd_path)
    wvd_entry.config(state='readonly')

def select_wvd():
    wvd_path = filedialog.askopenfilename(filetypes=[("WVD files", "*.wvd")])
    update_wvd(wvd_path)

def get_keys():
    # Get the values from the GUI
    wvd = wvd_entry.get()
    pssh = pssh_entry.get().strip()
    lic_url = lic_url_entry.get().strip()
    lic_headers = lic_headers_text.get('1.0', 'end').strip()

    # Validate arguments
    if not os.path.exists(wvd):
        return output_error('WVD file does not exist')
    
    if pssh == '' or lic_url == '':
        return output_error('PSSH and License URL cannot be empty')

    lic_headers_json = {}
    if lic_headers != '':
        try:
            lic_headers_json = json.loads(lic_headers)
        except Exception as e:
            return output_error('License headers must be valid JSON')

    # Get decryption keys
    try:
        keys = l3.get_keys(wvd, pssh, lic_url, lic_headers=lic_headers_json)
        output_keys(keys)
    except Exception as e:
        output_error(e)

def output(text):
    result_text.config(state='normal')
    result_text.delete('1.0', 'end')
    result_text.insert('1.0', text)
    result_text.see('1.0')
    result_text.config(state='disabled')

def output_keys(keys):
    text = '\n'.join(keys)
    output(text)
    # Copy to clipboard
    result_text.clipboard_clear()
    result_text.clipboard_append(text)

def output_error(msg):
    output(f'Error: {msg}')

# Window
window = Tk()
window.title(f'Get Widevine L3 Decryption Keys {version}')
window.resizable(False, False)

# Fix DPI scaling issues
ctypes.windll.shcore.SetProcessDpiAwareness(1)
scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
window.tk.call('tk', 'scaling', scale_factor/75)

# Frame
frame = Frame(window)
frame.pack(padx=20, pady=20)

def add_label(text='', pady=(0, 0)):
    label = Label(frame, text=text)
    label.pack(anchor='w', pady=pady)
    return label

def add_entry(pady=(0, 0)):
    entry = Entry(frame)
    entry.pack(fill='both', pady=pady, ipady=10)
    return entry

def add_text(height=5, pady=(0, 0), state='normal'):
    # Container
    box = Frame(frame)
    box.pack(fill='both', pady=pady)
    # Scrollbar
    scrollbar = Scrollbar(box, orient='vertical')
    scrollbar.grid(row=0, column=1, sticky='nsew')
    # Text
    text = Text(box, height=height, width=70, undo=True, state=state)
    text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
    # Associate the scrollbar and text widget
    text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=text.yview)
    return text

# WVD
wvd_box = Frame(frame)
wvd_box.pack(fill='both')
wvd_label = Label(wvd_box, text='* WVD File: ')
wvd_label.grid(row=0, column=0)
wvd_entry = Entry(wvd_box, state='readonly')
wvd_entry.grid(row=0, column=1, sticky='ew', ipady=10)
wvd_button = Button(wvd_box, text='Select File', command=select_wvd)
wvd_button.grid(row=0, column=2)
wvd_box.columnconfigure(1, weight=1)

# PSSH
pssh_label = add_label(text='* PSSH:', pady=(20, 0))
pssh_entry = add_entry(pady=(10, 0))

# License URL
lic_url_label = add_label(text='* License URL:', pady=(20, 0))
lic_url_entry = add_entry(pady=(10, 0))

# License Headers
lic_headers_label = add_label(text='License Headers:', pady=(20, 0))
lic_headers_text = add_text(height=10, pady=(10, 0))

# Get Keys
get_keys_button = Button(frame, text='GET KEYS', command=get_keys)
get_keys_button.pack(anchor='e', pady=20)

# Result
result_label = add_label(text='Result:')
result_text = add_text(height=5, pady=(10, 0), state='disable')

# About
about_label = Label(frame, text='github@ssnangua', fg='#c0c4cc', cursor="hand2")
about_label.pack(anchor='w', pady=(20, 0))
about_label.bind("<Enter>", lambda e: about_label.config(fg='#409eff'))
about_label.bind("<Leave>", lambda e: about_label.config(fg='#c0c4cc'))
about_label.bind("<Button-1>", lambda e: webbrowser.open('https://github.com/ssnangua/l3-keys'))

# Auto select WVD file
wvd_path = None
for root, dirs, files in os.walk(r'./'):
    for file in files:
        if file.lower().endswith('.wvd'):
            wvd_path = os.path.join(root, file)
            update_wvd(wvd_path)
            break
    if wvd_path is not None:
        break

""" 
# Test
pssh_entry.insert('end', 'AAAANHBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAABQIARIQnrQFDeRLSAKTLifXUIPiZg==')
lic_url_entry.insert('end', 'https://drm-widevine-licensing.axtest.net/AcquireLicense')
lic_headers_text.insert('1.0', '{\n  "accept": "*/*",\n  "accept-language": "zh-CN,zh;q=0.9",\n  "priority": "u=1, i",\n  "sec-ch-ua": "\\"Google Chrome\\";v=\\"131\\", \\"Chromium\\";v=\\"131\\", \\"Not_A Brand\\";v=\\"24\\"",\n  "sec-ch-ua-mobile": "?0",\n  "sec-ch-ua-platform": "\\"Windows\\"",\n  "sec-fetch-dest": "empty",\n  "sec-fetch-mode": "cors",\n  "sec-fetch-site": "cross-site",\n  "x-axdrm-message": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoxLCJjb21fa2V5X2lkIjoiYjMzNjRlYjUtNTFmNi00YWUzLThjOTgtMzNjZWQ1ZTMxYzc4IiwibWVzc2FnZSI6eyJ0eXBlIjoiZW50aXRsZW1lbnRfbWVzc2FnZSIsImtleXMiOlt7ImlkIjoiOWViNDA1MGQtZTQ0Yi00ODAyLTkzMmUtMjdkNzUwODNlMjY2IiwiZW5jcnlwdGVkX2tleSI6ImxLM09qSExZVzI0Y3Iya3RSNzRmbnc9PSJ9XX19.4lWwW46k-oWcah8oN18LPj5OLS5ZU-_AQv7fe0JhNjA"\n}')
 """

# Start
window.mainloop()
