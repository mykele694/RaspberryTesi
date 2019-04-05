from threading import Thread

class Robot:
    def __init__(self):
        Thread.__init__()
        Thread.setDaemon = True

        self.robot.is_tracking = False
        self.robot.target_x = None
        self.robot.target_y = None

    def run(self):
        while True:
            if self.robot.is_tracking == True:
                #muoviti
                pass
            else:
                #fermo
                pass
