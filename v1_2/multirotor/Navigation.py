
import time
import airsim
import numpy as np

def quat2euler(quat):
    q0 = quat['w_val']
    q1 = quat['x_val']
    q2 = quat['y_val']
    q3 = quat['z_val']
    phi = np.arctan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 ** 2 + q2 ** 2))
    the = np.arcsin(2 * (q0 * q2 - q3 * q1))
    psi = np.arctan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 ** 2 + q3 ** 2))
    return np.array([phi, the, psi])

class Navigation():
    def __init__(self, drone, lock):
        self.drone = drone
        self.lock = lock

    def correct(self, yaw):
        h = np.array([0, np.pi/2, np.pi, -np.pi, -np.pi/2])
        c = np.abs(yaw*np.ones_like(h) - h)
        return h[np.argmin(c)]

    def turnRight(self):
        cYaw = self.correct(self.getCurrentYaw())
        targetYaw = cYaw + np.pi/2
        self.yaw(cYaw, targetYaw)

    def turnLeft(self):
        cYaw = self.correct(self.getCurrentYaw())
        targetYaw = cYaw - np.pi / 2
        self.yaw(cYaw, targetYaw)

    def getCurrentYaw(self):
        with self.lock:
            quat = self.drone.simGetGroundTruthKinematics()['orientation']
        euler = quat2euler(quat)
        return euler[2]

    def getPos(self):
        with self.lock:
            pos = self.drone.simGetVehiclePose().position
        x = pos.x_val
        y = pos.y_val
        z = pos.z_val
        return [x, y, z]

    def getVel(self):
        with self.lock:
            v = self.drone.simGetGroundTruthKinematics()['linear_velocity']
        x = v['x_val']
        y = v['y_val']
        z = v['z_val']
        return [x, y, z]

    def takeoff(self):
        print('taking off')
        target = -3
        pos = self.getPos()
        with self.lock:
            self.drone.moveToPositionAsync(pos[0], pos[1], target, 3)
        pos = self.getPos()
        v = self.getVel()
        while (np.abs(pos[2]-target) > 0.1 or np.abs(v[1]) > 0.1):
            pos = self.getPos()
            vel = self.getVel()

    def yaw(self, cYaw, targetYaw):
        pos = self.getPos()
        dYaw = targetYaw - cYaw
        for i in range(0, 100):
            cYaw += dYaw / 100
            with self.lock:
                self.drone.moveByAngleZAsync(pitch=0, roll=0, z=pos[2], yaw=cYaw, duration=0.03)
            time.sleep(0.03)
        time.sleep(1.5)
        return targetYaw

    def moveToTargetPoint(self, tp, v):
        with self.lock:
            self.drone.moveToPositionAsync(tp[0], tp[1], tp[2], v)

    def move(self, tp):
        self.moveToTargetPoint(tp, 8)
        self.waitForPreCheckPoint(tp, preDist=50)
        self.moveToTargetPoint(tp, 5)
        self.waitForPreCheckPoint(tp, preDist=10)
        self.moveToTargetPoint(tp, 1)
        self.waitWhile(tp)

    def waitForPreCheckPoint(self, targetPos, preDist = 15):
        while (not self.isReached(targetPos, preDist)):
            time.sleep(0.01)

    def isReached(self, targetPos, preDist=15):
        pos = self.getPos()
        dist = self.getDistance(pos, targetPos)
        if (dist < preDist):
            return True
        else:
            return False

    def waitWhile(self, targetPos, preDist = 15):
        while (not self.isArrived(targetPos)):
            time.sleep(0.01)

    def isArrived(self, targetPos, preDist = 0):
        pos = self.getPos()
        dist = self.getDistance(pos, targetPos) - preDist
        if (dist < 1 and self.getSpeed()<0.01):
            return True
        else:
            return False

    def getSpeed(self):
        vel = np.array(self.getVel())
        return np.sqrt(np.dot(vel, vel))

    def getDistance(self, p1, p2):
        tx, ty, tz = p2[0], p2[1], p2[2]
        x, y, z = p1
        loss = np.array([tx-x, ty-y, tz-z])
        loss2 = np.dot(loss, loss)
        dist = np.sqrt(loss2)
        return dist





