from flask import Flask, render_template, request, redirect
from firebase_admin import credentials, firestore

app = Flask(__name__)

#init firebase stuff

pins_queue = ["5000", "8080"]

@app.route('/')
def index():
    return "hello :)"

# user can enter pin
@app.route('/num-pad')
def num_pad():
    return render_template("num_pad.html")

@app.route('/temp')
def temp():
    return "ass"

@app.route('/check-pin', methods=["POST"])
def check_pin():
    pin = (request.data).decode("utf-8")

    #apparently this checks if list is empty
    global pins_queue

    if pins_queue:
        p= pins_queue[0]
        if pin == p:
            print("ayyyy lmao")
            pins_queue = pins_queue[1:]
            print(pins_queue)
            
            #code that tells the server to go to the next person lol
            return redirect("/temp")
        else:
            print("p is " + p)
            print("pin is " + pin)
            print(pins_queue)
            print("try again")
            return render_template("num_pad.html")
    else:
        return render_template("num_pad.html")

if __name__ == '__main__':
    app.run(port=5001)

