"""
Author: Alireza Ghaderi
Email: p30planets@gmail.com
GitHub: alireza787b
Repository: github.com/alireza787b/mavsdk_drone_show
Date: June 2023
---------------------------------------------------------------------------

Ground Control Station (GCS) Script for Drone Telemetry and Command Control
---------------------------------------------------------------------------

This script is designed to function as a Ground Control Station (GCS) in a drone network, providing functionality for receiving telemetry data from drones and
sending commands to them. The script communicates with the drones over User Datagram Protocol (UDP), and it can be easily configured and expanded to 
handle multiple drones simultaneously.

Setup and Configuration:
------------------------
The script is set up to read its configuration from a .csv file named 'config.csv' which should be located in the same directory as the script. The columns
in 'config.csv' should be as follows: hw_id, pos_id, x, y, ip, mavlink_port, debug_port, gcs_ip.

Each row in 'config.csv' corresponds to a drone. The 'hw_id' column indicates the hardware ID of the drone, the 'pos_id' gives its position ID, 'x' and 'y'
provide coordinates, 'ip' specifies the drone's IP address, 'mavlink_port' and 'debug_port' provide the ports for MAVLink communication and debug information,
and 'gcs_ip' specifies the IP address of the GCS.

The script is designed to work with a specific drone determined by the hardware ID specified in a file named 'i.hwID', where 'i' is the hardware ID of the drone.
This file should also be located in the same directory as the script.

Sim Mode:
---------
The script includes a 'sim_mode' boolean variable that allows the user to switch between simulation mode and real-world mode. When 'sim_mode' is set to True,
the script is in simulation mode, and the IP address of the coordinator (essentially the drone control node) should be manually defined in the code. 
If 'sim_mode' is False, the script uses the IP address from 'config.csv' for the drone with the hardware ID matching that in 'i.hwID'.

Communication Protocol:
-----------------------
The script communicates with the drone over UDP using binary packets. For telemetry data, these packets have the following structure:

- Header (1 byte): A constant value of 77. 
- HW_ID (1 byte): The hardware ID of the drone.
- Pos_ID (1 byte): The position ID of the drone.
- State (1 byte): The current state of the drone.
- Trigger Time (4 bytes): The Unix timestamp when the data was sent.
- Terminator (1 byte): A constant value of 88.

For commands, the packets have a similar structure, but the header value is 55 and the terminator value is 66.

Each part of the packet is packed into a binary format using the struct.pack method from Python's 'struct' library.
The '=' character ensures that the bytes are packed in standard size, 'B' specifies an unsigned char (1 byte), and 'I' specifies an unsigned int (4 bytes).

Example:
--------
For example, a command packet could look like this in binary:

Header = 55 (in binary: 00110111)
HW_ID = 3 (in binary: 00000011)
Pos_ID = 3 (in binary: 00000011)
State = 1 (in binary: 00000001)
Trigger Time = 1687840743 (in binary: 11001010001100001101101100111111)
Terminator = 66 (in binary: 01000010)

The whole packet in binary would look like this:
00110111 00000011 00000011 00000001 11001010001100001101101100111111 01000010

Please note that the actual binary representation would be a sequence of 8-bit binary numbers.
The above representation is simplified to demonstrate the concept.

Running the script:
-------------------
To run the script, simply execute it in a Python environment. You will be prompted to enter commands for the drone.
You can enter 't' to send a command to the drone or 'q' to quit the script. If you choose to send a command,
you will be asked to enter the number of seconds for the trigger time. You can enter '0' to cancel the command.

License:
--------
This script is open-source and available to use and modify as per the terms of the license agreement.

Disclaimer:
-----------
The script is provided as-is, and the authors and contributors are not responsible for any damage or loss resulting from its use.
Always ensure that you comply with all local laws and regulations when operating drones.

"""

