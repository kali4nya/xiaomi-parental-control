# xiaomi-parental-control

simple python script to run on a home server that controls internet access for specified devices

everything to set up is explained in code

**tested on xiaomi router 4A** and python 3.12

```python
cutoff_time = "00:00"  # Time to cutoff internet access
restore_time = "05:30"  # Time to restore internet access
mac = ['2C:F0:5D:72:BF:F0', 'E6:45:8B:93:84:3D', '2C:D9:74:1B:85:DF']  # <- Replace with MAC address of the device you want to control

ip = '192.168.31.1'  # <- Replace with your router IP (default is usually 192.168.31.1)
username = 'admin'  # Router username (for Xiaomi routers, it's admin by default)
password = 'password'  # <- Replace with your actual router password
host_an_interface_server = True
server_port = 8000
```
in this version there is an interface that the user can access on "{serverIP}:{port set in code}"
by default the port is set to 8000, the interface loads data from the program everytime it is loaded
and sets data to server everytime the 'Submit' button is clicked, devices in the list in the interface
need to be seperated by commas

interface:

![image](https://github.com/user-attachments/assets/d6ad75da-e49b-4131-b2e3-39167af6b167)

If you have any problems/issues/questions let me know, Im happy to help :3
