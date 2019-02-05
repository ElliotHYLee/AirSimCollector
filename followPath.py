from AirSimClient import *
import sys
import time

client = MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

print('here1')
client.armDisarm(True)
#client.takeoff()
z = -7
y = -130
print('taking off')
client.moveToPosition(0, 0, z, 3)
print('hover mode')
time.sleep(1.5)
cYaw = 0
print('starting yaw')
for i in range(0,100):
    cYaw += -np.pi/2/100
    client.moveByAngle(pitch=0, roll=0, z=z, yaw=cYaw, duration=10)
    time.sleep(0.025)
time.sleep(1)

# see https://github.com/Microsoft/AirSim/wiki/moveOnPath-demo

# this method is async and we are not waiting for the result since we are passing max_wait_seconds=0.
result = client.moveOnPath([Vector3r(0,-130,z),Vector3r(130,-130,z),
                            Vector3r(130,0,z), Vector3r(130,127,z),
                            Vector3r(0, 127, z), Vector3r(-120, 127, z),
                            Vector3r(-120, 127, -30), Vector3r(0, 0, -30)],
                        10, 10000,
                        DrivetrainType.ForwardOnly, YawMode(False, 0), 15, 1)


client.moveToPosition(0, 0, -5, 10)
client.moveToPosition(0, 0, -0.2, 1)

time.sleep(10)
# print('hre 1')
# print(result)
# client.moveToPosition(120,y,-3, 5)

client.land()
client.armDisarm(False)
client.enableApiControl(False)
time.sleep(1)
client.reset()
