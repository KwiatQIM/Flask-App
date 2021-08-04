import qutip
import QuantumTomography as qlib
import numpy as np
import matplotlib.pyplot as plt




colors = ['#6900D1', '#2D00D1', '#0040D1', '#00A4D1', '#00D1AB', '#00D169', '#00D104', '#6FD100', '#D1D100', '#D18B00', '#D13300']
purple = ['#663399']
blue = ['#001DD1']
green = ['#00D126']

three_colors = 202*purple + 202*blue + 202*green

gates = {
    'X': np.array([[0, 1], [1, 0]], dtype=complex),
    'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
    'Z': np.array([[1, 0], [0, 1]], dtype=complex),
    'H': (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex),
    'S': np.array([[1, 0],[0, np.cos(np.pi / 2) + 1j*np.sin(np.pi / 2)]], dtype=complex),
    'St': np.array([[1, 0],[0, np.cos(-1*np.pi / 2) + 1j*np.sin(-1*np.pi / 2)]], dtype=complex),
    'T': np.array([[1, 0],[0, np.cos(np.pi / 4) + 1j*np.sin(np.pi / 4)]], dtype=complex),
    'Tt': np.array([[1, 0],[0, np.cos(-1*np.pi / 4) + 1j*np.sin(-1*np.pi / 4)]], dtype=complex)
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

def get_sphere(type):
    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(projection='3d'))

    sphere = qutip.Bloch(fig=fig, axes=ax)
    sphere.point_color = three_colors
    sphere.point_marker = ['o']
    sphere.point_size = [55]
    sphere.view = [-67, 12]
    if type == 'poincare':
        sphere.xlabel = ['$\\left|H\\right>$', '$\\left|V\\right>$']
        sphere.ylabel = ['$\\left|D\\right>$', '$\\left|A\\right>$']
        sphere.zlabel = ['$\\left|R\\right>$', '$\\left|L\\right>$']
    elif type == 'bloch':
        sphere.xlabel = ['$x$', '']
        sphere.ylabel = ['$y$', '']
        sphere.zlabel = ['$\\left|1\\right>$', '$\\left|0\\right>$']

    return sphere, fig, ax

"""Returns a blank bloch sphere matplotlib figure"""
def blank_bloch(type):
    sphere, fig, ax = get_sphere(type)
    sphere.render(fig=fig, axes=ax)
    return fig

"""Given a state, and a list of gates, returns a figure with the corresponding bloch sphere plot of the transformation"""
def bloch_sphere(type, state, input_gates):
        if state in states.keys():
            state = states[state]
        elif state.count('=') == 1:
            state_elements = state.split('=')
            for i in range(len(state_elements)):
                if 'j' in state_elements[i]:
                    state_elements[i] = complex(state_elements[i].replace(" ", "").replace("+-", "-"))
                elif 'i' in state_elements[i]:
                    state_elements[i] = complex(state_elements[i].replace("i","j").replace(" ", "").replace("+-", "-"))
                else:
                    state_elements[i] = float(state_elements[i])
            state = np.zeros(2, dtype=complex)
            state[0] += state_elements[0]
            state[1] += state_elements[1]

        gates_list = []
        for gate in input_gates:
            if gate in gates.keys():
                gates_list.append(gates[gate])
            elif gate.count('=') == 3:
                elements = gate.split('=')
                for i in range(len(elements)):
                    if 'j' in elements[i]:
                        elements[i] = complex(elements[i].replace(" ", "").replace("+-", "-"))
                    elif 'i' in elements[i]:
                        elements[i] = complex(elements[i].replace("i", "j").replace(" ", "").replace("+-", "-"))
                    else:
                        elements[i] = float(elements[i])
                gate = np.array([[elements[0], elements[1]],[elements[2], elements[3]]], dtype=complex)
                gates_list.append(gate)


        sphere, fig, ax = get_sphere(type)

        points = [[], [], []]
        for gate in gates_list:
            state, current_points = gate_points(type, state, gate)
            points[0].extend(current_points[0])
            points[1].extend(current_points[1])
            points[2].extend(current_points[2])

        sphere.add_points(points, 'm')

        sphere.render(fig=fig, axes=ax)


        return fig

