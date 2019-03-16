
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

    def setAttitude(self, roll, pitch, yaw):
        pitch = pitch * np.pi / 180
        roll = roll * np.pi / 180
        yaw = yaw * np.pi / 180
        z = 0
        self.drone.moveByAngleZAsync(pitch, roll, z, yaw, duration=10**-4)


