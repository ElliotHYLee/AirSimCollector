# In settings.json first activate computer vision mode:
# https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode

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
nav = Navigation(drone.drone, lock)
nav.takeoff()

# ctrl = Controller(drone.drone, lock)
try:
    drone.setAttitude(0, 10, 0)
except:
    print('err')
    pass

time.sleep(3)

drone.reset()












