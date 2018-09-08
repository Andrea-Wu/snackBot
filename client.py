from flask import Flask, render_template, request, redirect
from firebase_admin import credentials, firestore
from random import randint 

#i made these!
from forms import requestForm  

app = Flask(__name__)

#init firebase stuff

pins_queue = ["5000", "8080"]
snack_queue = []

@app.route('/')
def index():
    return "hello :)"

@app.route('/request-robot', methods=["GET", "POST"])
def call_robot():
    form = requestForm()
    if request.method == "POST" and form.validate:
        name = form.name.data
        location = form.location.data
        snack = form.snack.data

        pin = generate_pin()
        global pins_queue

        #this is bad
        while pin in pins_queue:
            pin = generate_pin()
            print("pin is")
            print(pin)
        return redirect("/temp")

        #1. do something with name that interfaces with the LCD screen
        #2. location: idk what to do with this
        

    return render_template("request_robot.html", form=form)



def generate_pin():
    return randint(10000,99999)


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

