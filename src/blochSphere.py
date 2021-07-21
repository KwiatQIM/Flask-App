import qutip
import QuantumTomography as qlib
import numpy as np
import matplotlib.pyplot as plt




colors = ['#6900D1', '#2D00D1', '#0040D1', '#00A4D1', '#00D1AB', '#00D169', '#00D104', '#6FD100', '#D1D100', '#D18B00', '#D13300']
purple = ['#663399']



gates = {
    'X': np.array([[0, 1], [1, 0]], dtype=complex),
    'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
    'Z': np.array([[1, 0], [0, 1]], dtype=complex),
    'H': (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
}

paulis = {
    0: np.array([[1, 0], [0, 1]], dtype=complex),
    1: np.array([[0, 1], [1, 0]], dtype=complex),
    2: np.array([[0, -1j], [1j, 0]], dtype=complex),
    3: np.array([[1, 0], [0, -1]], dtype=complex)
}

        # HV is X axis, H positive
        # DA is Y axis, A positive
        # LR is Z axis, R positive
states = {
    'H': np.array([1, 0], dtype=complex),
    'V': np.array([0, 1], dtype=complex),
    'D': (1 / np.sqrt(2)) * np.array([1, 1], dtype=complex),
    'A': (1 / np.sqrt(2)) * np.array([1, -1], dtype=complex),
    'R': (1 / np.sqrt(2)) * np.array([1, 1j], dtype=complex),
    'L': (1 / np.sqrt(2)) * np.array([1, -1j], dtype=complex)
}

def get_sphere():
    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(projection='3d'))

    sphere = qutip.Bloch(fig=fig, axes=ax)
    sphere.point_color = purple
    sphere.xlabel = ['$\\left|H\\right>$', '$\\left|V\\right>$']
    sphere.ylabel = ['$\\left|D\\right>$', '$\\left|A\\right>$']
    sphere.zlabel = ['$\\left|R\\right>$', '$\\left|L\\right>$']

    return sphere, fig, ax

"""Returns a blank bloch sphere matplotlib figure"""
def blank_bloch():
    sphere, fig, ax = get_sphere()
    sphere.render(fig=fig, axes=ax)
    return fig

"""Given a state, and a list of gates, returns a figure with the corresponding bloch sphere plot of the transformation"""
def bloch_sphere(state, input_gates):
        if state in states.keys():
            state = states[state]
        elif state.shape != (2,):
            raise ValueError(
                "Input must be a pure state vector (numpy array with 2 elements) or one of the following: 'H' 'V' 'D' 'A' 'R' 'L'")

        gates_list = []
        for gate in input_gates:
            if gate in gates.keys():
                gates_list.append(gates[gate])
            elif gate.count('=') == 3:
                elements = gate.split('=')
                for i in range(len(elements)):
                    if 'j' in elements[i]:
                        elements[i] = complex(elements[i].replace(" ", ""))
                    elif 'i' in elements[i]:
                        elements[i] = complex(elements[i].replace("i", "j").replace(" ", ""))
                    else:
                        elements[i] = float(elements[i])
                gate = np.array([[elements[0], elements[1]],[elements[2], elements[3]]], dtype=complex)
                gates_list.append(gate)


        sphere, fig, ax = get_sphere()

        points = [[], [], []]
        for gate in gates_list:
            state, current_points = gate_points(state, gate)
            points[0].extend(current_points[0])
            points[1].extend(current_points[1])
            points[2].extend(current_points[2])

        sphere.add_points(points, 'm')

        sphere.render(fig=fig, axes=ax)


        return fig

"""Returns a list of the lists of coordinates for a given state going through a given gate"""
def gate_points(state, gate):
    if state.shape != (2,):
        raise ValueError('Input must be a pure state vector (numpy array with 2 elements)')
    if gate.shape != (2, 2):
        raise ValueError('Gate must be 2x2 matrix')

    post_gate_state = gate @ state

    stokes_before = normalize(stokes(state))
    stokes_after = normalize(stokes(post_gate_state))
    difference = [stokes_after[i] - stokes_before[i] for i in range(len(stokes_before))]

    nsteps = 100
    difference_steps = [diff / nsteps for diff in difference]

    points = [stokes_before]

    for i in range(nsteps):
        step_number = i + 1
        step = [step_number * element for element in difference_steps]
        current_point = [stokes_before[i] + step[i] for i in range(len(step))]
        points.append(current_point)

    points = coords(points)
    return post_gate_state, points

"""Returns the stokes parameters (bloch sphere coordinates) of a pure state input"""
def stokes(pure_state):
    if len(pure_state) != 2:
        raise ValueError('pure state must have two elements')
    rho = qlib.toDensity(pure_state)

    da = np.trace(paulis[1] @ rho).real
    rl = np.trace(paulis[2] @ rho).real
    hv = np.trace(paulis[3] @ rho).real

    return [hv, da, rl]

"""This changes a list of different points into a list containing three lists corresponding to the three stokes coordinates"""
def coords(args):
    h = []
    d = []
    r = []
    for arg in args:
        h.append(arg[0])
        d.append(arg[1])
        r.append(arg[2])
    return [h, d, r]

"""Normalizes a point within the sphere to the closest point on the outside of the sphere"""
def normalize(stokes):
    magnitude = 0
    normalized_stokes = []

    for parameter in stokes:
        magnitude += parameter ** 2

    magnitude = np.sqrt(magnitude)

    for parameter in stokes:
        normalized_stokes.append(parameter / magnitude)

    return normalized_stokes

def pgate(phi):
    gate = ['1', '0', '0', f'{round(np.cos(phi), 5)}+{round(np.sin(phi), 5)}j']
    return '='.join(gate)

# b = bloch_sphere('H', ['1-1-1-1', '0', '0'])
# plt.show()