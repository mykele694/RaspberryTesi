from threading import Thread
import time
from pyzbar.pyzbar import decode
import cv2

class QR_class(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.setDaemon = True
        self.bbox=None

    def run(self):
        while True:
            if self.CAM.status:
                self.frame = self.CAM.get_frame()
                try:
                    barcode=decode(self.frame)
                    if len(barcode)==1:
                        for obj in barcode:
                            self.bbox=(obj.rect[0],obj.rect[1],obj.rect[2],obj.$
                        self.set_rect_qr()
                        print("trovato")
                    else:
                        self.set_rect_qr_missing()
                except TypeError:
                    pass
            else:
                print("Arresto qr")
                break
    def set_CAM_obj(self, cam):
        self.CAM = cam

    def set_rect_qr(self):
        p1 = (int(self.bbox[0]), int(self.bbox[1]))
        p2 = (int(self.bbox[0] + self.bbox[2]), int(self.bbox[1] + self.bbox[3]$
        self.CAM.qr_presence = True
        self.CAM.set_qr_rect(p1,p2)

    def set_rect_qr_missing(self):
        self.CAM.qr_presence = False

    def QRdetect(self):
        return self.bbox

if __name__ == '__main__':
    QR_OBJ = QR_class()
    QR_OBJ.start()
