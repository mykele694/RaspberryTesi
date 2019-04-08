from threading import Thread
from driver import *
import acq_camera
import RPi.GPIO as GPIO
from builtins import input
from pwm import *
GPIO.setmode(GPIO.BCM) #Numerazione BCM
GPIO.setwarnings(False)
import math

class Robot(Thread):
    def __init__(self):
        Thread.__init__(self)
        Thread.setDaemon = True

        self.is_tracking = False
        self.angle = None
        self.motoreDx = Driver(23,10, 0)
        self.motoreSx = Driver(24,12, 1)
        self.safe=20
        self.distance=None

    def run(self):
        while True:
            if self.CAM.status:
                self.set_tracking()
                if self.is_tracking == True:
                    time.sleep(0.2)
                    self.MOVE()
                    #muoviti
                    pass
                else:
                    self.fermati()
                    #fermo
                    pass
            else:
                print("arresto robot")
                break
    
    def muovi_angle(self):
        angle_rad = math.radians(self.angle)
        angle_rad += math.pi/4
        velDx = -1*int(math.sin(angle_rad)*4095)
        velSx = -1*int(math.cos(angle_rad)*4095)
        self.motoreDx.update(velDx,1)
        self.motoreSx.update(velSx,1)


    def fermati(self):
        velDx = int(1*0*4095)
        velSx = int(1*0*4095)
        self.motoreDx.update(velDx,1)
        self.motoreSx.update(velSx,1)


    def MOVE(self):
        while(self.is_tracking):
            self.check()
            print("DISTANZA: ",self.distance)
            if self.distance>self.safe:
                self.muovi_angle()
        
            elif self.distance<self.safe:
                self.fermati()
                time.sleep(0.1)

    def set_angle(self):
        self.angle=self.CAM.ang

    def set_distance(self):
        self.distance=self.CAM.distance
        #print("distance: ",self.distance)

    def set_obj_cam(self,cam):
        self.CAM = cam

    def set_tracking(self):
        if self.CAM.qr_presence or self.CAM.track_presence:
            self.is_tracking=True

        else:
            self.is_tracking=False

    def check(self):
        self.set_angle()
        self.set_distance()
        self.set_tracking()
