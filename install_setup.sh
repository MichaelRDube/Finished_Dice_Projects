#!/bin/bash

# Update package list
sudo apt update

# Install Python, pip, and venv (if not already installed)
if ! command -v python3 &>/dev/null; then
    echo "Python not found. Installing Python..."
    sudo apt install -y python3 python3-pip
else
    echo "Python is already installed."
fi

# Ensure python3-venv is installed for creating virtual environments
echo "Installing python3-venv if not already installed..."
sudo apt install -y python3-venv

# Upgrade pip to the latest version
echo "Upgrading pip to the latest version..."
pip3 install --upgrade pip

# Install system libraries
echo "Installing required system libraries..."
sudo apt install -y python3-tk libsqlite3-dev v4l-utils python3-opencv

# Create and activate a virtual environment
echo "Creating a virtual environment..."
python3 -m venv myenv

echo "Activating the virtual environment..."
source myenv/bin/activate

# Install Python libraries within the virtual environment
echo "Installing and upgrading Python libraries within the virtual environment..."
pip install --upgrade pillow ultralytics pyserial

# Configure camera settings (optional)
echo "Configuring camera settings..."
v4l2-ctl -d /dev/video0 --set-ctrl=brightness=128
v4l2-ctl -d /dev/video0 --set-ctrl=contrast=150
v4l2-ctl -d /dev/video0 --set-ctrl=saturation=60
v4l2-ctl -d /dev/video0 --set-ctrl=white_balance_automatic=0
v4l2-ctl -d /dev/video0 --set-ctrl=gain=0
v4l2-ctl -d /dev/video0 --set-ctrl=power_line_frequency=2
v4l2-ctl -d /dev/video0 --set-ctrl=white_balance_temperature=3900
v4l2-ctl -d /dev/video0 --set-ctrl=sharpness=128
v4l2-ctl -d /dev/video0 --set-ctrl=backlight_compensation=1
v4l2-ctl -d /dev/video0 --set-ctrl=auto_exposure=3
v4l2-ctl -d /dev/video0 --set-ctrl=exposure_dynamic_framerate=0
v4l2-ctl -d /dev/video0 --set-ctrl=pan_absolute=0
v4l2-ctl -d /dev/video0 --set-ctrl=tilt_absolute=0
v4l2-ctl -d /dev/video0 --set-ctrl=focus_absolute=183
v4l2-ctl -d /dev/video0 --set-ctrl=focus_automatic_continuous=0
v4l2-ctl -d /dev/video0 --set-ctrl=zoom_absolute=100

echo "Camera configuration complete!"

# Add user to dialout group for serial port access
echo "Granting user permissions to access serial ports..."
sudo usermod -a -G dialout $USER
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Please restart computer for the dialout group changes to take effect."

