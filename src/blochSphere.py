import qutip
import QuantumTomography as qlib
import numpy as np


class blochSphere:
    def __init__(self):
        self.colors = ['#6900D1', '#2D00D1', '#0040D1', '#00A4D1', '#00D1AB', '#00D169', '#00D104', '#6FD100', '#D1D100', '#D18B00', '#D13300']
        self.sphere = qutip.Bloch()
        self.sphere.xlabel = ['$\\left|H\\right>$', '$\\left|V\\right>$']
        self.sphere.ylabel = ['$\\left|D\\right>$', '$\\left|A\\right>$']
        self.sphere.zlabel = ['$\\left|R\\right>$', '$\\left|L\\right>$']
        self.sphere.point_color = self.colors

        self.gates = {
            'X': np.array([[0, 1], [1, 0]], dtype=complex),
            'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
            'Z': np.array([[1, 0], [0, 1]], dtype=complex),
            'H': (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
        }

        self.paulis = {
            0: np.array([[1, 0], [0, 1]], dtype=complex),
            1: np.array([[0, 1], [1, 0]], dtype=complex),
            2: np.array([[0, -1j], [1j, 0]], dtype=complex),
            3: np.array([[1, 0], [0, -1]], dtype=complex)
        }

        # HV is X axis, H positive
        # DA is Y axis, A positive
        # LR is Z axis, R positive
        self.states = {
            'H': np.array([1, 0], dtype=complex),
            'V': np.array([0, 1], dtype=complex),
            'D': (1 / np.sqrt(2)) * np.array([1, 1], dtype=complex),
            'A': (1 / np.sqrt(2)) * np.array([1, -1], dtype=complex),
            'R': (1 / np.sqrt(2)) * np.array([1, 1j], dtype=complex),
            'L': (1 / np.sqrt(2)) * np.array([1, -1j], dtype=complex)
        }

    def get_Sphere(self):
        return self.sphere

    def gate(self, state, gate):
        if state in self.states.keys():
            state = self.states[state]
        elif state.shape != (2,):
            raise ValueError(
                "Input must be a pure state vector (numpy array with 2 elements) or one of the following: 'H' 'V' 'D' 'A' 'R' 'L'")

        if gate in self.gates.keys():
            gate = self.gates[gate]
        elif gate.shape != (2, 2):
            raise ValueError("Gate must be 2x2 matrix or one of the following: 'X' 'Y' 'Z' 'H'")

        points = self.gate_points(state, gate)

        self.sphere.add_points(points, 'm')

        return self.sphere

    def gate_points(self, state, gate):
        if state.shape != (2,):
            raise ValueError('Input must be a pure state vector (numpy array with 2 elements)')
        if gate.shape != (2, 2):
            raise ValueError('Gate must be 2x2 matrix')

        post_gate_state = gate @ state

        stokes_before = self.normalize(self.stokes(state))
        stokes_after = self.normalize(self.stokes(post_gate_state))
        difference = [stokes_after[i] - stokes_before[i] for i in range(len(stokes_before))]

        nsteps = 10
        difference_steps = [diff / nsteps for diff in difference]

        points = [stokes_before]

        for i in range(nsteps):
            step_number = i + 1
            step = [step_number * element for element in difference_steps]
            current_point = [stokes_before[i] + step[i] for i in range(len(step))]
            points.append(current_point)

        points = self.coords(points)
        return points

    def stokes(self, pure_state):
        if len(pure_state) != 2:
            raise ValueError('pure state must have two elements')
        rho = qlib.toDensity(pure_state)

        da = np.trace(self.paulis[1] @ rho).real
        rl = np.trace(self.paulis[2] @ rho).real
        hv = np.trace(self.paulis[3] @ rho).real

        return [hv, da, rl]

    def coords(self, args):
        h = []
        d = []
        r = []
        for arg in args:
            h.append(arg[0])
            d.append(arg[1])
            r.append(arg[2])
        return [h, d, r]

    def normalize(self, stokes):
        magnitude = 0
        normalized_stokes = []

        for parameter in stokes:
            magnitude += parameter ** 2

        magnitude = np.sqrt(magnitude)

        for parameter in stokes:
            normalized_stokes.append(parameter / magnitude)

        return normalized_stokes