"""
Author: Alireza Ghaderi
Email: p30planets@gmail.com
GitHub: alireza787b
Repository: github.com/alireza787b/mavsdk_drone_show
Date: June 2023
---------------------------------------------------------------------------

Ground Control Station (GCS) Script for Drone Telemetry and Command Control
---------------------------------------------------------------------------

This script is designed to function as a Ground Control Station (GCS) in a drone network, providing functionality for receiving telemetry data from drones and
sending commands to them. The script communicates with the drones over User Datagram Protocol (UDP), and it can be easily configured and expanded to 
handle multiple drones simultaneously.

Setup and Configuration:
------------------------
The script is set up to read its configuration from a .csv file named 'config.csv' which should be located in the same directory as the script. The columns
in 'config.csv' should be as follows: hw_id, pos_id, x, y, ip, mavlink_port, debug_port, gcs_ip.

Each row in 'config.csv' corresponds to a drone. The 'hw_id' column indicates the hardware ID of the drone, the 'pos_id' gives its position ID, 'x' and 'y'
provide coordinates, 'ip' specifies the drone's IP address, 'mavlink_port' and 'debug_port' provide the ports for MAVLink communication and debug information,
and 'gcs_ip' specifies the IP address of the GCS.

The script is designed to work with a specific drone determined by the hardware ID specified in a file named 'i.hwID', where 'i' is the hardware ID of the drone.
This file should also be located in the same directory as the script.

Sim Mode:
---------
The script includes a 'sim_mode' boolean variable that allows the user to switch between simulation mode and real-world mode. When 'sim_mode' is set to True,
the script is in simulation mode, and the IP address of the coordinator (essentially the drone control node) should be manually defined in the code. 
If 'sim_mode' is False, the script uses the IP address from 'config.csv' for the drone with the hardware ID matching that in 'i.hwID'.

Communication Protocol:
-----------------------
The script communicates with the drone over UDP using binary packets. For telemetry data, these packets have the following structure:

- Header (1 byte): A constant value of 77. 
- HW_ID (1 byte): The hardware ID of the drone.
- Pos_ID (1 byte): The position ID of the drone.
- State (1 byte): The current state of the drone.
- Trigger Time (4 bytes): The Unix timestamp when the data was sent.
- Terminator (1 byte): A constant value of 88.

For commands, the packets have a similar structure, but the header value is 55 and the terminator value is 66.

Each part of the packet is packed into a binary format using the struct.pack method from Python's 'struct' library.
The '=' character ensures that the bytes are packed in standard size, 'B' specifies an unsigned char (1 byte), and 'I' specifies an unsigned int (4 bytes).

Example:
--------
For example, a command packet could look like this in binary:

Header = 55 (in binary: 00110111)
HW_ID = 3 (in binary: 00000011)
Pos_ID = 3 (in binary: 00000011)
State = 1 (in binary: 00000001)
Trigger Time = 1687840743 (in binary: 11001010001100001101101100111111)
Terminator = 66 (in binary: 01000010)

The whole packet in binary would look like this:
00110111 00000011 00000011 00000001 11001010001100001101101100111111 01000010

Please note that the actual binary representation would be a sequence of 8-bit binary numbers.
The above representation is simplified to demonstrate the concept.

Running the script:
-------------------
To run the script, simply execute it in a Python environment. You will be prompted to enter commands for the drone.
You can enter 't' to send a command to the drone or 'q' to quit the script. If you choose to send a command,
you will be asked to enter the number of seconds for the trigger time. You can enter '0' to cancel the command.

License:
--------
This script is open-source and available to use and modify as per the terms of the license agreement.

Disclaimer:
-----------
The script is provided as-is, and the authors and contributors are not responsible for any damage or loss resulting from its use.
Always ensure that you comply with all local laws and regulations when operating drones.

"""

# Imports
import socket
import struct
import threading
import time
import pandas as pd
import os

# Sim Mode
sim_mode = True  # Set this variable to True for simulation mode

# Read the hwID
hw_id_file = [file for file in os.listdir() if file.endswith('.hwID')][0]  # Assuming there's only one such file
hw_id = int(hw_id_file.split('.')[0])  # Extract the hw_id

# Read the config file
config_df = pd.read_csv('config.csv')

# Find the drone row
drone_config = config_df.loc[config_df['hw_id'] == hw_id]

# Extract variables
if sim_mode:
    # Define the coordinator IP manually for the simulation mode
    coordinator_ip = '172.22.141.34'  # Insert the WSL IP here
else:
    coordinator_ip = drone_config['ip'].values[0]  # If not in sim mode, use the IP from config.csv
debug_port = int(drone_config['debug_port'].values[0])  # Debug port
gcs_ip = drone_config['gcs_ip'].values[0]  # GCS IP

# Socket for communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((gcs_ip, debug_port))

# This flag controls whether telemetry is printed to the screen
print_telemetry = True

# This flag indicates if the telemetry thread should keep running
keep_running = True


# Function to send commands
def send_command(n):
    # Prepare the command data
    header = 55
    hw_id = 1
    pos_id = 1
    state = 1
    trigger_time = int(time.time()) + n
    terminator = 66

    # Encode the data
    data = struct.pack('=B B B B I B', header, hw_id, pos_id, state, trigger_time, terminator)

    # Send the command data
    sock.sendto(data, (coordinator_ip, debug_port))
    print(f"Sent command: Header={header}, HW_ID={hw_id}, Pos_ID={pos_id}, State={state}, Trigger Time={trigger_time}, Terminator={terminator}")



# Function to handle telemetry
def handle_telemetry():
    global print_telemetry
    global keep_running
    while keep_running:
        # Receive telemetry data
        data, addr = sock.recvfrom(1024)
        
        # Ensure we received a correctly sized packet
        if len(data) == 9:
            # Decode the data
            header, hw_id, pos_id, state, trigger_time, terminator = struct.unpack('=BBBBIB', data)
            
            # Check if header and terminator are as expected
            if header == 77 and terminator == 88:
                # Print the received and decoded data if the flag is set
                if print_telemetry:
                    print(f"Received telemetry: Header={header}, HW_ID={hw_id}, Pos_ID={pos_id}, State={state}, Trigger Time={trigger_time}, Terminator={terminator}")
            else:
                print("Invalid header or terminator received in telemetry data.")
        else:
            print(f"Received packet of incorrect size. Expected 9, got {len(data)}.")

# Start the telemetry thread
telemetry_thread = threading.Thread(target=handle_telemetry)
telemetry_thread.start()

try:
    # Main loop for command input
    while True:
        command = input("\n Enter 't' to send a command, 'q' to quit: \n")
        if command.lower() == 'q':
            break
        elif command.lower() == 't':
            print_telemetry = False
            n = input("\n Enter the number of seconds for the trigger time (or '0' to cancel): \n")
            if int(n) == 0:
                print_telemetry = True
                continue
            send_command(int(n))
            print_telemetry = True
except ValueError:
    print("Invalid input. Please enter a valid command.")
except KeyboardInterrupt:
    pass
finally:
    # When KeyboardInterrupt happens or an error occurs, stop the telemetry thread
    keep_running = False
    telemetry_thread.join()

print("Exiting the application...")