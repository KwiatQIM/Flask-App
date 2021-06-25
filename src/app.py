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
    tograph = '/plot/' + str(epsilon) + '/' + str(decoherence) + '/' + str(background)
    return render_template("stateCharacterization.html", concRND=str(round(concurrence,4)), daVisRND=str(round(daVis,4)), eps=epsilon, dec=decoherence, bac=background, grph=tograph)


# This is function grabs the values from the sliders on the previous page.
@app.route("/stateCharacterizationResults", methods=["POST"])
def state_characterization_results():
    epsilon = float(request.form["amountInputEps"])
    decoherence = float(request.form["amountInputDco"])
    background = float(request.form["amountInputBgd"])



    tograph = '/plot/' + str(epsilon) + '/' + str(decoherence) + '/' + str(background)

    myState = StateDiagnosis(epsilon, decoherence, background)
    concurrence = myState.concurrence()
    daVis = myState.DA_visibility()

    return render_template("stateCharacterizationResults.html", concRND=str(round(concurrence,4)), daVisRND=str(round(daVis,4)), eps=epsilon, dec=decoherence, bac=background, grph=tograph)


# Function that creates a page with only the 9 subplots on it.
@app.route('/plot/<eps>/<dec>/<bac>')
def plot_everything(eps='1', dec='1', bac='0'):
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
    axes1.plot(concEps, DAEps, color='#663399')
    axes1.set_title('Varying\nImbalance')
    axes1.set_xlabel('Concurrence')
    axes1.set_ylabel('DA visibility')
    axes1.set_xlim([0,1])
    axes1.set_ylim([0,1])

    axes2 = fig.add_subplot(3,3,2)
    axes2.plot(concDec, DADec, color='#663399')
    axes2.set_title('Varying\nDecoherence')
    axes2.set_xlabel('Concurrence')
    axes2.set_xlim([0, 1])
    axes2.set_ylim([0, 1])

    axes3 = fig.add_subplot(3,3,3)
    axes3.plot(concBack, DABack, color='#663399')
    axes3.set_title('Varying\nBackground')
    axes3.set_xlabel('Concurrence')
    axes3.set_xlim([0, 1])
    axes3.set_ylim([0, 1])

    axes4 = fig.add_subplot(3,3,4)
    axes4.plot(zero_to_one, DAEps, color='#663399')
    axes4.set_xlabel('Imbalance')
    axes4.set_ylabel('DA visibility')
    axes4.set_xlim([0, 1])
    axes4.set_ylim([0, 1])

    axes5 = fig.add_subplot(3,3,5)
    axes5.plot(zero_to_one, DADec, color='#663399')
    axes5.set_xlabel('Decoherence')
    axes5.set_xlim([0, 1])
    axes5.set_ylim([0, 1])

    axes6 = fig.add_subplot(3,3,6)
    axes6.plot(zero_to_one, DABack, color='#663399')
    axes6.set_xlabel('Background')
    axes6.set_xlim([0, 1])
    axes6.set_ylim([0, 1])

    axes7 = fig.add_subplot(3,3,7)
    axes7.plot(zero_to_one, concEps, color='#663399')
    axes7.set_xlabel('Imbalance')
    axes7.set_ylabel('Concurrence')
    axes7.set_xlim([0, 1])
    axes7.set_ylim([0, 1])

    axes8 = fig.add_subplot(3,3,8)
    axes8.plot(zero_to_one, concDec, color='#663399')
    axes8.set_xlabel('Decoherence')
    axes8.set_xlim([0, 1])
    axes8.set_ylim([0, 1])

    axes9 = fig.add_subplot(3,3,9)
    axes9.plot(zero_to_one, concBack, color='#663399')
    axes9.set_xlabel('Background')
    axes9.set_xlim([0, 1])
    axes9.set_ylim([0, 1])

    fig.tight_layout(pad=1)

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


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
    todisplay = 'algorithm_pages/wiki_' + function + '.html'
    return render_template(todisplay, function=function)

@app.route("/performance/")
def performance():
    return render_template('performance.html')


if __name__ == "__main__":
    app.run(debug=True)
