import numpy as np
import QuantumTomography as qlib
from matplotlib.figure import Figure


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

    def plot_everything(self):
        concEps, DAEps = self.plot_varyEpsilon()
        concBack, DABack = self.plot_varyBackground()
        concDec, DADec = self.plot_varyDecoherence()
        zero_to_one = np.linspace(0, 1, 100)

        fig = Figure()
        axes1 = fig.add_subplot(3, 3, 1)
        axes1.plot(concEps, DAEps, color='#663399')
        axes1.set_title('Varying\nImbalance')
        axes1.set_xlabel('Concurrence')
        axes1.set_ylabel('DA visibility')
        axes1.set_xlim([0, 1])
        axes1.set_ylim([0, 1])

        axes2 = fig.add_subplot(3, 3, 2)
        axes2.plot(concDec, DADec, color='#663399')
        axes2.set_title('Varying\nDecoherence')
        axes2.set_xlabel('Concurrence')
        axes2.set_xlim([0, 1])
        axes2.set_ylim([0, 1])

        axes3 = fig.add_subplot(3, 3, 3)
        axes3.plot(concBack, DABack, color='#663399')
        axes3.set_title('Varying\nBackground')
        axes3.set_xlabel('Concurrence')
        axes3.set_xlim([0, 1])
        axes3.set_ylim([0, 1])

        axes4 = fig.add_subplot(3, 3, 4)
        axes4.plot(zero_to_one, DAEps, color='#663399')
        axes4.set_xlabel('Imbalance')
        axes4.set_ylabel('DA visibility')
        axes4.set_xlim([0, 1])
        axes4.set_ylim([0, 1])

        axes5 = fig.add_subplot(3, 3, 5)
        axes5.plot(zero_to_one, DADec, color='#663399')
        axes5.set_xlabel('Decoherence')
        axes5.set_xlim([0, 1])
        axes5.set_ylim([0, 1])

        axes6 = fig.add_subplot(3, 3, 6)
        axes6.plot(zero_to_one, DABack, color='#663399')
        axes6.set_xlabel('Background')
        axes6.set_xlim([0, 1])
        axes6.set_ylim([0, 1])

        axes7 = fig.add_subplot(3, 3, 7)
        axes7.plot(zero_to_one, concEps, color='#663399')
        axes7.set_xlabel('Imbalance')
        axes7.set_ylabel('Concurrence')
        axes7.set_xlim([0, 1])
        axes7.set_ylim([0, 1])

        axes8 = fig.add_subplot(3, 3, 8)
        axes8.plot(zero_to_one, concDec, color='#663399')
        axes8.set_xlabel('Decoherence')
        axes8.set_xlim([0, 1])
        axes8.set_ylim([0, 1])

        axes9 = fig.add_subplot(3, 3, 9)
        axes9.plot(zero_to_one, concBack, color='#663399')
        axes9.set_xlabel('Background')
        axes9.set_xlim([0, 1])
        axes9.set_ylim([0, 1])

        fig.tight_layout(pad=1)

        return fig