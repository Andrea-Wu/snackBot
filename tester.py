from robot_util import Robot
import random

def test_random():
    r = Robot()
    dest = (random.randint(0, 100), random.randint(0, 100))
    print("Going to", dest)
    plodding = r.go_to_coord(dest)
    random_tuple = None
    for i in range(100):
        print("Sending", random_tuple)
        print("Robot location", r.x, r.y, r.t)
        nxt = plodding.send(random_tuple)
        print("Next instruction", nxt)
        random_tuple = (random.randint(0, 75), random.randint(0, 75), random.randint(0, 7) % 2 == 0)


