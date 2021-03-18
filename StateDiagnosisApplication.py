import numpy as np
import QuantumTomography as qlib

class StateDiagnosis:
    def __init__(self, epsilon, decoherence, background):
        self.epsilon = epsilon
        self.decoherence = decoherence
        self.background = background

        self.background_density = 1 / 4 * np.eye(4)
        self.StateDensity = StateDensity = np.array([[1 / (1 + self.epsilon), 0, 0, self.decoherence * np.sqrt(self.epsilon) / (1 + self.epsilon)] \
                                                        , [0, 0, 0, 0], [0, 0, 0, 0], [self.decoherence * np.sqrt(self.epsilon) / (1 + self.epsilon), 0, 0, self.epsilon / (1 + self.epsilon)]])
        self.finalStateDensity = (1-self.background)*(self.StateDensity) + self.background*(self.background_density)

    def DA_visibility(self):
        def proj(state1, state2, normalize=True):

            # converting the states to density matrices if they are given as pure states.
            if (state1.ndim == 1):
                dstate1 = qlib.toDensity(state1)
            else:
                dstate1 = state1

            if (state2.ndim == 1):
                dstate2 = qlib.toDensity(state2)
            else:
                dstate2 = state2

            # normalizing the states if specified
            if (normalize):
                dstate1 = dstate1 / np.trace(dstate1)
                dstate2 = dstate2 / np.trace(dstate2)

            # returning the projection
            return np.trace(dstate1 @ dstate2)

        N_DD = proj(np.kron([1, 1], [1, 1]), self.finalStateDensity, normalize=True)
        N_AA = proj(np.kron([1, -1], [1, -1]), self.finalStateDensity, normalize=True)
        N_AD = proj(np.kron([1, -1], [1, 1]), self.finalStateDensity, normalize=True)
        N_DA = proj(np.kron([1, 1], [1, -1]), self.finalStateDensity, normalize=True)

        return ((N_DD + N_AA - N_AD - N_DA) / (N_DD + N_AA + N_DA + N_AD))

    def concurrence(self):
        return qlib.concurrence(self.finalStateDensity)