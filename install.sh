#!/bin/bash
sudo apt install -y python3-pip
sudo apt install -y python3-tk
sudo apt install -y libffi-dev
sudo pip install --upgrade pip
export CRYPTOGRAPHY_DONT_BUILD_RUST=1
# sudo python3 -m pip install -r ./requirements.txt
# sudo pip3 install -r ./requirements.txt
# https://stackoverflow.com/questions/49324802/pip-always-fails-ssl-verification
sudo python3 -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt

echo "creating symlink in path (/usr/local/bin)"
chmod a+x "./ssh-edit.py"
sudo ln -sf "$(pwd)/ssh-edit.py" "/usr/local/bin/ssh-edit"