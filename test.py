
# Derick DeLeon
# 2014-02
# theremin.py
"""MIDI based theremin using a Raspberry Pi and a sonar HC-SR04 as pitch control"""
"""derickdeleon.com"""

import RPi.GPIO as GPIO
import pygame.midi
import time

# Distance Related Methods

def prepare(GPIO_ECHO, GPIO_TRIGGER):
    """ Initialize the Raspberry Pi GPIO  """
    # Set pins as output and input
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)    # Trigger
    GPIO.setup(GPIO_ECHO,GPIO.IN)        # Echo
    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)
    # Allow module to settle
    time.sleep(0.5)

def get_distance(GPIO_ECHO, GPIO_TRIGGER):
    """ get the distance from the sensor, echo - the input from sensor """
    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    # Taking time
    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()
    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()
    # Calculate pulse length
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300
    # That was the distance there and back so halve the value
    distance = distance / 2
    return distance

def get_note(dist=0):
    """ Compute the note based on the distance measurements, get percentages of each scale and compare """
    # Config
    # you can play with these settings
    minDist = 3    # Distance Scale
    maxDist = 21
    octaves = 1
    minNote = 48   # c4 middle c
    maxNote = minNote + 12*octaves
    # Percentage formula
    fup = (dist - minDist)*(maxNote-minNote)
    fdown = (maxDist - minDist)
    note = minNote + fup/fdown
    """ To-do: calculate trends form historical data to get a smoother transitions """
    return int(note)

# MAIN
GPIO.setwarnings(False)
# The pin number is the actual pin number
GPIO.setmode(GPIO.BCM)
# Set up the GPIO channels
trigger = 17
echo = 27
prepare(echo, trigger)
note = 0
volume = 127
print("getting distance")
print(get_distance(echo, trigger))

GPIO.cleanup()

