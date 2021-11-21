#!/bin/bash
# for pwntools which provides easy ssh api, rustc is needed for cryptography, which is transitive dep of pwntools
sudo apt install -y python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential rustc
sudo apt install -y python3-tk
sudo apt install -y libffi-dev
sudo python3 -m pip install --upgrade pip
# sudo python3 -m pip install -r ./requirements.txt
# sudo pip3 install -r ./requirements.txt
# https://stackoverflow.com/questions/49324802/pip-always-fails-ssl-verification
sudo python3 -m pip install --trusted-host files.pythonhosted.org --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt

echo "creating symlink in path (/usr/local/bin)"
chmod a+x "./ssh-edit.py"
sudo ln -sf "$(pwd)/ssh-edit.py" "/usr/local/bin/ssh-edit"