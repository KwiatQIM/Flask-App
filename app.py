from flask import Flask, make_response, redirect, request, jsonify, render_template, flash
import matplotlib.pyplot as plt
import numpy as np
from StateDiagnosisApplication import StateDiagnosis
app = Flask(__name__)



# Default home page. This is the page the user first sees when visting the site
@app.route('/')
def index():
    return render_template("FrontPage.html")

# This is function grabs the values from the sliders on the previous page.
@app.route("/test", methods=["POST"])
def test():
    epsilon     = float(request.form["amountInputEps"])
    decoherence = float(request.form["amountInputDco"])
    background  = float(request.form["amountInputBgd"])

    myState = StateDiagnosis(epsilon, decoherence, background)
    concurrence = myState.concurrence()
    daVis = myState.DA_visibility()

    return render_template("ResultPage.html", concurrence=str(concurrence), daVis=str(daVis), concRND = str(round(concurrence,4)), daVisRND = str(round(daVis,4)))




if __name__ == "__main__":
    app.run(debug=True)
