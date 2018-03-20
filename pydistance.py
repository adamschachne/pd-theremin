from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo = 5, trigger = 4)

while True:
	print(sensor.distance)
	sleep(1)

