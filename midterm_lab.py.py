import paramiko
import getpass
import pexpect

# Replace these with your router's and VM's information
router_ip = '192.168.100.1'
vm_ip = '192.168.100.2'
controller_ip = '10.20.30.2'
controller_port = '6653'
routers = ['192.168.200.1', '172.16.100.2', '10.20.30.1']  # Replace with the actual IP addresses of R1, R2, and R3
router_user = 'username'
router_pass = 'password'
username = 'username'
password = 'password'
sudo_password = 'mininet'  # Password for sudo mn

try:
    # Create an SSH client instance for the router
    ssh_client_router = paramiko.SSHClient()
    ssh_client_router.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the router
    ssh_client_router.connect(router_ip, username=username, password=password)

    # Run the command to retrieve DHCP server bindings on the router
    router_command = "show ip dhcp binding"
    stdin, stdout, stderr = ssh_client_router.exec_command(router_command)

    # Read and print the DHCP bindings on the router
    dhcp_bindings = stdout.read().decode('utf-8')
    print("Router DHCP Bindings:")
    print(dhcp_bindings)

    # Close the router SSH connection
    ssh_client_router.close()

    # Create an SSH client instance for the VM
    ssh_client_vm = paramiko.SSHClient()
    ssh_client_vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the VM
    ssh_client_vm.connect(vm_ip, username=username, password=password)

    # Use pexpect to interactively provide the password for 'sudo mn'
    child = pexpect.spawn(f'ssh {username}@{vm_ip} sudo mn --switch ovsk --controller remote,ip={controller_ip},port={controller_port},protocol=OpenFlow13')
    child.expect('Password:')
    child.sendline(sudo_password)
    child.expect('mininet>')
    print ("==================================")
    print("initialize the mininet.")
    print ("===================================")
    # SSH into routers R1, R2, and R3 to configure routing
    for router in routers:
        child.sendline(f'ssh {router_user}@{router}')
        child.expect(f'{router_user}@{router}\'s password:')
        child.sendline(router_pass)
        child.expect(f'{router}#')
        
        # Configure routing settings for OpenFlow connectivity
        child.sendline('configure terminal')
        child.expect(f'{router}(config)#')
        child.sendline('ip route 0.0.0.0 0.0.0.0 {controller_ip}')
        child.expect(f'{router}(config)#')
        child.sendline('end')
        child.expect(f'{router}#')
        child.sendline('exit')
        child.expect(f'{router_user}@{router}#')

    print("Routing configured on routers R1, R2, and R3 for OpenFlow connectivity.")

    # Exit Mininet
    child.sendline('exit')

    print("Mininet initialized on the VM with OvS and OpenFlow13 connected to the controller.")

    # Close the VM SSH connection
    ssh_client_vm.close()

except paramiko.AuthenticationException:
    print("Authentication failed. Check your username and password.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    ssh_client_router.close()