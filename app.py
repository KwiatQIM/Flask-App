from flask import Flask, make_response, redirect, request, jsonify, render_template, flash
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import numpy as np
from StateDiagnosisApplication import StateDiagnosis
app = Flask(__name__)

# default values for the three inputs
# eps = 0.5
# dec = 1
# bac = 0


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
    tograph = '/plot/' + str(epsilon) + '/' + str(decoherence) + '/' + str(background)

    myState = StateDiagnosis(epsilon, decoherence, background)
    concurrence = myState.concurrence()
    daVis = myState.DA_visibility()

    return render_template("ResultPage.html", concRND=str(round(concurrence,4)), daVisRND=str(round(daVis,4)), eps=epsilon, dec=decoherence, bac=background, grph=tograph)


@app.route('/plot/<eps>/<dec>/<bac>')
def plot_everything(eps='0.5', dec='1', bac='0'):
    eps = float(eps)
    dec = float(dec)
    bac = float(bac)
    x = StateDiagnosis(eps, dec, bac)
    concEps, DAEps = x.plot_varyEpsilon()
    concBack, DABack = x.plot_varyBackground()
    concDec, DADec = x.plot_varyDecoherence()
    zero_to_one = np.linspace(0, 1, 100)

    fig = Figure()
    axes1 = fig.add_subplot(3, 3, 1)
    axes1.plot(concEps, DAEps)
    axes1.set_title('Varying\nEpsilon')
    axes1.set_xlabel('Concurrence')
    axes1.set_ylabel('DA visibility')

    axes2 = fig.add_subplot(3,3,2)
    axes2.plot(concDec, DADec)
    axes2.set_title('Varying\nDecoherence')
    axes2.set_xlabel('Concurrence')

    axes3 = fig.add_subplot(3,3,3)
    axes3.plot(concBack, DABack)
    axes3.set_title('Varying\nBackground')
    axes3.set_xlabel('Concurrence')

    axes4 = fig.add_subplot(3,3,4)
    axes4.plot(zero_to_one, DAEps)
    axes4.set_xlabel('Epsilon')
    axes4.set_ylabel('DA visibility')

    axes5 = fig.add_subplot(3,3,5)
    axes5.plot(zero_to_one, DADec)
    axes5.set_xlabel('Decoherence')

    axes6 = fig.add_subplot(3,3,6)
    axes6.plot(zero_to_one, DABack)
    axes6.set_xlabel('Background')

    axes7 = fig.add_subplot(3,3,7)
    axes7.plot(zero_to_one, concEps)
    axes7.set_xlabel('Epsilon')
    axes7.set_ylabel('Concurrence')

    axes8 = fig.add_subplot(3,3,8)
    axes8.plot(zero_to_one, concDec)
    axes8.set_xlabel('Decoherence')

    axes9 = fig.add_subplot(3,3,9)
    axes9.plot(zero_to_one, concBack)
    axes9.set_xlabel('Background')

    fig.tight_layout(pad=1)

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response



if __name__ == "__main__":
    app.run(debug=True)
