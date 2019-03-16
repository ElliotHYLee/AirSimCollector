import numpy as np
import airsim
import time
import cv2
import os
from PIL import Image
class MyDrone():
    def __init__(self, drone, lock):
        self.drone = drone
        self.lock = lock

    def getState(self):
        self.drone_state_gt = self.drone.simGetGroundTruthKinematics()
        self.drone_state_est = self.drone.getMultirotorState()
        vel_gt = self.drone_state_gt.linear_velocity
        pos_gt = self.drone_state_gt.position
        quat_gt = self.drone_state_gt.orientation
        self.timeStamp =self.drone_state_est.timestamp
        dwdt = self.drone_state_est.kinematics_estimated.angular_velocity
        dwdt = np.array([dwdt.x_val, dwdt.y_val, dwdt.z_val], dtype=np.float32)
        dvdt = self.drone_state_est.kinematics_estimated.linear_acceleration
        dvdt = np.array([dvdt.x_val, dvdt.y_val, dvdt.z_val], dtype=np.float32)

        return self.timeStamp, self.getXYZ(vel_gt), self.getXYZ(pos_gt), self.getWXYZ(quat_gt), dwdt, dvdt

    def getWXYZ(self, obj):
        res = [obj.w_val, obj.x_val, obj.y_val, obj.z_val]
        return np.array(res, dtype=np.float32)

    def getXYZ(self, obj):
        res = [obj.x_val, obj.y_val, obj.z_val]
        return np.array(res, dtype=np.float32)


