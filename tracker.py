from threading import Thread
import qr
import cv2
import acq_camera
#from main import *
import numpy as np
import time

class Tracker_class(Thread):
    def __init__(self):
        Thread.__init__(self)
        Thread.setDaemon = True
        self.found=False
        self.box=None
        self.frame=None
        self.tracker=None
        self.color=False
        self.is_tracking=False
        # Come tutte
    def set_obj(self, rob):
        self.robot = rob
    
    def set_CAM_obj(self, cam):
        self.CAM = cam

    def set_QR_obj(self, qr):
        self.QR = qr

    def run(self):
        time.sleep(2)
        while True:
            start=time.time()
            if self.CAM.status:
                # do something
                self.frame = self.CAM.get_frame()  
                #print(self.frame)             
                self.track_set()
                if not self.found:
                   self.set_mask()
                    self.track_color_set()

                if self.is_tracking:  
                    self.get_center()

            else:
                print("arresto tracker")
                break
            #print("Time Tracker:",(time.time()-start))
    def set_box(self):
        self.box=self.QR.QRdetect()

    def set_rect_track(self):
        p1 = (int(self.box[0]), int(self.box[1]))
        p2 = (int(self.box[0] + self.box[2]), int(self.box[1] + self.box[3]))
        self.CAM.track_presence = True
        self.CAM.set_track_rect(p1,p2)
        print("width",int(self.box[2]))

    def track_set(self):
        if self.found:
            if self.CAM.qr_presence:
                self.set_box()
                ret=self.tracker.init(self.frame,self.box)
            else:
                ret, self.box=self.tracker.update(self.frame)
            if not ret:
                self.found=False
                self.CAM.track_presence=False
                self.is_tracking = False
            else:
                self.found=True
                self.CAM.track_presence=True
                self.set_rect_track()
                self.is_tracking = True
        if not self.found:            
            if self.CAM.qr_presence:
                self.set_box()
                self.tracker=cv2.TrackerMedianFlow_create()
                ret=self.tracker.init(self.frame,self.box)
                if ret:
                    self.found=True
                    self.is_tracking = True
    def track_color_set(self):
        i, conts, h = cv2.findContours(self.yellow,cv2.RETR_EXTERNAL,cv2.CHAIN_$
        if len(conts)!=0:
            c = max(conts, key=cv2.contourArea)
            self.box=cv2.boundingRect(c)
            self.CAM.track_presence=True
            self.set_rect_track()
            self.is_tracking=True

        else:
            self.is_tracking=False
            self.box=None
            self.CAM.track_presence=False
    def get_center(self):
        # returning x
        return int((self.box[0]+self.box[2]/2))
        #self.robot.target_x=(self.box[0]+self.box[2]/2)
        #self.robot.target_y=(self.box[1]+self.box[3]/2)

    def set_mask(self):
        #self.frame = np.array(self.frame, dtype=np.uint8)
        lower = np.array([0, 140, 140])  #YELLOW  
        upper = np.array([100, 255, 255])
        mask = cv2.inRange(self.frame, lower, upper)
        kernelOpen=np.ones((2,2))
        kernelClose=np.ones((80,80))
        maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
        maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
        self.yellow = maskClose

if __name__ == '__main__':
    TRACK_OBJ = Tracker_class()
    TRACK_OBJ.start()


