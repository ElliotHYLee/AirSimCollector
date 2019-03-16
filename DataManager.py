import os
from time import gmtime, strftime
# import _thread as thread

class DataManager():
    def __init__(self, vehicle):
        # init folder and txt file
        self.vehicle = vehicle
        self.path = os.getcwd()+'/'
        self.createFolder()
        self.file = open(self.path + '/data.txt', 'w')

    def createFolder(self):
        dd = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
        self.path += dd
        try:
            os.mkdir(self.path)
            os.mkdir(self.path + '/images')
        except OSError:
            print('error: cannot create a folder')

    def saveImg(self, t):
       #self.vehicle.saveRawImg(t, self.path + '/images/')
       self.vehicle.saveSemImg(t, self.path + '/images/')

    def writeToFile(self, t, vel, pos, quat, dwdt, dvdt):
        fName = 'img_' + str(t) + '.png'
        self.file.write('%d '
                        '%.4f %.4f %.4f '
                        '%.4f %.4f %.4f '
                        '%.4f %.4f %.4f %.4f '
                        '%.4f %.4f %.4f '
                        '%.4f %.4f %.4f\n'
                        %(t,
                          vel[0], vel[1], vel[2],
                          pos[0], pos[1], pos[2],
                          quat[0], quat[1], quat[2], quat[3],
                          dwdt[0], dwdt[1], dwdt[2],
                          dvdt[0],dvdt[1], dvdt[2]))
    def closeFile(self):
        self.file.close()
