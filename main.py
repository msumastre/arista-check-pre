import paramiko

def collect_arista_commands(device, username, password):
    try:
        # Create an SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the device
        ssh_client.connect(device, username=username, password=password, timeout=10)

        # List of Arista commands to execute
        arista_commands = [
            "show version",
            "show interface status | no-more",
            "show lldp neighbors | no-more",
            "show ip bgp summary | no-more ",
            "show arp | no-more",
            "show mac address-table | no-more",
            "show inventory | no-more",
            "show port-channel summary",
            "show vlan | no-more",
            "show mlag detail | no-more",
            "show mlag interfaces | no-more",
            # Add more commands as needed
        ]

        # Open a file for writing the output
        with open(f"{device}_output.txt", "w") as output_file:
            # Execute each command and write the output to the file
            for command in arista_commands:
                stdin, stdout, stderr = ssh_client.exec_command(command)
                output_file.write(f"=== {command} ===\n")
                output_file.write(stdout.read().decode("utf-8"))
                output_file.write("\n")

        print(f"Command output for {device} saved to {device}_output.txt")

    except Exception as e:
        print(f"Error connecting to {device}: {str(e)}")

    finally:
        # Close the SSH connection
        ssh_client.close()

def main():
    # Prompt the user for device list, username, and password
    device_list = input("Enter a comma-separated list of devices: ").split(',')
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    # Iterate through each device and collect Arista commands
    for device in device_list:
        device = device.strip()  # Remove leading/trailing whitespaces
        collect_arista_commands(device, username, password)

if __name__ == "__main__":
    main()
