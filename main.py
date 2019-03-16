from MyDrone import MyDrone
from DataRecorder import DataRecorder
import airsim
import threading
import time

lock = threading.Lock()
drone = MyDrone()
dr = DataRecorder(drone, lock)

while dr.numData < 200:
    if dr.numData % 100 == 0:
        print(dr.numData)
        time.sleep(1)

dr.done = True



