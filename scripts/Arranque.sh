#!/bin/bash
sudo service mongod start
export PATH=$PATH:/home/ubuntu
echo $PATH
sudo su - ubuntu -c "nohup ~/ddns.sh > ~/duck.log 2>&1&"
cd /home/ubuntu/Lab-Compu-18
. flask/bin/activate
sudo python app.py