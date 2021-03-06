from gpiozero import PWMLED, LED
from time import sleep
import socket
import msgpack 

drivel = PWMLED(13)
driver = PWMLED(6)

motor1 = LED(4)
motor2 = LED(17)

motor3 = LED(27)
motor4 = LED(22)



def forwardl():
    motor1.off()
    motor2.on()

def reversel():
    motor1.on()
    motor2.off()

def forwardr():
    motor3.on()
    motor4.off()

def reverser():
    motor3.off()
    motor4.on()

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
        drivel.value = 0
        driver.value = 0
        continue
    d = msgpack.loads(pkt)

    drivel.value = d['drivel_value']
    if d['drivel_direction'] == 'forward':
        forwardl()
    else:
        reversel()

    driver.value = d['driver_value']
    if d['driver_direction'] == 'forward':
        forwardr()
    else:
        reverser()
