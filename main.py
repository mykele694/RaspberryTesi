from qr import QR_class
from acq_camera import VideoCam
from tracker import Tracker_class
from robot import Robot
# Creo oggetti
CAM = VideoCam()
QR_OBJ = QR_class()
TRACK_OBJ = Tracker_class()
ROBOT_OBJ = Robot()
#inizializzo 

QR_OBJ.set_CAM_obj(CAM)
TRACK_OBJ.set_CAM_obj(CAM)
TRACK_OBJ.set_QR_obj(QR_OBJ)
ROBOT_OBJ.set_obj_cam (CAM)
# Avvio thread
CAM.start()
QR_OBJ.start()
TRACK_OBJ.start()
ROBOT_OBJ.start()
#Robot_def = Robot()

# Inizializzo oggetti
#self.Tracker_obj.set_obj(Robot_def)

# Avvio i Thread

# Avvio la macchina principale

