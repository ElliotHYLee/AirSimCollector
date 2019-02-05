from AirSimClient import *
import sys
import time

def yaw(cYaw, targetYaw):
    dYaw = targetYaw - cYaw
    for i in range(0, 100):
        cYaw += dYaw / 100
        client.moveByAngle(pitch=0, roll=0, z=z, yaw=cYaw, duration=10)
        time.sleep(0.02)
    time.sleep(5)

client = MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

print('here1')
client.armDisarm(True)
#client.takeoff()
z = -7
y = -130
print('taking off')
client.moveToPosition(0, 0, z, 1)
print('hover mode')
time.sleep(3)
cYaw = 0
print('starting yaw')
# for i in range(0,100):
#     cYaw += -np.pi/2/100
#     client.moveByAngle(pitch=0, roll=0, z=z, yaw=cYaw, duration=10)
#     time.sleep(0.025)
# time.sleep(1)
yaw(0, -np.pi/2)

# see https://github.com/Microsoft/AirSim/wiki/moveOnPath-demo


p1 = Vector3r(0, -130, z)
p2 = Vector3r(125, -130, z)
p3 = Vector3r(125, 0, z)
p4 = Vector3r(130, 110, z)

# result = client.moveOnPath([p1, p2],10, 10000, DrivetrainType.ForwardOnly, YawMode(False, 0), 15, 1)

client.moveToPosition(p1.x_val, p2.y_val, p3.z_val, 10)
time.sleep(3)
client.moveToPosition(p1.x_val, p2.y_val, p3.z_val, 10)
time.sleep(3)
x = client.getMultirotorState().kinematics_true.position.x_val
y = client.getMultirotorState().kinematics_true.position.y_val

print('descending')
client.moveToPosition(x, y, -2, 3)
time.sleep(3)
client.moveToPosition(x, y, -1, 2)
time.sleep(3)
# print('hre 1')
# print(result)
# client.moveToPosition(120,y,-3, 5)
print('landing')
client.land()
client.armDisarm(False)
client.enableApiControl(False)
time.sleep(1)
client.reset()
