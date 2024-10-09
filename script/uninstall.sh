#!/bin/bash

systemctl stop ev3-wfc

systemctl disable ev3-wfc

rm /etc/systed/system/ev3-wfc.service

systemctl daemon-reload
