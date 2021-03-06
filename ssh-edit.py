#!/usr/bin/env python3
from pwn import *
import sys
import subprocess
from pynput.keyboard import Key, Listener
import uuid
import os

# usage: ssh-edit [-p password | -k keyfile] user ip port /path/to/file/to/edit
# updates remote file on ctrl+s
# password and key auth cannot be used together
# if used with ez-bash run 'backx ssh-edit ...'

password = None
user = None
ip = None
port = None
ssh_remote_file_path = None
file_to_edit = None
key_file = None
index = 1


def load_arg():
    global index
    try:
        v = sys.argv[index]
    except Exception as e:
        print("usage: ssh-edit [-p password | -k keyfile] user ip port /path/to/file/to/edit")
        exit(1)
    if index == 1 and v == "--help":
        print("usage: ssh-edit [-p password | -k keyfile] user ip port /path/to/file/to/edit")
        exit(0)
    index += 1
    return v


first_arg = load_arg()

if first_arg == "-p":
    password = load_arg()
elif first_arg == "-k":
    key_file = load_arg()

user = load_arg()
ip = load_arg()
port = load_arg()
port = int(port)

file_to_edit = load_arg()

try:
    gui_editor = os.environ['GUI_EDITOR']
except KeyError:
    gui_editor = "gedit"

temp_file = "/tmp/ssh-edit-"+file_to_edit.replace("/","\\")
if os.path.exists(temp_file):
  os.remove(temp_file)

def create_session():
    if password:
        s = ssh(user, ip, port, password,cache=False)
    else:
        s = ssh(user, ip, port, keyfile=key_file,cache=False)
    return s


session = create_session()


def update_remote_file():
    log.info("saving remote file")
    session.upload(temp_file, file_to_edit)
    log.info("saved remote file")


def download_remote_file():
    log.info("downloading remote file")
    session.download(file_to_edit, temp_file)
    log.info("downloaded file")


ctrl_down = False


def on_press(key):
    global ctrl_down
    if key == Key.ctrl:
        ctrl_down = True


def on_release(key):
    global ctrl_down
    key_s = '{0}'.format(key)
    if key_s == "\'s\'":
        if ctrl_down:
            update_remote_file()
    if key == Key.ctrl:
        ctrl_down = False


download_remote_file()

subprocess.call([gui_editor, temp_file])
log.info("after process started")


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    # listener.join()
    time.sleep(1)
    while True:
       time.sleep(0.3)
       io = process("ps aux | grep " + gui_editor + " | grep -v grep", shell=True)
       proc_running = io.recvall()
       log.info(f"proc_running {proc_running}")
       if proc_running == b"":
           io.close()
           s.close()
           log.info("editor closed")
           process(["rm",temp_file])
           exit(0)
           break
       io.close()
