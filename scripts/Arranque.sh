#!/bin/bash
sudo service mongod start
cd /home/ubuntu/Lab-Compu-18
. flask/bin/activate
sudo python app.py
