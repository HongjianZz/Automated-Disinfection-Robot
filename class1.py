from flask import Flask, redirect, url_for, render_template, request
#from gpiozero import LED


app = Flask(__name__)

# run the html file
#@app.route("/")
#def home():
#    return render_template("index.html")



@app.route("/", methods=["GET","POST"])
def home():
    if request.method =="POST":
        userValue = request.form["val"] # get the value of val from html file and store as str
        print(userValue)
        IntVal = int(userValue)
        Servo1(IntVal)
        return render_template("index.html")
    else:
        return render_template("index.html")

def Servo1(val):
    if (val<90) and (val>-90):
        print("valid")
    else:
        print("invalid")

        




if __name__ == "__main__":
    app.run()
    





