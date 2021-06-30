from flask import Flask, make_response, request, render_template
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import numpy as np
from StateDiagnosisApplication import StateDiagnosis
from createDocumentation import create_page

app = Flask(__name__)

# NOTE: in this code, epsilon refers to Term Imbalance

# Default home page. This is the page the user first sees when visiting the site
@app.route('/')
def index():
    return render_template('FrontPage.html')

# Default home page. This is the page the user first sees when visiting the site
@app.route('/stateCharacterization')
def state_characterization():
    epsilon = 1
    decoherence = 1
    background = 0
    myState = StateDiagnosis(epsilon, decoherence, background)
    daVis = myState.DA_visibility()
    concurrence = myState.concurrence()
    tograph = f'/plot/{epsilon}/{decoherence}/{background}'
    return render_template("stateCharacterization.html", concRND=str(round(concurrence,4)), daVisRND=str(round(daVis,4)), eps=epsilon, dec=decoherence, bac=background, grph=tograph)


# This is function grabs the values from the sliders on the previous page.
@app.route("/stateCharacterizationResults", methods=["POST"])
def state_characterization_results():
    epsilon = float(request.form["amountInputEps"])
    decoherence = float(request.form["amountInputDco"])
    background = float(request.form["amountInputBgd"])

    tograph = f'/plot/{epsilon}/{decoherence}/{background}'

    myState = StateDiagnosis(epsilon, decoherence, background)
    concurrence = myState.concurrence()
    daVis = myState.DA_visibility()

    return render_template("stateCharacterizationResults.html", concRND=str(round(concurrence,4)), daVisRND=str(round(daVis,4)), eps=epsilon, dec=decoherence, bac=background, grph=tograph)


TomoClassFunctions, TomoFunctionsFunctions, TomoDisplayFunctions, functions, \
    titles, function_parameters, descriptions, param_bools, return_bools, param_dicts, return_dicts, see_also, count = create_page()
# Route for documentation page
@app.route("/Doc/")
@app.route("/Doc/<display>")
def displayDocumentationPage(display='Tomography'):

    return render_template("DocumentationPage.html", disp=display, TomoClassFunctions=TomoClassFunctions,
                           TomoFunctionsFunctions=TomoFunctionsFunctions, TomoDisplayFunctions=TomoDisplayFunctions,
                           functions=functions, titles=titles, function_parameters=function_parameters,
                           descriptions=descriptions, param_bools=param_bools, return_bools=return_bools,
                           param_dicts=param_dicts, return_dicts=return_dicts, see_also=see_also, count=count)


@app.route("/Algorithm/")
@app.route("/Algorithm/<function>")
def displayAlgorithmPage(function="StateTomography"):
    todisplay = f'algorithm_pages/wiki_{function}.html'
    return render_template(todisplay, function=function)


@app.route("/performance/")
def performance():
    return render_template('performance.html')


# Function that creates a page with only the 9 subplots on it.
@app.route('/plot/<eps>/<dec>/<bac>')
def plot_everything(eps='1', dec='1', bac='0'):
    eps = float(eps)
    dec = float(dec)
    bac = float(bac)

    x = StateDiagnosis(eps, dec, bac)

    fig = x.plot_everything()

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response



if __name__ == "__main__":
    app.run(debug=True)
