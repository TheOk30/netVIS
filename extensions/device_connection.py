import netmiko
from netmiko import ConnectHandler

class DeviceConnection:
    def __init__(self, connection_name:str, host:str, username:str = "admin",
                  password:str = "admin", device_type:str = "unknown"):
        """
        Initializes a DeviceConnection instance.

        Args:
            device (dict): A dictionary containing device connection details.
                Example:
                {
                    "device_type": "cisco_ios",
                    "host": "192.168.1.1",
                    "username": "admin",
                    "password": "password",
                    "port": 22
                }
        """
        self.__device = device
        self.__connection_name = connection_name
        self.__connection = None

    def connect(self):
        """Establishes an SSH connection to the device."""
        try:
            self.__connection = ConnectHandler(**self.__device)
            print(f"Successfully connected to {self.__device['host']}")
        except Exception as e:
            print(f"An error occurred while connecting to {self.__device['host']}: {e}")

    def disconnect(self):
        """Closes the SSH connection to the device."""
        if self.__connection:
            self.__connection.disconnect()
            print(f"Disconnected from {self.__device['host']}")

    def send_command(self, command):
        """
        Sends a command to the device and returns the output.

        Args:
            command (str): The command to send to the device.

        Returns:
            str: The output of the command.
        """
        if not self.__connection:
            print("Connection not established. Please call connect() first.")
            return ""

        try:
            output = self.__connection.send_command(command)
            return output
        except Exception as e:
            print(f"An error occurred while sending command: {e}")
            return ""
