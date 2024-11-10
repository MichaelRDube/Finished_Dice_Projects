#!/bin/bash

# Update package list
sudo apt update

# Install Python and pip (if not already installed)
if ! command -v python3 &>/dev/null; then
    echo "Python not found. Installing Python..."
    sudo apt install -y python3 python3-pip
else
    echo "Python is already installed."
fi

# Upgrade pip to the latest version
echo "Upgrading pip to the latest version..."
pip3 install --upgrade pip

# Install system libraries only with apt where necessary
echo "Installing required system libraries..."
sudo apt install -y python3-tk libsqlite3-dev v4l-utils

# Install required Python libraries with pip
echo "Installing and upgrading Python libraries with pip..."
pip3 install --upgrade pillow ultralytics opencv-python opencv-python-headless

# Configure camera to match training conditions
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

