# In settings.json first activate computer vision mode:
# https://github.com/Microsoft/AirSim/blob/master/docs/image_apis.md#computer-vision-mode

import setup_path
import numpy as np
import airsim
import cv2
import pprint
def getXYZ(obj):
    res = [obj.x_val, obj.y_val, obj.z_val]
    return np.array(res, dtype=np.float32)


client = airsim.CarClient()
client.confirmConnection()

# car_state_gt = client.simGetGroundTruthKinematics()
# vel_gt = car_state_gt['linear_velocity']
# pos_gt = car_state_gt['position']
# print(vel_gt)
# print(pos_gt)

car_state = client.getCarState()
t = np.array([car_state.timestamp], dtype=np.longlong)
vel = getXYZ(car_state.kinematics_estimated.linear_velocity)
spd = np.array(car_state.speed, dtype=np.float32)
pos = getXYZ(car_state.kinematics_estimated.position)

print(t)
print(vel)
print(pos)

responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.DepthVis),
        airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True),
        airsim.ImageRequest("2", airsim.ImageType.Segmentation),
        airsim.ImageRequest("3", airsim.ImageType.Scene),
        airsim.ImageRequest("4", airsim.ImageType.DisparityNormalized),
        airsim.ImageRequest("4", airsim.ImageType.SurfaceNormals)])

for i, response in enumerate(responses):
    if response.image_type == airsim.ImageType.Scene:
        airsim.write_file(str(i) + '.png', response.image_data_uint8)
    # if response.pixels_as_float:
    #     print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_float), pprint.pformat(response.camera_position)))
    #     airsim.write_pfm(str(i) + '.pfm', airsim.get_pfm_array(response))
    # else:
    #     print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_uint8), pprint.pformat(response.camera_position)))
    #     airsim.write_file(str(i) + '.png', response.image_data_uint8)

# for i, response in enumerate(responses):
#
#     AirSimClientBase.write_file(str(i) + '.png', response.image_data_uint8)







