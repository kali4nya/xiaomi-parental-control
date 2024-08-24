import requests
import time

cutoff_time = "23:00" #time to cutoff internet access
restore_time = "06:00" #time to restore internet access

mac = '4F:76:51:92:58:5F' # <- replace with mac address of the device you want to control (you can do a list for multiple devices)

ip = '192.168.31.1' # <- repalce with your router ip (default is usually 192.168.31.1)
username = 'admin' #router username (for xiaomi routers, it's admin by default)
password = 'password' # <- replace with your actuall router password

print("program started")
print("")
print("cutoff time set to: " + cutoff_time)
print("restore time set to: " + restore_time)
print("")
print("mac address set to: " + mac)
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
            print("login successful")
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

def main(): #main loop function
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == cutoff_time:
            ##################################################
            token = login(ip, username, password)
            ##################################################
            changeInternetAccessForDevice(ip, mac, 'disable', token)
            time.sleep(20)
        elif current_time == restore_time:
            ##################################################
            token = login(ip, username, password)
            ##################################################
            changeInternetAccessForDevice(ip, mac, 'enable', token)
            time.sleep(20)
        time.sleep(20)

if __name__ == "__main__":
    main()