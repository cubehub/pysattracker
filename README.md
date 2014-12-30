#pysattracker

Python library for calculating azimuth, elevation, doppler shift etc for satellite overflights.

#dependencies
    sudo pip install pyephem

#install
There is no special library installation available. Just clone it into your project directory.
    git clone https://github.com/cubehub/pysattracker.git

Or it is better to use it as a submodule if your project is already using git for version control.
    git submodule add https://github.com/cubehub/pysattracker.git

#example

```python
import sys
import time

from pysattracker import sattracker

ec1_tle = { "name": "ESTCUBE 1", \
            "tle1": "1 39161U 13021C   14364.09038846  .00002738  00000-0  45761-3 0  7997", \
            "tle2": "2 39161  98.0855  83.4746 0010705 128.9405 231.2717 14.70651844 88381"}

tallinn = ("59.4000", "24.8170", "0")

tracker = sattracker.Tracker(satellite=ec1_tle, groundstation=tallinn)

while 1:
    tracker.set_epoch(time.time())

    print "az         : %0.1f" % tracker.azimuth()
    print "ele        : %0.1f" % tracker.elevation()
    print "range      : %0.0f km" % (tracker.range()/1000)
    print "range rate : %0.3f km/s" % (tracker.satellite.range_velocity/1000)
    print "doppler    : %0.0f Hz" % (tracker.doppler(100e6))

    time.sleep(0.5)
```
