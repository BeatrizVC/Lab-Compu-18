#!/bin/bash
sudo apt-get install ssh
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo apt-get install python-dev
sudo apt-get install python-pip
sudo apt-get install python-virtualenv
sudo apt-get install git
sudo apt-get update
sudo apt-get upgrade
git clone https://github.com/BeatrizVC/Lab-Compu-18
cd Lab-Compu-18
virtualenv flask
. flask/bin/activate
sudo pip install -r requirements.txt
deactivate