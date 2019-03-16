from MyDrone import MyDrone
from DataRecorder import DataRecorder
from Navigation import Navigation
from Controller import Controller
import time
import airsim
import threading
import numpy as np


lock = threading.Lock()

drone = MyDrone()
dr = DataRecorder(drone, lock)
nav = Navigation(drone.drone, lock)
nav.takeoff()

ctrl = Controller(drone.drone, lock)

try:
    #drone.drone.moveByAngleZAsync(0.5, 0, 0, 0, duration=10 ** 0)
    for i in range(0, 100):
        drone.drone.moveByVelocityAsync(0, 0, -2, duration=0.01)

except:
    print('err')
    pass

time.sleep(3)

drone.reset()