"""Returns a list of the lists of coordinates for a given state going through a given gate"""
def gate_points(type, state, gate):
    if state.shape != (2,):
        raise ValueError('Input must be a pure state vector (numpy array with 2 elements)')
    if gate.shape != (2, 2):
        raise ValueError('Gate must be 2x2 matrix')

    post_gate_state = gate @ state

    # to the points that make the lines around which to rotate
    eigvals, eigvectors = np.linalg.eig(gate)
    eig_point = []
    direction = []

    eig_point = stokes(type, eigvectors[:,0])
    direction = normalize([stokes(type, eigvectors[:,1])[i] - eig_point[i] for i in range(len(eig_point))])

    stokes_before = normalize(stokes(type, state))
    stokes_after = normalize(stokes(type, post_gate_state))

    # rotating (x, y, z) around line with point (a, b, c) and direction (u, v, w)
    (x, y, z) = stokes_before
    (x2, y2, z2) = stokes_after
    (a, b, c) = eig_point
    (u, v, w) = direction


    A_matrix = np.array([[x - (a*(v**2 + w**2) - u*(b*v + c*w - u*x - v*y - w*z)), -1*c*v + b*w - w*y + v*z],
                         [y - (b*(u**2 + w**2) - v*(a*u + c*w - u*x - v*y - w*z)), c*u - a*w + w*x - u*z],
                         [z - (c*(u**2 + v**2) - w*(a*u + b*v - u*x - v*y - w*z)), -1*b*u + a*v - v*x + u*y]])

    B_vector = np.array([x2 - (a*(v**2 + w**2) - u*(b*v + c*w - u*x - v*y - w*z)),
                         y2 - (b*(u**2 + w**2) - v*(a*u + c*w - u*x - v*y - w*z)),
                         z2 - (c*(u**2 + v**2) - w*(a*u + b*v - u*x - v*y - w*z))])

    cos_sin_theta = np.linalg.lstsq(A_matrix, B_vector)[0]
    theta = -1*np.arccos(min(max(cos_sin_theta[0], -1), 1))

    n_steps = 200

    points = [stokes_before]
    for i in range(n_steps):
        prop = i / n_steps
        thet = theta * prop
        current_point = [(a*(v**2 + w**2) - u*(b*v + c*w - u*x - v*y - w*z))*(1 - np.cos(thet)) + x*np.cos(thet) + (-1*c*v + v*w - w*y + v*z)*np.sin(thet),
                         (b*(u**2 + w**2) - v*(a*u + c*w - u*x - v*y - w*z))*(1 - np.cos(thet)) + y*np.cos(thet) + (c*u - a*w + w*x - u*z)*np.sin(thet),
                         (c*(u**2 + v**2) - w*(a*u + b*v - u*x - v*y - w*z))*(1 - np.cos(thet)) + z*np.cos(thet) + (-1*b*u + a*v - v*x + u*y)*np.sin(thet)]

        original_distance = np.sqrt((x - x2)**2 + (y - y2)**2 + (z - z2)**2)
        current_distance = np.sqrt((current_point[0] - x2)**2 + (current_point[1] - y2)**2 + (current_point[2] - z2)**2)

        # basically, if the current point is further from the original point then the angle is the opposite of what you want
        if current_distance > original_distance:
            current_point = [(a*(v**2 + w**2) - u*(b*v + c*w - u*x - v*y - w*z))*(1 - np.cos(-1*thet)) + x*np.cos(-1*thet) + (-1*c*v + v*w - w*y + v*z)*np.sin(-1*thet),
                         (b*(u**2 + w**2) - v*(a*u + c*w - u*x - v*y - w*z))*(1 - np.cos(-1*thet)) + y*np.cos(-1*thet) + (c*u - a*w + w*x - u*z)*np.sin(-1*thet),
                         (c*(u**2 + v**2) - w*(a*u + b*v - u*x - v*y - w*z))*(1 - np.cos(-1*thet)) + z*np.cos(-1*thet) + (-1*b*u + a*v - v*x + u*y)*np.sin(-1*thet)]
            theta *= -1


        points.append(current_point)



    points.append(stokes_after)
    points = coords(points)
    return post_gate_state, points

"""Returns the stokes parameters (bloch sphere coordinates) of a pure state input"""
def stokes(type, pure_state):
    if len(pure_state) != 2:
        raise ValueError('pure state must have two elements')
    rho = qlib.toDensity(pure_state)

    da = np.trace(paulis[1] @ rho).real
    rl = np.trace(paulis[2] @ rho).real
    hv = np.trace(paulis[3] @ rho).real

    if type == 'poincare':
        return [hv, da, rl]
    elif type == 'bloch':
        return [da, rl, hv]

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


# b = bloch_sphere('H', ['1=1=1=1'])
# plt.show()