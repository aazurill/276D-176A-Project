import sys
import RPi.GPIO as GPIO
from gpiozero import MotionSensor, LED
from time import sleep

# SETTING ENVIROMENTAL VARIABLES
pir = MotionSensor(4) # pir sensor connected to GP4 (GPIO 4)
relay = LED(17)       # relay connected to GP17 (GPIO 17)
mode = GPIO.getmode() # get current mode

# change times to open the door dependening on door
time_to_open_door_fully = 10 # time to open door fully
time_to_open_door_half = 5   # time to open door half way
time_to_open_door_quarter = 2.5  # tiem to open door quarter
door_open = False
time_until_close = 0 # time door is taking to close before finishing closing
time_to_open = 0 # time to open the door
GPIO.cleanup()

Forward=26
Backward=20
sleeptime=1

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)

# Function to make robot move forward (open door)
# x is time the motor is on
def forward(x):
  GPIO.output(Forward, GPIO.HIGH)
  print("Moving Forward")
  time.sleep(x)
  GPIO.output(Forward, GPIO.LOW)

#Function to make robot move backward (close door)
# x is time the motor is on
def reverse(x):
  GPIO.output(Backward, GPIO.HIGH)
  print("Moving Backward")
  time.sleep(x)
  GPIO.output(Backward, GPIO.LOW)

# Always keep listening to motion sensor
while True:
  if pir.motion_detected:
    print("Motion detected! - Opening door")
    relay.on() # relay for debugging - notify that motion is detected

    # If door not open, open door
    if not door_open:
      door_open = True
      forward(time_to_open_door_fully)
      # Sleep 10 seconds to wait for person to go through door
      sleep(10)
      # Close door fully
      time_until_close = time.time()

    else: # implication that door is partway open - open door for variable time
      time_to_open = time.time() - time_until_close
      forward(time_to_open_door_fully - time_to_open)
      sleep(10)
      time_until_close = time.time()

    backward(time_to_open_door_fully)
    door_open = False
    relay.off()



