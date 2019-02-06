from DataManager import DataManager
import time
from threading import Thread

class DataRecorder():
    def __init__(self, drone, lock):
        self.lock = lock
        self.drone = drone
        self.dm = DataManager(self.drone)
        self.done = False
        t = Thread(target = self.record)
        t.start()

    def record(self):
        t = 0
        prev = time.time()
        now = 0
        while(not self.done):
            prevT = t
            with self.lock:
                t, vel, pos, quat = self.drone.getState()
                self.dm.saveImg(t)
            self.dm.writeToFile(t, vel, pos, quat)  # this also saves img
            now = time.time()
            elapsed = now - prev
            while (elapsed < 0.09):
                now = time.time()
                elapsed = now - prev
            dt = (t - prevT) / 10 ** 9
            print(1 / dt)
            prev = now

        self.dm.closeFile()




