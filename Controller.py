
import time
import airsim
import numpy as np

def quat2euler(quat):
    q0 = quat.w_val
    q1 = quat.x_val
    q2 = quat.y_val
    q3 = quat.z_val
    phi = np.arctan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 ** 2 + q2 ** 2))
    the = np.arcsin(2 * (q0 * q2 - q3 * q1))
    psi = np.arctan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 ** 2 + q3 ** 2))
    return np.array([phi, the, psi])

class Controller():
    def __init__(self, drone, lock):
        self.drone = drone
        self.lock = lock

    def getDistance(self, p1, p2):
        tx, ty, tz = p2[0], p2[1], p2[2]
        x, y, z = p1
        loss = np.array([tx - x, ty - y, tz - z])
        loss2 = np.dot(loss, loss)
        dist = np.sqrt(loss2)
        return dist

    def setPoint(self, tp):
        pass

    def setVelocity(self, tv):
        self.drone.moveByVelocityAsync(tv[0], tv[1], -tv[2], duration=0.01)


