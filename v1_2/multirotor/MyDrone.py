import numpy as np
import airsim
import time
class MyDrone():
    def __init__(self):
        self.drone = airsim.MultirotorClient()
        self.reset()
        self.drone.confirmConnection()
        self.drone.enableApiControl(True)
        self.drone.armDisarm(True)
        time.sleep(1)

    def getState(self):
        self.drone_state_gt = self.drone.simGetGroundTruthKinematics()
        self.drone_state_est = self.drone.getMultirotorState()
        vel_gt = self.drone_state_gt['linear_velocity']
        pos_gt = self.drone_state_gt['position']
        quat_gt = self.drone_state_gt['orientation']
        self.timeStamp =self.drone_state_est.timestamp
        return self.timeStamp, self.getXYZ(vel_gt), self.getXYZ(pos_gt), self.getWXYZ(quat_gt)

    def saveImg(self, t, path):
        img = self.drone.simGetImages([airsim.ImageRequest(0, airsim.ImageType.Scene)])[0].image_data_uint8
        airsim.write_file(path + 'img_' + str(t) + '.png', img)

    def getWXYZ(self, obj):
        res = [obj['w_val'], obj['x_val'], obj['y_val'], obj['z_val']]
        return np.array(res, dtype=np.float32)

    def getXYZ(self, obj):
        res = [obj['x_val'], obj['y_val'], obj['z_val']]
        return np.array(res, dtype=np.float32)

    def reset(self):
        self.drone.enableApiControl(False)
        self.drone.reset()


