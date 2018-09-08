FULL_TURN_DURATION = 5 # TODO: Figure this out
#TODO: CAN WE ROTATE THE WHEELS BACKWARDS?
TURN_TOLERANCE = 69 # TODO: make actual

TIME_FOR_UNIT = 1 #TODO: find out waht this is

SENSOR_SEPARATION = 1 #TODO: find this out

import time
import math

def turn(degs):
    # TODO: if both wheels can't run, make one 0.
    # Can this be done intelligently? (Make the better wheel 0.)
    if deg < 0:
        return (1, -1, FULL_TURN_DURATION * deg / (2 * math.pi))
    return (-1, 1, FULL_TURN_DURATION * deg / (2 * math.pi))

def turn_and_back_away(deg):
    while deg > 0:
        rot = turn(deg)
        curr = time.time()
        l, r, ok = yield rot
        if ok: break
        percent_rot = (time.time() - curr) / rot[2]
        deg *= percent_rot
        # This backward movement is slight and can't fail.
        # We might wanna do the geometry to minimize this, but any amount should work out eventually.
        l, r, ok = yield (-1, 1, TIME_FOR_UNIT * 0.1)
        if not ok:
            # this is impossible.
            raise Exception("I blame Andrea")

def go_to_coord(old, new):
    while old != new:
        yield from turn_and_back_away(math.atan(new[1] - old[1], new[0] - old[0]))
        distance = math.sqrt((old[1] - new[1]) ** 2 + (old[0] - new[0]) ** 2)
        curr = time.time()
        l, r, ok = yield (1, 1,TIME_FOR_UNIT *distance)
        if not ok:
            dt = time.time() - curr / (TIME_FOR_UNIT * distance)
            angle = math.atan((l - r)/ SENSOR_SEPARATION)
            yield from turn_and_back_away(angle)

