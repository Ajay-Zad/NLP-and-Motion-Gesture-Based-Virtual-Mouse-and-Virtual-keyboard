from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mouse_home.html")
def mohome():
    return render_template("mouse_home.html")

@app.route("/mouse_hand.html")
def mohand():
    return render_template("mouse_hand.html")

@app.route("/mouse_eye.html")
def moeye():
    return render_template("mouse_eye.html")

@app.route("/mouse_voice.html")
def movoice():
    return render_template("mouse_voice.html")

@app.route("/keyboard_home.html")
def keyhome():
    return render_template("keyboard_home.html")

@app.route("/keyboard_hand.html")
def keyhand():
    return render_template("keyboard_hand.html")


    

if __name__ == "__main__":
    app.run(debug=True, port=5000)