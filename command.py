import socket
import msgpack
import time
import pygame
import sys

if len(sys.argv) > 1:
    UDP_IP = "192.168.50.175"
else:
    UDP_IP = '127.0.0.1'
UDP_PORT = 5005
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(joystick.get_name())
print(joystick.get_numaxes())
print(joystick.get_numbuttons())

msg = dict(
        drive_value = 0.0,
        turn_value = 0.0, 
        drive_direction='forward', 
        turn_direction='left',
        )
s.sendto(msgpack.dumps(msg), (UDP_IP, UDP_PORT))

TH = 4

#handle joystick reset -> wait for first button from user
while joystick.get_axis(TH) < 0.5:
    pygame.event.pump()
    time.sleep(0.1)

while True:
    time.sleep(1/20)
    pygame.event.pump()
    dv = (joystick.get_axis(TH) + 1) / 2
    msg['drive_value'] = 0 if dv < 0.1 else dv
    msg['drive_direction'] = 'forward' if joystick.get_button(1) == 1 else 'b'
    msg['turn_direction'] = 'right' if joystick.get_axis(0) < 0 else 'left'
    tv = abs(joystick.get_axis(0))
    msg['turn_value'] = 0 if tv < 0.1 else tv
    s.sendto(msgpack.dumps(msg), (UDP_IP, UDP_PORT))

    #print(joystick.get_axis(0), joystick.get_axis(1), joystick.get_axis(2), joystick.get_axis(3), joystick.get_axis(4), joystick.get_axis(5))

    #for i in range(joystick.get_numbuttons()):
    #    print(joystick.get_button(i), end =' ')
    #print('')
