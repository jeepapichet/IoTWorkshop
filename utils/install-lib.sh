#!/bin/bash

#Install modules for IoT Core Lab
pip2 install AWSIoTPythonSDK


#Install for Greegrass Lab
sudo python3 -m pip install -U pip
sudo ln -s $(which pip3) /usr/bin/pip3
python3 -m pip install awsiotsdk