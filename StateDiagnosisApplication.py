import numpy as np
import QuantumTomography as qlib


# test
class StateDiagnosis:
    def __init__(self, epsilon, decoherence, background):
        self.epsilon = epsilon
        self.decoherence = decoherence
        self.background = background

        self.background_density = 1 / 4 * np.eye(4)
        self.StateDensity = StateDensity = np.array(
                [[1 / (1 + self.epsilon), 0, 0, self.decoherence * np.sqrt(self.epsilon) / (1 + self.epsilon)]
                    , [0, 0, 0, 0], [0, 0, 0, 0], [self.decoherence * np.sqrt(self.epsilon) / (1 + self.epsilon), 0, 0,
                                                   self.epsilon / (1 + self.epsilon)]])

        self.finalStateDensity = (1-self.background)*self.StateDensity + self.background*self.background_density

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
            if normalize:
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

    def plot_varyEpsilon(self):
        # setting up the imbalance vector to be used in calculations
        eps_vec = np.linspace(0, 1, 100)
        concVec = np.zeros_like(eps_vec)
        DAVec = np.zeros_like(eps_vec)

        for i in range(len(eps_vec)):
            diagnosis = StateDiagnosis(eps_vec[i], self.decoherence, self.background)
            concVec[i] = diagnosis.concurrence()
            DAVec[i] = diagnosis.DA_visibility()

        # returns the concurrence and DA visibility vectors when you vary the IMBALANCE
        return concVec, DAVec

    def plot_varyBackground(self):
        # setting up background proportion vector to be varied
        bkg_vec = np.linspace(0, 1, 100)
        concVec = np.zeros_like(bkg_vec)
        DAVec = np.zeros_like(bkg_vec)

        for i in range(len(bkg_vec)):
            diagnosis = StateDiagnosis(self.epsilon, self.decoherence, bkg_vec[i])
            concVec[i] = diagnosis.concurrence()
            DAVec[i] = diagnosis.DA_visibility()

        # returns the concurrence and DA visibility vectors when varying BACKGROUND PROPORTION
        return concVec, DAVec

    def plot_varyDecoherence(self):
        # setting up the decoherence vector to be varied
        dec_vec = np.linspace(0, 1, 100)
        concVec = np.zeros_like(dec_vec)
        DAVec = np.zeros_like(dec_vec)

        for i in range(len(dec_vec)):
            diagnosis = StateDiagnosis(self.epsilon, dec_vec[i], self.background)
            concVec[i] = diagnosis.concurrence()
            DAVec[i] = diagnosis.DA_visibility()

        # returns the concurrence and DA visibility vectors when varying DECOHERENCE
        return concVec, DAVec