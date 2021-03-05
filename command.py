import socket
import msgpack
import time
import pygame
import sys

#if len(sys.argv) > 1:
#    #UDP_IP = "192.168.50.175"
#else:
#    UDP_IP = '127.0.0.1'

UDP_IP = "192.168.50.243"
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
        drivel_value = 0.0,
        driver_value = 0.0, 
        drivel_direction='forward', 
        driver_direction='forward',
        )
s.sendto(msgpack.dumps(msg), (UDP_IP, UDP_PORT))

THL = 1
THR = 4


#handle joystick reset -> wait for first button from user
#while joystick.get_axis(TH) < 0.5:
#    pygame.event.pump()
#    time.sleep(0.1)

while True:
    time.sleep(1/20)
    pygame.event.pump()

    dl = abs(joystick.get_axis(THL))
    msg['drivel_value'] = 0 if dl < 0.1 else dl
    msg['drivel_direction'] = 'forward' if joystick.get_axis(THL) > 0 else 'b'

    dr = abs(joystick.get_axis(THR))
    msg['driver_value'] = 0 if dr < 0.1 else dr
    msg['driver_direction'] = 'forward' if joystick.get_axis(THR) > 0 else 'b'

    s.sendto(msgpack.dumps(msg), (UDP_IP, UDP_PORT))

    print(joystick.get_axis(0), joystick.get_axis(1), joystick.get_axis(2), joystick.get_axis(3), joystick.get_axis(4), joystick.get_axis(5))

    #for i in range(joystick.get_numbuttons()):
    #    print(joystick.get_button(i), end =' ')
    #print('')
