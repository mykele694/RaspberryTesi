# Import the ADS1x15 module.
import Adafruit_ADS1x15
import math
import time
import sys
from threading import Thread
GAIN = 2/3


class Joystick(Thread):
    def __init__(self, drive_min=-13333,drive_max=13333,motor_min=-100,motor_max=100):
        Thread.__init__(self)
        self.setDaemon(True)
        self.values = [0]*2
        self.drive_min = drive_min
        self.drive_max = drive_max
        self.motor_min = motor_min
        self.motor_max = motor_max
        # Create an ADS1115 ADC (16-bit) instance.
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.map_values = [0] * 2
        self.values = [0]*4
        self.off_x=0
        self.off_y=0
        #self.calibration()

    def calcolo_bounds_deathzone(self):
        perc = 5 #percentuale zona morta
        self.upper_x = (2048 + self.off_x) + (2048 + self.off_x)*perc/100
        self.lower_x = (2048 + self.off_x) - (2048 + self.off_x)*perc/100
        self.upper_y = (2048 + self.off_y) + (2048 + self.off_y)*perc/100
        self.lower_y = (2048 + self.off_y) - (2048 + self.off_y)*perc/100
        return self.upper_x, self.lower_x, self.upper_y, self.lower_y

    def calibration(self):
        x_cal=0
        y_cal=0
        n=0
        start=time.time()
        while(time.time()-start<5):
            self.lettura_ADC()
            self.map()
            x_cal+=self.map_values[0]-2048
            y_cal+=self.map_values[1]-2048
            n+=1
        self.off_x=round(x_cal/n,0)
        self.off_y=round(y_cal/n,0)
        print("FINE CALIBRAZIONE")
        print(self.off_x)
        print(self.off_y)
        time.sleep(2)

    def deathzone(self,x,y):
        x_zone=0
        y_zone=0
        if self.lower_x< x <self.upper_x:
            x_zone=2048
        else:
            x_zone=x

        if self.lower_y< y <self.upper_y:
            y_zone=2048
        else: 
            y_zone=y
        return x_zone, y_zone

    def read_raw(self):
        while True:
            for i in range(4):
                self.values[i] = self.adc.read_adc(i, gain=GAIN)
            print('| {:>6} | {:>6} | {:>6} | {:>6} |'.format(*self.values))

    def lettura_ADC(self): # funzione di lettura dei valori in Volt dall'ADC
        for i in range(2):
            self.values[i] = self.adc.read_adc(i, gain=GAIN)
        return self.values[0],self.values[1]
        

    def map2(self,x,in_min=-13333,in_max=13333,out_min=0,out_max=4095):
        return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min

    def map(self):  # mappatura dei valori in volt da una scala ad un'altra 
        for i in range(2):
            #self.map_values[i] = self.values[i]
            self.map_values[i] = round((self.values[i]-self.drive_min)*(self.motor_max-self.motor_min)/(self.drive_max - self.drive_min) + self.motor_min,2)          
        #print('| {0:>6} | {1:>6} |'.format(self.map_values[0]-self.off_x,self.map_values[1]-self.off_y))

    def run(self):
        a,b = self.lettura_ADC()
        a,b = self.diamond(a,b)
        return int(a),int(b)

    def diamond(self, x, y): #dal joystick alle diamond coordinate
        #print("Ingresso: {}\t{}".format(x,y))
        x-=13333
        y-=13333
        #calcolo l'ipotenusa
        z = math.sqrt(x*x+y*y)
        #print("Z = {}".format(z))
        #calcolo l'angolo in radianti
        try:
            rad = math.acos(abs(x)/z)
        except ZeroDivisionError:
            rad = 0
        #if (math.isnan(rad)): #per NaN valori (Not a Number)
        #    rad = 0

        #calcolo l'angolo in gradi
        angle = rad*180/math.pi
        #print("ANGOLO : {}".format(angle))

        #ora l' angolo indica la misura della rotazione; lungo una linea retta, il coefficiente di rotazione e' lo stesso che si applica per angoli tra 0 e 90:con angolo
        #pari a 0, il coefficiente e' apri a -1, con angolo pari a 45, il coefficiente e' 0 e con angolo di 90, il coefficiente e' pari a 1.
        tcoeff = -1+(angle/90)*2
        Vi = tcoeff*abs(abs(y) - abs(x))
        #Vi = round(turn*100)/100
        
        #il max di y o x e' il movimento
        Ve = max(abs(y),abs(x))
        #print("VE: {}\tVi: {}".format(Ve,Vi))
        #primo e terzo quadrante
        if (x >= 0 and y >= 0) or (x < 0 and y < 0):
            rawLeft = Ve
            rawRight = Vi
        else:
            rawRight = Ve
            rawLeft = Vi
        
        #Polarita' inversa
        if y < 0:
            rawLeft = 0 - rawLeft
            rawRight = 0- rawRight
        #print("Before map: {}\t{}".format(rawLeft,rawRight))
        #Mappo i valori in un rang definito
        LeftMotorOutput = round(self.map2(rawLeft),0)
        RightMotorOutput = round(self.map2(rawRight),0)
        #print("{}\t{}".format(LeftMotorOutput, RightMotorOutput))
        return LeftMotorOutput, RightMotorOutput

if __name__ == '__main__':
    joy=Joystick()
    if len(sys.argv) > 1:
        if str(sys.argv[1] == 'RAW'):
            joy.read_raw()
    else:
        print(len(sys.argv))
        joy.run()