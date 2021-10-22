import time
import serial
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
  #connection setup
GPIO.setup(7, GPIO.OUT, initial = GPIO.HIGH)
send = serial.Serial(
     port ='/dev/serial0',
     baudrate = 9600 
     )
ADDR = 1 #Address electrical bracket
#fourth bytes (check pelco-d protocol)
PAN_LEFT  = 4 
PAN_RIGHT = 2
TILT_UP = 8
TILT_DOWN = 16
# Pan Left commands
pan_left__high_speed  = [255,ADDR, 0,PAN_LEFT, 0x3f,     0, 68]
pan_left__stop        = [255,ADDR, 0,PAN_LEFT,    0,     0,  5]
# Pan right commands
pan_right__high_speed = [255,ADDR, 0,PAN_RIGHT, 0x3f,    0, 66]
pan_right__stop       = [255,ADDR, 0,PAN_RIGHT,    0,    0,  3]
# Tilt up commands
tilt_up__high_speed   = [255,ADDR, 0,TILT_UP  ,    0, 0x3f, 72]
tilt_up_stop          = [255,ADDR, 0,TILT_UP  ,    0,    0,  9]
# Tilt down commands
tilt_down__high_speed = [255,ADDR, 0,TILT_DOWN,    0, 0x3f, 80]
tilt_down_stop        = [255,ADDR, 0,TILT_DOWN,    0,    0, 17]
#Pan stop command
pan_stop              = [255,ADDR, 0,        0,    0,    0,  1]
 #stop command
def halt():
  send.write(bytes(pan_stop))
  time.sleep(0.1)
 #Commands (downward movement,upward movement, movement to the left, movement to the right)
def down(timer):
  send.write(bytes(tilt_down__high_speed))
  time.sleep(1)
  send.write(bytes(tilt_down_stop))
 
  send.write(bytes(tilt_down__high_speed))
  time.sleep(timer)
  send.write(bytes(tilt_down_stop))

def up(timer):
  send.write(bytes(tilt_up__high_speed))
  time.sleep(1)
  send.write(bytes(tilt_up_stop))
 
  send.write(bytes(tilt_up__high_speed))
  time.sleep(timer)
  send.write(bytes(tilt_up_stop))

def left(timer):
  send.write(bytes(pan_left__high_speed))
  time.sleep(1)
  send.write(bytes(pan_left__stop))
 
  send.write(bytes(pan_left__high_speed))
  time.sleep(timer)
  send.write(bytes(pan_left__stop))

def right(timer):
  send.write(bytes(pan_right__high_speed))
  time.sleep(1)
  send.write(bytes(pan_right__stop))

  send.write(bytes(pan_right__high_speed))
  time.sleep(timer)
  send.write(bytes(pan_right__stop))
  
try:
 direction = input()
 angle = float(input())
 if direction == 'l':
     timer = angle/10.6
     left(timer)
     halt()
 elif direction == 'r':
     timer = angle/10.6
     right(timer)
     halt()
 elif direction == 'u':
     timer = angle/11.6
     up(timer)
     halt()
 elif direction == 'd':
     timer = angle/11.6
     down(timer)
     halt()
     
finally:
  GPIO.output(7,GPIO.LOW)
  GPIO.cleanup()