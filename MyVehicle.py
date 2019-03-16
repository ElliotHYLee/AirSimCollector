from AirSimClient import *
import numpy as np

class MyVehicle():
    def __init__(self):
        self.client = CarClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.car_controls = CarControls()
        self.car_state = self.client.getCarState()

    def getState(self):
        self.car_state = self.client.getCarState()
        self.timeStamp =self.car_state.timestamp
        vel, pos, quat = self.getGTState()
        return self.timeStamp, vel, pos, quat

    def saveImg(self, t, path):
        img = self.client.simGetImages([ImageRequest(0, AirSimImageType.Scene)])[0].image_data_uint8
        AirSimClientBase.write_file(path + 'img_' + str(t) + '.png', img)

    def getGTState(self):
        vel = self.getXYZ(self.car_state.kinematics_true.linear_velocity)
        pos = self.getXYZ(self.car_state.kinematics_true.position)
        quat = self.getWXYZ((self.car_state.kinematics_true.orientation))
        return vel, pos, quat

    def getWXYZ(self, obj):
        res = [obj.w_val, obj.x_val, obj.y_val, obj.z_val]
        return np.array(res, dtype=np.float32)

    def getXYZ(self, obj):
        res = [obj.x_val, obj.y_val, obj.z_val]
        return np.array(res, dtype=np.float32)

    def reset(self):
        self.client.reset()
        self.client.enableApiControl(False)