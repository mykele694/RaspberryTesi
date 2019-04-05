import threading 
import time
from random import randint

#Definizione del lock
threadLock = threading.Lock()

class IlMioThread (threading.Thread):
    def __init__(self, nome, durata):
        threading.Thread.__init__(self)
        self.nome = nome
        self.durata = durata
    def run(self):
        print ("Thread ' " + self.nome + "' avviato")
        #Acquisizione del lock
        threadLock.acquire()
        time.sleep(self.durata)
        print ("Thread ' " + self.nome + "' terminato")
        #Rilascio del lock
        threadLock.release()

#Creazione dei thread
thread1 = IlMioThread("Thread#1", randint(1,100))
thread2 = IlMioThread("Thread#2", randint(1,100))
thread3 = IlMioThread("Thread#3", randint(1,100))

#Avvio dei thread
thread1.start()
thread2.start()
thread3.start()

#Join
thread1.join()
thread2.join()
thread3.join()

#Fine dello script
print("Fine")