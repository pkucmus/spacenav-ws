import socket
from struct import unpack
from collections import namedtuple


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/var/run/spnav.sock")
Event = namedtuple("Event", "motion X Z Y pitch yaw roll period")


try:
    while True:
        chunk = sock.recv(32)
        print(Event._make(unpack("iiiiiiii", chunk))._asdict())
except KeyboardInterrupt:
    print("bye!")
