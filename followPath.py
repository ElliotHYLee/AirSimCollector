from AirSimClient import *
import numpy as np
import time

def yaw(cYaw, targetYaw):
    print('starting yaw')
    z = client.getMultirotorState().kinematics_true.position.z_val
    dYaw = targetYaw - cYaw
    for i in range(0, 100):
        cYaw += dYaw / 100
        client.moveByAngle(pitch=0, roll=0, z=z, yaw=cYaw, duration=10)
        time.sleep(0.02)
    time.sleep(3)

def takeoff(client):
    x = client.getMultirotorState().kinematics_true.position.x_val
    y = client.getMultirotorState().kinematics_true.position.y_val
    print('taking off')
    client.moveToPosition(x, y, -2, 3)
    print('hover mode')
    time.sleep(2)

def land(client):
    x = client.getMultirotorState().kinematics_true.position.x_val
    y = client.getMultirotorState().kinematics_true.position.y_val
    print('descending')
    client.moveToPosition(x, y, -1, 3)
    time.sleep(3)
    print('landing')
    client.land()

def quat2euler(quat):
    q0 = quat.w_val
    q1 = quat.x_val
    q2 = quat.y_val
    q3 = quat.z_val
    phi = np.arctan2(2*(q0*q1+q2*q3), 1-2*(q1**2+q2**2))
    the = np.arcsin(2*(q0*q2-q3*q1))
    psi = np.arctan2(2*(q0*q3+q1*q2), 1-2*(q2**2+q3**2))
    return np.array([phi, the, psi])

def euler2rot(euler):
    x,y,z = euler
    Rz = np.array([[np.cos(z), -np.sin(z), 0],
                   [np.sin(z), np.cos(z), 0],
                   [0, 0, 1]])
    Ry = np.array([[np.cos(y), 0, np.sin(y)],
                   [0, 1, 0],
                   [-np.sin(y), 0, np.cos(y)]])
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(x), -np.sin(x)],
                   [0, np.sin(x), np.cos(x)]])
    R = np.dot(Rz, np.dot(Ry, Rx))
    print(R)
    return R


client = MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

print('Disarming')
client.armDisarm(True)
print('Taking off')
takeoff(client)
print('Change Heading..')
cYaw = 0
yaw(0, -np.pi/2)

print('calculating veloity')
print(client.getMultirotorState().kinematics_estimated.orientation)
euler = quat2euler(client.getMultirotorState().kinematics_estimated.orientation)
print(euler)
euler2rot(euler)
velB = np.array([[2, 0 ,0]]).transpose()
velG = np.matmul(euler2rot(euler),velB)
print('erher2')
print(velG)

# see https://github.com/Microsoft/AirSim/wiki/moveOnPath-demo
z = -2
p1 = Vector3r(0, -130, z)
p2 = Vector3r(125, -130, z)
p3 = Vector3r(125, 0, z)
p4 = Vector3r(130, 110, z)

# result = client.moveOnPath([p1, p2],10, 10000, DrivetrainType.ForwardOnly, YawMode(False, 0), 15, 1)
print()
print('velocty')

dur = 10

# client.moveByVelocity(velG[0,0], velG[1,0], velG[2,0], duration=dur, drivetrain=DrivetrainType.ForwardOnly, yaw_mode=YawMode(False, 0))
# time.sleep(10)

# result = client.moveOnPath([Vector3r(0,-253,z),Vector3r(125,-253,z),Vector3r(125,0,z),Vector3r(0,0,z),Vector3r(0,0,-20)],
#                         15, 65,
#                         DrivetrainType.ForwardOnly, YawMode(False,0), 20, 1)
client.moveToPosition(p1.x_val, p2.y_val+10, p3.z_val, 2)
client.setCameraOrientation(0, airsim.to_quaternion(0.261799, 0, 0))
time.sleep(3)
# client.moveToPosition(p1.x_val, p2.y_val, p3.z_val, 2)
# time.sleep(3)
# client.moveToPosition(p1.x_val, p2.y_val, p3.z_val, 1)
# time.sleep(3)


# land(client)


client.armDisarm(False)
client.enableApiControl(False)
time.sleep(1)
client.reset()
