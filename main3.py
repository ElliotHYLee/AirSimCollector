from MyDrone import MyDrone
from DataRecorder import DataRecorder
import airsim
import threading

lock = threading.Lock()
drone = MyDrone()
dr = DataRecorder(drone, lock)


while dr.numData < 5000:
    print(dr.numData)

dr.done = True



