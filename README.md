# xiaomi-parental-control

simple python script to run on a home server that controls internet access for specified devices
everything to set up is explained in code

**tested on xiaomi router 4A**

```python
cutoff_time = "23:00" #time to cutoff internet access
restore_time = "06:00" #time to restore internet access

mac = '4F:76:51:92:58:5F' # <- replace with mac address of the device you want to control (you can do a list for multiple devices)

ip = '192.168.31.1' # <- repalce with your router ip (default is usually 192.168.31.1)
username = 'admin' #router username (for xiaomi routers, it's admin by default)
password = 'password' # <- replace with your actuall router password
```
