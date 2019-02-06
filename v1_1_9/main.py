from MyVehicle import MyVehicle
from DataManager import DataManager
# connect to the AirSim simulator
import time
import asyncio
def main():
    vehicle = MyVehicle()
    dm = DataManager(vehicle)

    t = 0
    prev = time.time()
    now = 0
    for i in range(0, 10):
        prevT = t
        t, vel, pos, quat = vehicle.getState()
        dm.saveImg(t)
        dm.writeToFile(t, vel, pos, quat) # this also saves img
        now = time.time()
        elapsed = now - prev
        while (elapsed < 0.09):
            now = time.time()
            elapsed = now - prev
        dt = (t - prevT) / 10 ** 9
        print(1 / dt)
        prev = now

    dm.closeFile()

    # print(t)
    # print(vel)
    # print(pos)
    # print(quat)

    vehicle.reset()


if __name__ == '__main__':
    main()
