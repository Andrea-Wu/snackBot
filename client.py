from flask import Flask
app = Flask(__name__)

# user can enter pin
@app.route('/num-pad')
def num_pad():
    

