#!/bin/bash

# Download EV3-WFC server files
download_url=$(curl -sS https://api.github.com/repos/Workflow-Canvas-Ecosystem-Group/LEGO-EV3/releases/latest | grep 'tarball_url' | awk -F'"' '{print $4}')
echo "Download $download_url"

curl -sS -L $download_url > ./ev3-wfc.tar

tar -xf ev3-wfc.tar

# Search "Workflow*" folder and rename to  /home/robot/ev3-wfc
target_folder=$(find . -type d -name 'Workflow*' -print -quit)

if [ -n "$target_folder" ]; then
    mv "$target_folder" /home/robot/ev3-wfc
    echo "Renamed '$target_folder' to 'ev3-wfc'"
else
    echo "No folder starting with 'Workflow' found."
fi

# Create systemd service
cat <<EOT > /etc/systemd/system/ev3-wfc.service
[Unit]
Description=LEGO EV3 Workflow Canvas Server
After=network.target

[Service]
Type=simple
User=robot
ExecStart=/usr/bin/python3 /home/robot/ev3-wfc/src/main.py
WorkingDirectory=/home/robot/ev3-wfc/src
Restart=always

[Install]
WantedBy=multi-user.target
EOT

systemctl daemon-reload

# Enable and start ev3api server service
systemctl enable --now ev3-wfc
