import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

TRIG2 = 26
ECHO2 = 19

volume = 0
midi = 60

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)

GPIO.output(TRIG2, False)
GPIO.output(TRIG, False)

print("sensor settle..")

time.sleep(2)

def sendToPd(message=''):
	print(message)
	os.system("echo '" + message + "' | pdsend 3000 ")

def distance(trig, echo):
	GPIO.output(trig, True)
	time.sleep(0.00001)
	GPIO.output(trig, False)

	while GPIO.input(echo)==0:
		pulse_start = time.time()

	while GPIO.input(echo)==1:
		pulse_end = time.time()

	try:
		pulse_duration = pulse_end - pulse_start
	except:
		return 1000

	distance = pulse_duration * 17150

	distance = round(distance, 2)

	return distance

def get_vol(dist):
	min = 4
	max = 15

	if (dist > max):
		dist = max
	if (dist < min):
		dist = min

	vol = (dist - min)/(max - min)

	return vol


def get_MIDI(dist=20):
	min = 3
	max = 25

	note_range = 12
	dist_range = (max - min)

	offset = (dist * note_range)/dist_range
	midi = 80 - offset
	return(midi)

try:
	while True:
		time.sleep(0.1)

		dist = distance(TRIG, ECHO)
		volDist = distance(TRIG2, ECHO2)

		if (dist < 100):
			midi = get_MIDI(dist)
		if (volDist < 100):
			volume = get_vol(volDist)

		if (volDist >= 100 and dist >= 100):
			continue

		sendToPd(str(midi) + ' ' + str(volume) + ';\n')

except KeyboardInterrupt:
	print("cleaning up")
	GPIO.cleanup()
