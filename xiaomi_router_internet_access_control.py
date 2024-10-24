import requests
import time
import threading
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import re
import json

cutoff_time = "00:00"  # Time to cutoff internet access
restore_time = "05:30"  # Time to restore internet access
mac = ['2C:F0:5D:72:BF:F0', 'E6:45:8B:93:84:3D', '2C:D9:74:1B:85:DF']  # <- Replace with MAC address of the device you want to control

ip = '192.168.31.1'  # <- Replace with your router IP (default is usually 192.168.31.1)
username = 'admin'  # Router username (for Xiaomi routers, it's admin by default)
password = 'password'  # <- Replace with your actual router password
host_an_interface_server = True
server_port = 8000

macListAsString = ""
if isinstance(mac, list):
    for adres in mac:
        macListAsString += adres + ", "

print("Program started")
print("")
print("Cutoff time set to: " + cutoff_time)
print("Restore time set to: " + restore_time)
print("")
if isinstance(mac, list):
    print("MAC address set to: " + macListAsString)
else:
    print("MAC address set to: " + mac)
print("")


def login(ip, username, password):
    session = requests.Session()

    url = f"http://{ip}/cgi-bin/luci/api/xqsystem/login"
    payload = {
        "username": username,
        "password": password
    }
    response = session.post(url, data=payload)
    if response.status_code == 200:
        token = response.json().get('token')
        if token:
            print("Login successful")
            return token


def macAddressEncoding(mac):
    mac_encoded = mac.replace(':', '%3A')
    return mac_encoded


def changeInternetAccessForDevice(ip, device_mac_not_encoded, action, token):
    session = requests.Session()

    if isinstance(device_mac_not_encoded, list):
        for mac in device_mac_not_encoded:
            wan_value = 0 if action == 'disable' else 1
            url = f'http://{ip}/cgi-bin/luci/;stok={token}/api/xqsystem/set_mac_filter?mac={macAddressEncoding(mac)}&wan={wan_value}'
            response = session.get(url)
            if response.ok:
                print(f"Action '{action}' performed successfully for device {mac}")
    else:
        wan_value = 0 if action == 'disable' else 1
        url = f'http://{ip}/cgi-bin/luci/;stok={token}/api/xqsystem/set_mac_filter?mac={macAddressEncoding(device_mac_not_encoded)}&wan={wan_value}'
        response = session.get(url)
        if response.ok:
            print(f"Action '{action}' performed successfully for device {device_mac_not_encoded}")


class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        global cutoff_time, restore_time, mac  # Declare global variables
        if self.path == '/get_times':  # Endpoint to return cutoff_time and restore_time
            response_data = {
                'devices': mac,
                'cutoff_time': cutoff_time,
                'restore_time': restore_time
            }

            # Send the JSON response properly formatted
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))  # Properly format the response using json.dumps()
        else:
            if self.path == '/':  # Serve index.html or interface.html
                self.path = '/index.html'  
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        global cutoff_time, restore_time, mac  # Declare global variables
        if self.path == '/execute':  # Define the endpoint for execution
            content_length = int(self.headers['Content-Length'])  # Get the size of the data
            post_data = self.rfile.read(content_length)  # Read the data
            data_dict = parse_qs(post_data.decode('utf-8'))  # Parse the query string
            data = data_dict.get('data', [''])[0]  # Extract the data value
            
            data = data.split('&')
            devices = data[0].split(',')
            cutoff_time = data[1].split('=')[1]  # Update global cutoff_time
            restore_time = data[2].split('=')[1]  # Update global restore_time
            
            for device in devices:
                if not is_valid_mac_address(device):
                    devices = None
            if devices is not None:
                mac = devices  # Update global mac
                print(f"Devices set to: {devices}")
            print(f"Cutoff time set to: {cutoff_time} through the web interface")
            print(f"Restore time set to: {restore_time} through the web interface")
            
            # Send a response back to the client
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Executed successfully!')


def is_valid_mac_address(mac):
    mac_regex = re.compile(r'^([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})$')
    return bool(mac_regex.match(mac))


def start_web_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Ensure the correct directory is used
    server_address = ('0.0.0.0', server_port)  # Serve on all IPs, specified port
    httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
    print(f"Serving 'index.html' at http://localhost:{server_port}")  # Print server address
    httpd.serve_forever()


def main():  # Main loop function
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == cutoff_time:
            token = login(ip, username, password)
            changeInternetAccessForDevice(ip, mac, 'disable', token)
            time.sleep(20)
        elif current_time == restore_time:
            token = login(ip, username, password)
            changeInternetAccessForDevice(ip, mac, 'enable', token)
            time.sleep(20)
        time.sleep(20)


if __name__ == "__main__":
    if host_an_interface_server:
        web_thread = threading.Thread(target=start_web_server)
        web_thread.daemon = True  # Allows the web server to exit when the main program exits
        web_thread.start()
    main()
