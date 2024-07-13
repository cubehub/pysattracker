'''

https://github.com/cubehub/pysattracker/tree/master
https://rhodesmill.org/pyephem/rise-set.html
'''
import time
import datetime

from math import sin, cos, radians, degrees
from pynmeagps import llh2ecef
import ephem

class Tracker():

    def __init__(self, satellite, groundstation=("59.4000", "24.8170", "0")):
        self.groundstation = ephem.Observer()
        self.groundstation.pressure = 0
        #self.groundstation.horizon = '-0:34' # 1⁄60 of a degree of an angle
        self.groundstation.lat = groundstation[0]
        self.groundstation.lon = groundstation[1]
        self.groundstation.elevation = int(groundstation[2])

        self.satellite = ephem.readtle(satellite["name"], satellite["tle1"], satellite["tle2"])

    def set_epoch(self, epoch=time.time()):
        ''' sets epoch when parameters are observed '''

        self.groundstation.date = datetime.datetime.fromtimestamp(epoch,tz=datetime.UTC)
        self.satellite.compute(self.groundstation)

    def azimuth(self):
        ''' returns satellite azimuth in degrees '''
        return degrees(self.satellite.az)

    def elevation(self):
        ''' returns satellite elevation in degrees '''
        return degrees(self.satellite.alt)

    def latitude(self):
        ''' returns satellite latitude in degrees '''
        return degrees(self.satellite.sublat)

    def longitude(self):
        ''' returns satellite longitude in degrees '''
        return degrees(self.satellite.sublong)

    def range(self):
        ''' returns satellite range in meters '''
        return self.satellite.range

    def doppler(self, frequency_hz=437_505_000):
        ''' returns doppler shift in hertz '''
        return -self.satellite.range_velocity / 299792458. * frequency_hz

    def ecef_coordinates(self):
        ''' returns satellite earth centered cartesian coordinates
            https://en.wikipedia.org/wiki/ECEF
        '''
        x, y, z = self._aer2ecef(self.azimuth(), self.elevation(), self.range(), float(self.groundstation.lat), float(self.groundstation.lon), self.groundstation.elevation)
        return x, y, z

    def _aer2ecef(self, azimuthDeg, elevationDeg, slantRange, obs_lat, obs_long, obs_alt):

        #site ecef in meters
        sitex, sitey, sitez = llh2ecef(obs_lat,obs_long,obs_alt)

        #some needed calculations
        slat = sin(radians(obs_lat))
        slon = sin(radians(obs_long))
        clat = cos(radians(obs_lat))
        clon = cos(radians(obs_long))

        azRad = radians(azimuthDeg)
        elRad = radians(elevationDeg)

        # az,el,range to sez convertion
        south  = -slantRange * cos(elRad) * cos(azRad)
        east   =  slantRange * cos(elRad) * sin(azRad)
        zenith =  slantRange * sin(elRad)

        x = ( slat * clon * south) + (-slon * east) + (clat * clon * zenith) + sitex
        y = ( slat * slon * south) + ( clon * east) + (clat * slon * zenith) + sitey
        z = (-clat *        south) + ( slat * zenith) + sitez

        return x, y, z



if __name__ == "__main__":
    # taken from: http://celestrak.com/NORAD/elements/cubesat.txt
    ec1_tle = {
        "name": "ESTCUBE 1",
        "tle1": "1 39161U 13021C   24194.14473294  .00002706  00000+0  39461-3 0  9991",
        "tle2": "2 39161  97.8269 259.8501 0009982 143.1860 217.0037 14.76566041600819",
    }

    # http://www.gpscoordinates.eu/show-gps-coordinates.php
    tallinn = ("59.4000", "24.8170", "0")

    tracker = Tracker(satellite=ec1_tle, groundstation=tallinn)
    
    #diff = time.time() - tracker.satellite.epoch.datetime().timestamp()
    diff = 0 

    while 1:
        tracker.set_epoch(time.time()- diff)
        print ("datetime:", tracker.groundstation.date.datetime())
        print ("az         : %0.1f" % tracker.azimuth())
        print ("ele        : %0.1f" % tracker.elevation())
        print ("range      : %0.0f km" % (tracker.range()/1000))
        print ("range rate : %0.3f km/s" % (tracker.satellite.range_velocity/1000))
        print ("doppler    : %0.0f Hz" % (tracker.doppler(100e6)))

        time.sleep(0.5)
