#! /bin/bash
import subprocess
try:
    #connect the controller to the ovs
    subprocess.check_call("sudo ovs-vsctl set-controller mybridge tcp:192.168.1.7:6653")       
    print(f"Controller added successfully")
    print(f"This is the result: ")
    subprocess.check_call("ovs-vsctl show")
    #print the failover mode
    if (subprocess.check_call()=='ovs-vsctl get-fail-mode mybridge'):
        print("No failovers Detected")
    else:
        print(subprocess.check_call('ovs-vsctl get-fail-mode mybridge'))
except:
    print(f"Error adding controller:")
