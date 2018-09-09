FULL_TURN_DURATION = 5 # TODO: Figure this out
#TODO: CAN WE ROTATE THE WHEELS BACKWARDS?
TURN_TOLERANCE = 0.06 # TODO: make actual

TIME_FOR_UNIT = 1 #TODO: find out waht this is

SENSOR_SEPARATION = 1 #TODO: find this out

import time
import math

from lines import best_guess, Line

class Robot:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.t = 0

    def location(self):
        return (self.x, self.y)

    def turn(self, deg):
        # TODO: if both wheels can't run, make one 0.
        # Can this be done intelligently? (Make the better wheel 0.)
        if deg < 0:
            return (-1, 1, FULL_TURN_DURATION * deg / (2 * math.pi))
        return (1, -1, FULL_TURN_DURATION * deg / (2 * math.pi))

    def record_rotation(self, start_time, end_time, intent, ok):
        if not ok:
            df = -1 if intent < 0 else 1
            self.t += df *  (end_time - start_time) / FULL_TURN_DURATION / (2 * math.pi)
        else:
            self.t += intent

    def move_forward(self, d):
        if d > 0:
            return (1, 1, d * TIME_FOR_UNIT)
        else:
            return (-1, -1, d * TIME_FOR_UNIT)

    def record_motion(self, start_time, end_time, intent, ok):
        if not ok:
            df = -1 if intent < 0 else 1
            self.x += df * math.cos(self.t) * TIME_FOR_UNIT * (end_time - start_time)
            self.y += df * math.sin(self.t) * TIME_FOR_UNIT * (end_time - start_time)
        else:
            self.x += math.cos(self.t) * intent
            self.y += math.sin(self.t) * intent

    def turn_and_back_away(self, deg):
        while deg > TURN_TOLERANCE:
            rot = self.turn(deg)
            curr = time.time()
            l, r, ok = yield rot
            self.record_rotation(curr, time.time(), deg, ok)
            if ok: break
            # This backward movement is slight and can't fail.
            # We might wanna do the geometry to minimize this, but any amount should work out eventually.
            curr = time.time()
            l, r, ok = yield self.move_forward(-0.1)
            self.record_motion(curr, time.time(), -0.1, ok)
            if not ok:
                # this is impossible.
                raise Exception("I blame Andrea")

    def go_to_coord(self, new):
        line_start = None
        while (self.x, self.y) != new:
            #point toward the target
            yield from self.turn_and_back_away(math.atan((new[1] - self.y)/ (new[0] - self.x)))

            #go to target (if possible)
            distance = math.sqrt((self.y - new[1]) ** 2 + (self.x - new[0]) ** 2)
            curr = time.time()
            l, r, ok = yield self.move_forward(distance)
            self.record_motion(curr, time.time(), distance, ok)

            #didn't work?!
            if not ok:
                #record where we're at and turn the smallest reasonable amount
                line_start = self.location()
                angle = math.atan((l - r)/ SENSOR_SEPARATION)
                yield from self.turn_and_back_away(angle)
                # recall whether the obstacle is on the left or right
                o_left = l > r

                #move a bit forward
                curr = time.time()
                l, r, ok = yield self.move_forward(0.1)
                self.record_motion(curr, time.time(), 0.1, ok)

                #we can't move forward - we have a corner case
                if not ok:
                    #turn away from the known wall, along the new one
                    angle = math.atan((l - r)/ SENSOR_SEPARATION)
                    if o_left == l < r:
                        angle -= math.pi
                    yield from self.turn_and_back_away(angle)

                    #move alogn the second wall for a bit.
                    curr = time.time()
                    l, r, ok = yield self.move_forward(0.1)
                    self.record_motion(curr, time.time(), 0.1, ok)
                    #if you're at a third corner, give up
                    if not ok:
                        raise Exception("Andrea, why'd you put it in a box?")
            elif line_start is not None:
                Line(line_start, self.location()).clean_firebase()

    def use_best_guesses(self, place):
        for dest in best_guess(self.location(), place):
            yield from self.go_to_coord(dest)

