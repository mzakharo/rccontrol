from gpiozero import PWMLED, LED
from time import sleep
import socket
import json

drive = PWMLED(13)
turn = PWMLED(6)


motor1 = LED(4)
motor2 = LED(17)


motor3 = LED(27)
motor4 = LED(22)



def forward():
    motor1.off()
    motor2.on()

def reverse():
    motor1.on()
    motor2.off()

def right():
    motor3.on()
    motor4.off()

def left():
    motor3.off()
    motor4.on()

turn.value = 0.5

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
s.settimeout(1)
s.bind(('', UDP_PORT))
print('recv')
while True:
    try:
        pkt = s.recv(1024)
    except socket.timeout:
        drive.value = 0
        turn.value = 0
        continue
    d = json.loads(pkt)
    drive.value = d['drive_value']
    if d['drive_direction'] == 'forward':
        forward()
    else:
        reverse()
    turn.value = d['turn_value']
    if d['turn_direction'] == 'right':
        right()
    else:
        left()
