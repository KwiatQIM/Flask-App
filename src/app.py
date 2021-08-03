from flask import Flask, make_response, request, render_template
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import numpy as np
from StateDiagnosisApplication import StateDiagnosis
from blochSphere import *
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


@app.route('/singleQubitVisuals', methods=["GET", "POST"])
def singleQubitVisuals():
    if request.method == "POST":
        state = str(request.form["state_selection"])
        if state == 'custom':
            a_coef = request.form['custom_state_a']
            b_coef = request.form['custom_state_b']
            state = f'{a_coef}={b_coef}'
            state_todisplay = state.split("=")
        else:
            state_todisplay = [0, 0]


        gate1 = request.form["gate_1_selection"]
        if gate1 == 'custom':
            gate1_elements = [request.form['gate1_element1'].strip(), request.form['gate1_element2'].strip(),
                              request.form['gate1_element3'].strip(), request.form['gate1_element4'].strip()]
            gate1 = f'{gate1_elements[0]}={gate1_elements[1]}={gate1_elements[2]}={gate1_elements[3]}'
            gate1_todisplay = gate1.split('=')
        elif gate1 == 'P':
            gate1 = pgate(float(request.form['pgate1_angle'])* (3.1415926535897 / 180))
            gate1_todisplay = [float(request.form['pgate1_angle'])]
        else:
            gate1_todisplay = 0


        gate2 = request.form["gate_2_selection"]
        if gate2 == 'custom':
            gate2_elements = [request.form['gate2_element1'].strip(), request.form['gate2_element2'].strip(),
                              request.form['gate2_element3'].strip(), request.form['gate2_element4'].strip()]
            gate2 = f'{gate2_elements[0]}={gate2_elements[1]}={gate2_elements[2]}={gate2_elements[3]}'
            gate2_todisplay = gate2.split('=')
        elif gate2 == 'P':
            gate2 = pgate(float(request.form['pgate2_angle']) * (3.1415926535897 / 180))
            gate2_todisplay = [float(request.form['pgate2_angle'])]
        else:
            gate2_todisplay = 0

        gate3 = request.form["gate_3_selection"]
        if gate3 == 'custom':
            gate3_elements = [request.form['gate3_element1'].strip(), request.form['gate3_element2'].strip(),
                              request.form['gate3_element3'].strip(), request.form['gate3_element4'].strip()]
            gate3 = f'{gate3_elements[0]}={gate3_elements[1]}={gate3_elements[2]}={gate3_elements[3]}'
            gate3_todisplay = gate3.split('=')
        elif gate3 == 'P':
            gate3 = pgate(float(request.form['pgate3_angle'])* (3.1415926535897 / 180))
            gate3_todisplay = [float(request.form['pgate3_angle'])]
        else:
            gate3_todisplay = 0

        gates = f'{gate1}_{gate2}_{gate3}'
        sphere_path = f'/bloch/{state}/{gates}'
        return render_template("singleQubitVisuals.html", sphere_path=sphere_path, state_to_select=request.form["state_selection"], gate_1_to_select=request.form["gate_1_selection"]
                               , gate_2_to_select=request.form["gate_2_selection"], gate_3_to_select=request.form["gate_3_selection"],
                               dispstate=state_todisplay, dispgate1=gate1_todisplay, dispgate2=gate2_todisplay, dispgate3=gate3_todisplay)
    else:
        sphere_path = '/bloch/0/0'
        return render_template("singleQubitVisuals.html", sphere_path=sphere_path, state_to_select='H', gate_to_select='X',
                               dispstate=[0,0], dispgate1=[0,0,0,0], dispgate2=[0,0,0,0], dispgate3=[0,0,0,0])


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

@app.route('/bloch/<state>/<gates>')
def bloch(state='H', gates='X'):
    if state == '0' and gates == '0':
        fig = blank_bloch()
    else:
        gates_used = []
        for gate in gates.split('_'):
            if gate != '0':
                gates_used.append(gate)
        fig = bloch_sphere(state, gates_used)

    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response


if __name__ == "__main__":
    app.run(debug=True)
