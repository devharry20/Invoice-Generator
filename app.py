from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder=os.getcwd() + r"\static\templates")

@app.route("/", methods=["GET", "POST"])
def hello_world():
    return render_template("index.html")

app.run()