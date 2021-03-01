import socket
import msgpack
import time
import sys
from xbox360controller import Xbox360Controller

if len(sys.argv) > 1:
    UDP_IP = "192.168.50.175"
else:
    UDP_IP = '127.0.0.1'
UDP_PORT = 5005
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
msg = dict(
        drive_value = 0.0,
        turn_value = 0.0, 
        drive_direction='forward', 
        turn_direction='left',
        )
s.sendto(msgpack.dumps(msg), (UDP_IP, UDP_PORT))

controller = Xbox360Controller(0, axis_threshold=0.2)

def get_dv():
    return controller.axis_r.y
def get_tv():
    return controller.axis_l.x
def get_reverse():
    return controller.button_b.is_pressed

#handle joystick reset -> wait for first button from user
while get_dv() < 0.5:
    time.sleep(0.1)

while True:
    time.sleep(1/20)
    dv = (get_dv() + 1) / 2
    msg['drive_value'] = 0 if dv < 0.1 else dv
    msg['drive_direction'] = 'forward' if get_reverse() == 1 else 'b'
    msg['turn_direction'] = 'right' if get_tv() < 0 else 'left'
    tv = abs(get_tv())
    msg['turn_value'] = 0 if tv < 0.1 else tv
    s.sendto(msgpack.dumps(msg), (UDP_IP, UDP_PORT))

    #print(joystick.get_axis(0), joystick.get_axis(1), joystick.get_axis(2), joystick.get_axis(3), joystick.get_axis(4), joystick.get_axis(5))

    #for i in range(joystick.get_numbuttons()):
    #    print(joystick.get_button(i), end =' ')
    #print('')
