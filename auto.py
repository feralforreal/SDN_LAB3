#! /bin/bash

import subprocess

b = "mybridge"
ip = "192.168.1.7"  
port = "6653"  

c1 = ["ovs-vsctl", "set-controller", b, f"tcp:{ip}:{port}"]
c2 = ["ovs-vsctl", "show"]
failovercmd = ["ovs-vsctl","get-fail-mode","mybridge"]

try:
   
    subprocess.check_call(c1)
        
    print(f"Controller added to {b}.")
    print(f"This is the result: ")
    subprocess.check_call(c2)
    if (subprocess.check_call(failovercmd)==''):
        print("No failovers Detected")
    else:
        print(subprocess.check_call(failovercmd))
except:
   
    print(f"Error adding controller to {b}: {e}")