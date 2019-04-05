import sys
import imutils
RASPBERRY = True
#if len(sys.argv) > 1: RASPBERRY = True
if RASPBERRY: from imutils.video.pivideostream import PiVideoStream
import time
import cv2
from threading import Thread
from pwm import PwmClass
 
class VideoCam(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon = True
        self.status = True
        self.frame = None
        self.qr_presence = False
        self.track_presence=False
        self.setpoint=None
        self.senso=True
        self.ang=0
        self.PWM=PwmClass(60,15,0,0,1)
        self.X=None
        self.error=None
        if RASPBERRY:
            self.cam = PiVideoStream(resolution=(640,480)).start()            
            self.width=640
        else:
            self.cam = cv2.VideoCapture(0)
            self.get_dim()
           
    def run(self):
        self.set_setpoint()
        time.sleep(1)

        while True:
            start=time.time()
            try:
                if RASPBERRY:
                    self.frame = self.cam.read()
                else:
                    self.status, self.frame = self.cam.read()
            except TypeError:
                pass
            else:
                # Disegna rettangolo QR se esiste
                if not (self.qr_presence or self.track_presence):
                    self.move_cam()
                    print("RICERCA")
                else:
                    self.get_rect()
                    self.get_error()
                    self.follow_target()

                #cv2.imshow('nome',self.frame)

                if (cv2.waitKey(1) & 0xFF==ord('q')):       #Q per chiuedere
                    break
            #print("Time ACQ_CAM:",(time.time()-start))
        self.status = False
        if RASPBERRY:
            self.cam.stop()
        else:
            self.cam.release()
        cv2.destroyAllWindows()
        print("Arresto CAMERA")        

    def set_qr_rect(self, p1, p2):
        self.qr_p1 = p1
        self.qr_p2 = p2

    def set_track_rect(self,p1,p2):
        self.track_p1=p1
        self.track_p2=p2

    def get_rect(self):
        if self.qr_presence:
           cv2.rectangle(self.frame, self.qr_p1, self.qr_p2, (255,0,0), 2, 1)
           self.X=int((self.qr_p2[0]-self.qr_p1[0])/2+self.qr_p1[0])
           cv2.circle(self.frame,(self.X,int((self.qr_p2[1]-self.qr_p1[1])/2+se$
        elif self.track_presence:
            cv2.rectangle(self.frame, self.track_p1, self.track_p2, (0,255,0), $
            self.X=int((self.track_p2[0]-self.track_p1[0])/2+self.track_p1[0])
            cv2.circle(self.frame,(self.X,int((self.track_p2[1]-self.track_p1[1$
    def get_frame(self):
        return self.frame
    
    def get_dim(self):
        height=self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width=self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)

    def set_setpoint(self):
        self.setpoint=self.width/2
    def move_cam(self):
        #print(self.ang)
        time.sleep(0.1)
        if self.senso==True:
            self.ang=self.ang+1
        else:
            self.ang=self.ang-1
        #print(self.ang)
        self.PWM.rotate(self.ang)
        #time.sleep(0.001)
        if self.ang==180:
            self.senso=False
        elif self.ang==0:
            self.senso=True
     def get_error(self):
        if (self.qr_presence or self.track_presence):
            self.error=int(self.setpoint-self.X)
            time.sleep(0.02)
            print("ERRORE",self.error)
        else:
            self.error=None


      def follow_target(self):
            if self.error!=None:
                time.sleep(0.1)
                if self.error>20:
                    print("sx di: ",self.error)
                    self.ang=self.ang+1
                    self.PWM.rotate(self.ang)
                elif self.error<(-20):
                  print("dx di: ",self.error)
                  self.ang=self.ang-1
                  self.PWM.rotate(self.ang)
            else:
                pass
            #self.PWM.rotate(self.ang)
            print("angolo",self.ang)


if __name__ == '__main__':
    CAM = VideoCam()
    CAM.start()




    

                    
