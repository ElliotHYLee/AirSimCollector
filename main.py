from MyDrone import MyDrone
from DataRecorder import DataRecorder
from Navigation import Navigation
import time
import airsim
import threading
import numpy as np


lock = threading.Lock()

drone = MyDrone()

nav = Navigation(drone.drone, lock)
dr = DataRecorder(drone, lock)

nav.takeoff()

p0 = [0, 0, -3]
p1 = [80, 0, -3]
p2 = [128, 0, -3]
p3 = [128, 128, -3]
p4 = [0, 128, -3]
p5 = [-128, 128, -3]
p6 = [-128, 0, -3]
p7 = [-128, -128, -3]
p8 = [0, -128, -3]
p9 = [80, -128, -3]
p10 = [128, -128, -3]

# nav.move([0, 0 , -10000])

nav.move(p1)
nav.turnLeft()
nav.move(p9)
nav.turnRight()
nav.move(p10)
nav.turnRight()
nav.move(p2)
nav.turnRight()
nav.move(p0)
nav.turnLeft()
nav.move(p4)
nav.turnLeft()
nav.move(p3)
nav.turnLeft()
nav.move(p10)
nav.turnLeft()
nav.move(p7)
nav.turnLeft()
nav.move(p6)
nav.turnLeft()
nav.move(p0)
nav.turnRight()
nav.move(p4)
nav.turnRight()
nav.move(p5)
nav.turnRight()
nav.move(p7)
nav.turnRight()
nav.move(p8)
nav.turnRight()
nav.move(p4)
nav.turnLeft()
nav.turnLeft()
nav.move(p0)
nav.turnRight()

# nav.turnLeft()
# nav.move(p8)
# nav.turnRight()
# nav.move(p9)
# nav.turnRight()
# nav.move(p1)
# nav.turnLeft()
# nav.move(p2)
# nav.turnRight()
# nav.move(p3)
# nav.turnRight()
# nav.move(p5)
# nav.turnRight()
# nav.move(p6)
# nav.turnRight()
# nav.move(p2)


# nav.move(p1)
# nav.turnLeft()
# nav.move(p9)
# nav.turnRight()
# nav.move(p10)
# nav.turnRight()
# nav.move(p2)
# nav.turnRight()
# nav.move(p0)
# nav.turnRight()


dr.done = True
