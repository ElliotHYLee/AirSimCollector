import numpy as np
import airsim
import time
import cv2
import os
from PIL import Image
class MyDrone():
    def __init__(self):
        print('im here1')
        self.drone = airsim.MultirotorClient()
        print('im here2')
        #self.resetAll()
        print('im here3')
        self.drone.confirmConnection()
        print('im here4')
        #self.drone.enableApiControl(True)
        self.drone.armDisarm(True)
        print('im here5')
        time.sleep(1)

    def setAttitude(self, roll, pitch, yaw):
        pitch = pitch * np.pi / 180
        roll = roll * np.pi / 180
        yaw = yaw * np.pi / 180
        z = 0
        self.drone.moveByAngleZAsync(pitch, roll, z, yaw, duration=10**-4)

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

        return self.timeStamp, self.getXYZ(vel_gt), self.getXYZ(pos_gt),\
               self.getWXYZ(quat_gt), dwdt, dvdt

    def depthImg(self, data):
        img1d = np.array(data.image_data_float, dtype=np.float)
        img1d = 255 / np.maximum(np.ones(img1d.size), img1d)
        img2d = np.reshape(img1d, (data.height, data.width))
        image = np.invert(np.array(Image.fromarray(img2d.astype(np.uint8), mode='L')))
        factor = 10
        maxIntensity = 255.0  # depends on dtype of image data

        # Decrease intensity such that dark pixels become much darker, bright pixels become slightly dark
        newImage1 = (maxIntensity) * (image / maxIntensity) ** factor
        newImage1 = np.array(newImage1, dtype=np.uint8)
        return newImage1

    def saveImg(self, t, path):
        #img = self.drone.simGetImages([airsim.ImageRequest(0, airsim.ImageType.Scene)])[0].image_data_uint8
        responses = self.drone.simGetImages([airsim.ImageRequest(0, airsim.ImageType.DepthPerspective, True)])
        depthImg = self.depthImg(responses[0])

        # cv2.imshow('asdf', newImage1)
        # cv2.waitKey(1)
        cv2.imwrite(path + 'img_' + str(t) + '.png', depthImg)
        #airsim.write_file(path + 'img_' + str(t) + '.png', img)

    def getWXYZ(self, obj):
        res = [obj.w_val, obj.x_val, obj.y_val, obj.z_val]
        return np.array(res, dtype=np.float32)

    def getXYZ(self, obj):
        res = [obj.x_val, obj.y_val, obj.z_val]
        return np.array(res, dtype=np.float32)

    def resetAll(self):
        self.drone.enableApiControl(False)
        self.drone.reset()

    def reset(self):
        self.drone.reset()

