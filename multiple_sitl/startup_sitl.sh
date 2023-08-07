#!/bin/bash

# To run the script with graphics enabled, you would execute the script with the g argument, like this:
# ./startup.sh g

# To run without graphics, you would simply execute the script without any arguments:
# ./startup.sh

# Function to handle SIGINT
cleanup() {
  echo "Received interrupt, terminating background processes..."
  kill $gazebo_pid
  exit 0
}

# Trap SIGINT
trap 'cleanup' INT

# Check for the 'g' argument to enable or disable graphics
if [[ $1 == "g" ]]; then
  GRAPHICS_COMMAND="make px4_sitl gazebo"
  echo "Graphics enabled."
else
  GRAPHICS_COMMAND="HEADLESS=1 make px4_sitl gazebo"
  echo "Graphics disabled."
fi

# Wait for the .hwID file to exist
while [ ! -f ~/mavsdk_drone_show/*.hwID ]
do
  echo "Waiting for hwID file..."
  sleep 1
done

echo "Found .hwID file, continuing with the script."
cd ~/mavsdk_drone_show
echo "Stashing and pulling the latest changes from the repository..."
git stash
git pull

echo "Checking Python Requirements..."
pip install -r requirements.txt

echo "Running the set_sys_id.py script to set the MAV_SYS_ID..."
python3 ~/mavsdk_drone_show/multiple_sitl/set_sys_id.py

echo "Starting the px4_sitl gazebo process in a new terminal window..."
gnome-terminal -- bash -c "cd ~/PX4-Autopilot; hwid_file=\$(find ~/mavsdk_drone_show -name '*.hwID'); hwid=\$(echo \$hwid_file | cut -d'.' -f2); export px4_instance=\$hwid-1; $GRAPHICS_COMMAND; bash" &
gazebo_pid=$!

echo "Starting the coordinator.py process in another new terminal window..."
gnome-terminal -- bash -c "python3 ~/mavsdk_drone_show/coordinator.py; bash" &

echo "Press Ctrl+C to stop the gazebo process."
wait $gazebo_pid
