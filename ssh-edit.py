from pwn import *
import sys
import subprocess
from pynput.keyboard import Key, Listener

# usage [-p password | -k keyfile] ssh-edit user ip port /path/to/file/to/edit
# updates remote file on ctrl+s
# password and key auth cannot be used together

password = None
user = None
ip = None
port = None
ssh_remote_file_path = None
file_to_edit = None
key_file = None

first_arg = sys.argv[1]

index = 1
if first_arg == "-p":
    index += 1
    password = sys.argv[index]
    index += 1
elif first_arg == "-k":
    index += 1
    key_file = sys.argv[index]
    index += 1


user = sys.argv[index]
index += 1

ip = sys.argv[index]
index += 1

port = int(sys.argv[index])
index += 1

file_to_edit = sys.argv[index]
index += 1

try:
    gui_editor = os.environ['GUI_EDITOR']
except KeyError:
    gui_editor = "gedit"

temp_file = "/tmp/ssh-edit"


def create_session():
    if password:
        s = ssh(user, ip, port, password)
    else:
        s = ssh(user, ip, port, keyfile=key_file)
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


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

#time.sleep(1)
#while True:
#    time.sleep(0.3)
#    io = process("ps aux | grep " + gui_editor + " | grep -v grep", shell=True)
#    proc_running = io.recvall()
#    if proc_running == b"":
#        io.close()
#        break
#    io.close()




