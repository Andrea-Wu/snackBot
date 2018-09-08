from client import app, pathq
from robot_util import robot

curr_path = None
android = Robot()

@app.route('/robo-update', methods=['POST'])
def robo_upd():
    form = roboForm()
    if request.method == "POST" and form.validate:
        l = form.l.data
        r = form.r.data
        ok = form.ok.data
        while pathq:
            try:
                if curr_path is not None:
                    return str(curr_path.send(l, r, ok))
                else:
                    curr_path = android.use_best_guesses(pathq[0])
                    pathq = pathq[1:]
            except StopIteration:
                curr_path = None
        return "Done!"
