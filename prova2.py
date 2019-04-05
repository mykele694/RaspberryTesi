import RPi.GPIO as GPIO
from builtins import input

GPIO.setmode(GPIO.BCM) #Numerazione BCM
GPIO.setwarnings(False)

from driver import *
from distance_sensor import Sensor
import time

guardaAvanti = Sensor(trigPin=19, echoPin=5)
guardaSx = Sensor(trigPin=16, echoPin=12)
guardaDx = Sensor(trigPin=13, echoPin=6)

motoreDx = Driver(23,10, 0)
motoreSx = Driver(24,12, 1)  
safeDist = 20

def vaiDritto(vel): 
	velDx = int(1*vel*4095)
	velSx = int(1*vel*4095)
	motoreDx.update(velDx,1)
	motoreSx.update(velSx,1)
	
def vaiIndietro(vel): 
	velDx = int(-1*vel*4095)
	velSx = int(-1*vel*4095)
	motoreDx.update(velDx,1)
	motoreSx.update(velSx,1)
	
def fermati():
	velDx = int(1*0*4095)
	velSx = int(1*0*4095)
	motoreDx.update(velDx,1)
	motoreSx.update(velSx,1)
	
def ruotaDx(vel):
	velDx = int(-1*vel*4095)
	velSx = int(1*vel*4095)
	motoreDx.update(velDx,1)
	motoreSx.update(velSx,1)
	
def ruotaSx(vel):
	velDx = int(1*vel*4095)
	velSx = int(-1*vel*4095)
	motoreDx.update(velDx,1)
	motoreSx.update(velSx,1)


#while True:
#	print(guardaAvanti.distance())



"""
while True:
	fermati()
	if round(guardaAvanti.distance(),2)>safeDist:
		while round(guardaAvanti.distance(),2) >safeDist:
			#vaiDritto(0.2)
			ruotaSx(0.2)
	else:
		fermati()
		time.sleep(0.1)
		start = time.time()
		if round(guardaDx.distance(),2) < safeDist:
			while ((round(guardaDx.distance(),2)<safeDist) or time.time()-start<3.5):
#				if round(guardaDx.distance(),2) < safeDist:
#					start = time.time()
				#ruotaSx(0.2)
				vaiDritto(0.2)
				time.sleep(0.1)
		elif round(guardaSx.distance(),2) < safeDist:
			while ((round(guardaSx.distance(),2)<safeDist) or time.time()-start<3.5):
#				if round(guardaSx.distance(),2) < safeDist:
#					start = time.time()
				#ruotaDx(0.2)
				vaiIndietro(0.2)
				time.sleep(0.1)	


while True:
	start = time.time()	
	while time.time()-start <3:
		ruotaSx(0.2) #avanti
	start = time.time()
	while time.time()-start <3:
		vaiDritto(0.2)	#sinistra
	start = time.time()
	while time.time()-start <3:
		#ruotaDx(0.2)
		vaiIndietro(0.2)	#destra
		
"""
