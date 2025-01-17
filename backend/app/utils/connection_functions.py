import paramiko
import time
from .extra_functions import check_for_more, is_timed_out
from models.device_type import get_all_output_type, get_device_type


def detect_device_type(host, username, password, timeout=20):
    """
    Detects the device type of a router based on the response to 'show version' or similar commands.
    Handles paginated output (e.g., --More--).
    Returns the device type as a string (e.g., 'cisco_ios', 'cisco_nxos') or 'unknown' if it cannot be determined.
    """
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the router
        client.connect(hostname=host, username=username, password=password, look_for_keys=False, allow_agent=False)
        print(f"Connected to {host}")

        # Open an interactive shell session
        remote_conn = client.invoke_shell()
        time.sleep(1)  # Wait briefly for the initial prompt
        remote_conn.recv(1000)  # Clear any initial banner

        # Send the command
        remote_conn.send("show version\n")
        output = ""
        start_time = time.time()

        while True:
            if remote_conn.recv_ready():
                chunk = remote_conn.recv(5000).decode("utf-8", errors="ignore")
                output += chunk
                print(chunk)  # Debug: Print received chunk

                # Check for pagination prompt '--More--'
                if check_for_more(chunk): 
                      # Send space to get the next page
                      remote_conn.send(" ")
                else:
                    break
            else:
                time.sleep(0.5)  # Avoid busy-waiting

            # Break if timeout is reached
            if is_timed_out(start_time, timeout):
                print("Timed out waiting for command output.")
                raise Exception("Connection timeout")

        # Close connection
        client.close()

        # Analyze output to determine device type
        for type in get_all_output_type():
            if type in output:
                return get_device_type(type)
        return "unknown"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "unknown"
