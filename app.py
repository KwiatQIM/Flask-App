from flask import Flask, make_response, redirect, request, jsonify, render_template, flash
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)



# Default home page. This is the page the user first sees when visting the site
@app.route('/')
def index():
    return render_template("FrontPage.html")

# This is function grabs the values from the sliders on the previous page.
@app.route("/test", methods=["POST"])
def test():
    epsilon     = request.form["epsilon"]
    decoherence = request.form["decoherence"]
    background  = request.form["background"]
    return background

if __name__ == "__main__":
    app.run(debug=True)
