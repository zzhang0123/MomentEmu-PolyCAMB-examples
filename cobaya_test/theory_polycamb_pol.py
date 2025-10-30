
import sys
import os
from MomentEmu import *
import numpy as np
from cobaya.theory import Theory
import pickle

# from cobaya.theories._base_classes import Theory


class PolyCAMB(Theory):
    """
    Cobaya theory module using polynomial-based emulator for CMB D_ell.
    Converts D_ell → C_ell and returns {"tt": Cls}.
    """

    # Set ℓ_max of the emulator 
    ell_max_emulator = 4000
    ells = np.arange(2, ell_max_emulator + 1)
    ell_factors = 2 * np.pi / (ells * (ells + 1)) #/ (2.7255**2 * 1e12)    # muK2 --> FIRASK2 convention

    def initialize(self):
        # Load the trained emulators for TT, TE, and EE
        with open("emulators/PolyCAMB_Dl_TT.pkl", "rb") as f:
            self.TT_emu = pickle.load(f)
        
        # Load EE and TE emulators - you'll need to create these
        try:
            with open("emulators/PolyCAMB_Dl_EE.pkl", "rb") as f:
                self.EE_emu = pickle.load(f)
        except FileNotFoundError:
            print("Warning: EE emulator not found. Using TT emulator as placeholder.")
            
        try:
            with open("emulators/PolyCAMB_Dl_TE.pkl", "rb") as f:
                self.TE_emu = pickle.load(f)
        except FileNotFoundError:
            print("Warning: TE emulator not found. Using TT emulator as placeholder.")

    def get_requirements(self):
        return ['omega_b', 'omega_c', 'theta_star', 'logA', 'ns', 'tau']

    def get_Cl(self, ell_max=4000, **kwargs):
        # Collect input parameters
        params = self.provider

        theta = np.array([
            params.get_param("omega_b"),
            params.get_param("omega_c"),
            params.get_param("theta_star"),
            params.get_param("logA"),
            params.get_param("ns"),
            params.get_param("tau"),
        ])

        # Predict D_ell from emulators
        D_ell_TT = self.TT_emu.forward_emulator(theta)
        D_ell_EE = self.EE_emu.forward_emulator(theta)
        D_ell_TE = self.TE_emu.forward_emulator(theta)

        # Handle low-ell vs high-ell cases differently
        if ell_max <= 30:  # Low-ell case
            # Extract ℓ=2 to ell_max (emulator starts from ℓ=2)
            # ells_used = np.arange(2, ell_max + 1)
            # ell_factors_used = 2 * np.pi / (ells_used * (ells_used + 1))
            
            # C_ell_TT = D_ell_TT[2:ell_max + 1] * self.ell_factors[:ell_max - 1]
            # C_ell_EE = D_ell_EE[2:ell_max + 1] * self.ell_factors[:ell_max - 1]  
            # C_ell_TE = D_ell_TE[2:ell_max + 1] * self.ell_factors[:ell_max - 1]
            C_ell_TT = D_ell_TT[:ell_max - 1] * self.ell_factors[:ell_max - 1]
            C_ell_EE = D_ell_EE[:ell_max - 1] * self.ell_factors[:ell_max - 1]  
            C_ell_TE = D_ell_TE[:ell_max - 1] * self.ell_factors[:ell_max - 1]

        else:  # High-ell case
            ell_cap = min(ell_max, self.ell_max_emulator)
            # ells_used = np.arange(2, ell_cap + 1)
            # ell_factors_used = 2 * np.pi / (ells_used * (ells_used + 1))

            used_ell_factors = self.ell_factors[:ell_cap - 1]
            
            C_ell_TT = D_ell_TT[:ell_cap - 1] * used_ell_factors
            C_ell_EE = D_ell_EE[:ell_cap - 1] * used_ell_factors
            C_ell_TE = D_ell_TE[:ell_cap - 1] * used_ell_factors

            # Pad with zeros if needed for high-ell
            if ell_max > self.ell_max_emulator:
                pad_len = ell_max - self.ell_max_emulator
                C_ell_TT = np.concatenate([C_ell_TT, np.zeros(pad_len)])
                C_ell_EE = np.concatenate([C_ell_EE, np.zeros(pad_len)])
                C_ell_TE = np.concatenate([C_ell_TE, np.zeros(pad_len)])

        # Return as required dictionary
        return {
            "tt": C_ell_TT,
            "ee": C_ell_EE, 
            "te": C_ell_TE
        }

    def get_can_provide(self):
        return {"Cl": ["tt", "ee", "te"]}

    def must_provide(self, **_):
        return {}
