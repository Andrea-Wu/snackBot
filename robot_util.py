FULL_TURN_DURATION = 5 # TODO: Figure this out
#TODO: CAN WE ROTATE THE WHEELS BACKWARDS?
TURN_TOLERANCE = 69 # TODO: make actual

TIME_FOR_UNIT = 1 #TODO: find out waht this is

SENSOR_SEPARATION = 1 #TODO: find this out

import time
import math

from lines import best_guess

class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.t = 0

    def location(self):
        return (self.x, self.y)

    def turn(self, degs):
        # TODO: if both wheels can't run, make one 0.
        # Can this be done intelligently? (Make the better wheel 0.)
        self.t += deg
        if deg < 0:
            return (-1, 1, FULL_TURN_DURATION * deg / (2 * math.pi))
        return (1, -1, FULL_TURN_DURATION * deg / (2 * math.pi))

    def move_forward(self, d):
        self.x, self.y = (self.x, self.y) + (math.cos(self.t) * d, math.sin(self.t) * d)
        if d > 0:
            return (1, 1, d * TIME_FOR_UNIT)
        else:
            return (-1, -1, d * TIME_FOR_UNIT)

    def turn_and_back_away(self, deg):
        while deg > TURN_TOLERANCE:
            rot = turn(deg)
            curr = time.time()
            l, r, ok = yield rot
            if ok: break
            percent_rot = (time.time() - curr) / rot[2]
            deg *= percent_rot
            # This backward movement is slight and can't fail.
            # We might wanna do the geometry to minimize this, but any amount should work out eventually.
            l, r, ok = yield self.move_forward(-0.1)
            if not ok:
                # this is impossible.
                raise Exception("I blame Andrea")

    def go_to_coord(self, new):
        while (self.x, self.y) != new:
            yield from turn_and_back_away(math.atan((new[1] - self.y)/ (new[0] - self.x)))
            distance = math.sqrt((self.y - new[1]) ** 2 + (self.x - new[0]) ** 2)
            curr = time.time()
            l, r, ok = yield self.move_forward(distance)
            if not ok:
                dt = time.time() - curr / (TIME_FOR_UNIT * distance)
                angle = math.atan((l - r)/ SENSOR_SEPARATION)
                yield from turn_and_back_away(angle)
                o_left = l > r
                l, r, ok = yield self.move_forward(0.1)
                if not ok:
                    angle = math.atan((l - r)/ SENSOR_SEPARATION)
                    if o_left == l < r:
                        angle -= math.pi
                    yield from turn_and_back_away(angle)
                    l, r, ok = yield self.move_forward(0.1)
                    if not ok:
                        raise Exception("Andrea, why'd you put it in a box?")

    def use_best_guesses(self, place):
        for dest in best_guess(self.location(), place):
            yield from self.go_to_coord(dest)

