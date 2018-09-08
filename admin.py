from client import app
from robot_util import Robot
from lines import best_guess

android = Robot()

@app.route('/robo-update', methods=['POST'])
def robo_upd():

