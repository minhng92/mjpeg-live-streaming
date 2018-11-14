#!/bin/bash

# Note: run with root permission
# Created symlink from /etc/systemd/system/multi-user.target.wants/ivas.service to /etc/systemd/system/ivas.service.
chmod +x src/main.py
cp mjpeg.service /etc/systemd/system
systemctl daemon-reload
systemctl enable mjpeg.service
systemctl start mjpeg
systemctl status mjpeg
