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
<<<<<<< HEAD
    epsilon     = request.form["epsilon"]
    decoherence = request.form["decoherence"]
    background  = request.form["background"]
    return background
=======
    slider_1_val = request.form["slide1"]
    slider_2_val = request.form["slide2"]
    slider_3_val = request.form["slide3"]
    return slider_2_val
>>>>>>> d87bf36c3bcbe32eaf626da20db36983c66ac11e

if __name__ == "__main__":
    app.run(debug=True)
