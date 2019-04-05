# classe con la prima funzione che genera pwm
# seconda funzione: deve pilotare i driver quindi in input ho il segnale pwm della funzione di prima e questo lo devo mandare ad m1 (motore 1)

from pwm import * #dalla libreria pwm importa tutto (*)
import Adafruit_PCA9685
import time
import RPi.GPIO as gpio 

"""gpio.setmode(gpio.BCM) #Numerazione BCM
gpio.setwarnings(False) """

class Driver:
    def __init__(self, enablePin, pinPWM, chMotor):
        self.driver = PwmClass(channel=chMotor)
        self.speed = 0
        self.enablePin = enablePin
        self.pinPWM = pinPWM
        self.chMotor = chMotor
        self.verso = gpio.HIGH
        gpio.setup(self.enablePin, gpio.OUT) #GPIO 0
        gpio.setup(self.pinPWM, gpio.OUT) #GPIO 1
        print("Driver %s created" % self.chMotor)

    def update(self, power, verso=None):
        if power<0:
            power = power * -1
            verso = -1

        if verso == None:
            verso = self.verso
        elif verso == -1:
            #print("negativo")
            if self.verso == gpio.HIGH:
                verso = gpio.LOW
            else:
                verso = gpio.HIGH
        gpio.output(self.enablePin, verso) #Verso = gpio.HIGH or gpio.LOW
        self.driver.setting_pwm(self.chMotor,0, power) #power = 0:4095

    def emergency(self):
        self.driver.setting_pwm(self.chMotor,0,0)
        print("Motor {} arrested".format(self.chMotor))

if __name__ == '__main__':
    driver_test = Driver(4,17, 0)
    delay = 0.0
    try:
        for i in range(4096):
            print(i)
            driver_test.update(i)
            time.sleep(delay)
        for i in range(4095,0,-1):
            print(i)
            driver_test.update(i)
            time.sleep(delay)

        driver_test.update(0,gpio.LOW)
        for i in range(4096):
            print(i)
            driver_test.update(i)
            time.sleep(delay)
        for i in range(4095,0,-1):
            print(i)
            driver_test.update(i)
            time.sleep(delay)
    except KeyboardInterrupt:
        driver_test.emergency()