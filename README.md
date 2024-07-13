# pysattracker

Python library for calculating azimuth, elevation, doppler shift etc for satellite overflights.

# dependencies
    sudo pip install pyephem

# install
There is no special library installation available. Just clone it into your project directory.

    git clone https://github.com/cubehub/pysattracker.git

Or it is better to use it as a submodule if your project is already using git for version control.

    git submodule add https://github.com/cubehub/pysattracker.git

# example

```python
import sys
import time

from pysattracker import sattracker

ec1_tle = {
        "name": "ESTCUBE 1",
        "tle1": "1 39161U 13021C   24194.14473294  .00002706  00000+0  39461-3 0  9991",
        "tle2": "2 39161  97.8269 259.8501 0009982 143.1860 217.0037 14.76566041600819",
    }

tallinn = ("59.4000", "24.8170", "0")

tracker = sattracker.Tracker(satellite=ec1_tle, groundstation=tallinn)

while 1:
    tracker.set_epoch(time.time())
    print ("datetime:", tracker.groundstation.date.datetime())
    print ("az         : %0.1f" % tracker.azimuth())
    print ("ele        : %0.1f" % tracker.elevation())
    print ("range      : %0.0f km" % (tracker.range()/1000))
    print ("range rate : %0.3f km/s" % (tracker.satellite.range_velocity/1000))
    print ("doppler    : %0.0f Hz" % (tracker.doppler(100e6)))

    time.sleep(0.5)
```
