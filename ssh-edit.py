from pwn import *
import sys
import subprocess
from pynput.keyboard import Key, Listener, KeyCode

# usage ssh-edit user@ip:/path/to/file/to/edit
# updates remote file on ctrl+s

ssh_remote_file_path = sys.argv[1]

try:
    gui_editor = os.environ['GUI_EDITOR']
except KeyError:
    gui_editor = "gedit"

temp_file = "/tmp/ssh-edit"


def update_remote_file():
    io = process(["scp", temp_file, ssh_remote_file_path])
    io.recvall()
    log.info("edited file updated on remote machine")


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


log.info(temp_file)


io = process(["scp", ssh_remote_file_path, temp_file])
io.recvall()

log.info("downloaded file")

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

log.info("file edited")



