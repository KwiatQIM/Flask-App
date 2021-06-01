import numpy as np
import numpy.linalg as la
import QuantumTomography as qlib
import matplotlib.pyplot as plt

# calculates the probability that state 2 will be projected on to state 1
# < state1 | state2 >
def prob_of_proj(state1,state2,normalize=True):

    if np.ndim(state1) == 1:
        state1 = qlib.toDensity(state1)
    elif state1.shape[1] != state1.shape[0]:
        raise ValueError("State1 is not a vector or density matrix")

    if np.ndim(state2) == 1:
        state2 = qlib.toDensity(state2)
    elif state2.shape[1] != state2.shape[0]:
        raise ValueError("State2 is not a vector or density matrix")

    if state2.shape != state1.shape:
        raise ValueError("Input states different dimensions")

    if(normalize):
        state1 = state1 / np.trace(state1)
        state2 = state2 / np.trace(state2)

    return np.trace(state1 @ state2)


# Calculates the visibility in the diagonal basis
def visibility_DA(state):
    # Convert to density matrix if not already
    if(len(state.shape)==1):
        state = qlib.toDensity(state)

    N_DD = prob_of_proj(np.kron([1,1],[1,1]),state,normalize=True)
    N_AA = prob_of_proj(np.kron([1,-1],[1,-1]),state,normalize=True)
    N_AD = prob_of_proj(np.kron([1,-1],[1,1]),state,normalize=True)
    N_DA = prob_of_proj(np.kron([1,1],[1,-1]),state,normalize=True)


    return (N_DD+N_AA-N_AD-N_DA)/(N_DD+N_AA+N_AD+N_DA)



# Setting up psi state
psi_pure = np.array([1,0,0,1])
psi_pure = psi_pure/la.norm(psi_pure)

psi_density = np.outer(psi_pure.conj(),psi_pure)

psi_density = qlib.toDensity(psi_pure)

# Setting up the background state
background_density = np.eye(4)*1/4



# # FIRST SET OF GRAPHS
# #####################
# p_vals = np.linspace(0,1,50)
# concurrence_vals = np.zeros_like(p_vals)
# visibility_DA_vals = np.zeros_like(p_vals)
# for i in range(len(p_vals)):
#     state_density = p_vals[i]*psi_density + (1-p_vals[i]) * background_density
#     if(np.trace(state_density)<.99999):
#         print(0)
#
#     # Concurrence
#     concurrence_vals[i] = qlib.concurrence(state_density)
#
#     # Visibility in Diagonal basis
#     visibility_DA_vals[i] = visibility_DA(state_density)
#
# plt.plot(1-p_vals,concurrence_vals)
# plt.title("Concurrence vs Fraction of Background")
# plt.ylabel("Concurrence")
# plt.ylim((0,1))
# plt.ylim((0,1))
# plt.xlabel("1-p")
# plt.show()
# plt.savefig('ADVR_plots/Conc_vs_background.png')
#
#
# # plt.plot(1-p_vals,visibility_DA_vals)
# # plt.title("D/A Visibility vs Fraction of Background")
# # plt.ylabel("D/A Visibility")
# # plt.ylim((0,1))
# # plt.ylim((0,1))
# # plt.xlabel("1-p")
# # plt.savefig('ADVR_plots/Vis_vs_background.png')
#
# # plt.plot(visibility_DA_vals,concurrence_vals)
# # plt.title("Concurrence vs D/A Visibility")
# # plt.ylabel("Concurrence")
# # plt.ylim((0,1))
# # plt.ylim((0,1))
# # plt.xlabel("D/A Visibility")
# # plt.savefig('ADVR_plots/Conc_vs_Vis.png')
#
# SECOND SET OF GRAPHS
######################


p_vals = np.linspace(0,.5,50)
concurrence_vals = np.zeros_like(p_vals)
visibility_DA_vals = np.zeros_like(p_vals)
decoherence_vals = np.zeros_like(p_vals)
for i in range(len(p_vals)):
    state_density = psi_density.copy()
    state_density[0, 3] = p_vals[i]
    state_density[3, 0] = p_vals[i]

    if(np.trace(state_density)<.99999):
        print(0)

    # Concurrence
    concurrence_vals[i] = qlib.concurrence(state_density)

    # Visibility in Diagonal basis
    visibility_DA_vals[i] = visibility_DA(state_density)
# decoherence Vals
decoherence_vals = p_vals*2
decoherence_sorted, concurrence_sorted = zip(*sorted(zip(decoherence_vals, concurrence_vals)))
decoherence_sorted, visibility_DA_sorted = zip(*sorted(zip(decoherence_vals, visibility_DA_vals)))

plt.plot(decoherence_sorted,concurrence_sorted)
plt.title("Concurrence vs Decoherence")
plt.ylabel("Concurrence")
plt.ylim((0,1))
plt.ylim((0,1))
plt.xlabel("2p|HH><VV|")
plt.show()
# plt.savefig('ADVR_plots/Conc_vs_Decoherence.png')

# plt.plot(decoherence_sorted,visibility_DA_sorted)
# plt.title("D/A Visibility vs Decoherence")
# plt.ylabel("D/A Visibility")
# # plt.ylim((0,1))
# # plt.ylim((0,1))
# plt.xlabel("2p|HH><VV|")
# plt.savefig('ADVR_plots/Vis_vs_Decoherence.png')

plt.plot(visibility_DA_vals,concurrence_vals)
plt.title("Concurrence vs D/A Visibility")
plt.ylabel("Concurrence")
plt.ylim((0,1))
plt.ylim((0,1))
plt.xlabel("D/A Visibility")
plt.savefig('ADVR_plots/Conc_vs_Vis_with_Decoherence.png')


# THIRD SET OF GRAPHS
######################

# Setting up psi state
psi_pure = np.array([1,0,0,1])
psi_pure = psi_pure/la.norm(psi_pure)
psi_density = qlib.toDensity(psi_pure)


theta_vals = np.linspace(0,np.pi/4,50)
concurrence_vals = list()
visibilityDA_vals = list()
epsilon_vals = list()
for theta in theta_vals:
    a = np.cos(theta)
    b = np.sin(theta)
    state_pure = np.array([a,0,0,b])
    state_density = qlib.toDensity(state_pure)

    if(np.trace(state_density)<.99999):
        print(0)
    if (b>a):
        print(0)
    epsilon_vals.append(np.abs(b/a)**2)

    # Concurrence
    concurrence_vals.append(qlib.concurrence(state_density))

    # Visibility in Diagonal basis
    visibilityDA_vals.append(visibility_DA(state_density))

# #
# # epsilon_sorted, concurrence_sorted = zip(*sorted(zip(epsilon_vals, concurrence_vals)))
# # plt.plot(epsilon_sorted,concurrence_sorted)
# # plt.title("Concurrence vs Term Imbalance")
# # plt.ylabel("Concurrence")
# # plt.ylim((0,1))
# # plt.ylim((0,1))
# # plt.xlabel(r'$\epsilon$')
# # plt.savefig('ADVR_plots/Conc_vs_Imbalance.png')
#
#
# epsilon_sorted, visibilityDA_sorted = zip(*sorted(zip(epsilon_vals, visibilityDA_vals)))
# plt.plot(epsilon_sorted,visibilityDA_sorted)
# plt.title("D/A Visibility vs Term Imbalance")
# plt.ylabel("D/A Visibility")
# # plt.ylim((0,1))
# # plt.ylim((0,1))
# plt.xlabel(r'$\epsilon$')
# plt.savefig('ADVR_plots/Vis_vs_Imbalance.png')