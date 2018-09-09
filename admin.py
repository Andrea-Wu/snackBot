from flask import jsonify

from client import app, pathq
from robot_util import robot
from lines import Line

curr_path = None
android = Robot()

@app.route('/robo-update', methods=['POST'])
def robo_upd():
    if request.method == "POST":
        tlp = request.data.split(',')
        while pathq:
            try:
                if curr_path is not None:
                    return ','.join(curr_path.send(tpl))
                else:
                    curr_path = android.use_best_guesses(pathq[0])
                    pathq = pathq[1:]
                    tpl = None
            except StopIteration:
                curr_path = None
        return "Done!"

@app.route('/dump-info')
def dump_info():
    return jsonify({
        "pathq": pathq,
        "robotPos": android.location() + (android.t,),
        "lines": Line.all_lines()
    })
