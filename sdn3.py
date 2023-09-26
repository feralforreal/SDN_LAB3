import subprocess
import time
import re
import json
from scapy.all import *

pcap_file = "imp.pcap"
json_file = "connected.txt"
of_connect_pattern = re.compile(r".*OpenFlowConnectionHandler.*Connected to OpenFlow switch (\d+).*")
switch_info = {}
controller_ip = "10.224.78.5"  # Replace with your controller's IP address
tdump = ["sudo", "tcpdump", "-i", "any", "-w", pcap_file]
try:
    tcpdump_process = subprocess.Popen(tdump)
    print("Packet capture started. Capturing for 10 seconds...")
    time.sleep(30) 
except KeyboardInterrupt:
    print("\nCapture stopped by user.")
finally:
    if 'tcpdump_process' in locals():
        tcpdump_process.terminate()
        tcpdump_process.wait()

text_file_path = 'cap.txt'

with open(text_file_path, 'r') as file:
    t_data = file.read()
print(t_data)
dpidp = r"Datapath unique ID: (0x[0-9a-fA-F]+)"
dst_ip= r"Dst: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
dpids = re.findall(dpidp, t_data)
dst_ips = re.findall(dst_ip, t_data)
if not dpids:
    print("")
else:
    for index, (dpid, dst_ip) in enumerate(zip(dpids, dst_ips), start=1):
        print("Entry {}: DPID: {}, IP: {}".format(index, dpid, dst_ip))
        switch_info[dpid] = {
            "ip_address": dst_ip,
            "status": "connected" if dpid in text_data else "not connected"
        }
with open(json_file, 'w') as json_file:
    json.dump(switch_info, json_file, indent=4)
