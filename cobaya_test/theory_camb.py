import sys
import os
from MomentEmu import *
import camb


import numpy as np
from cobaya.theory import Theory
import pickle

# from cobaya.theories._base_classes import Theory

def invert_log_As(ln_1e10_As):
    """
    Invert the logarithmic scaling of the primordial amplitude.
    Parameters:
        ln_1e10_As : float
            Logarithm of the primordial amplitude in units of 1e-10 As.
    Returns:
        As : float
            Primordial amplitude in units of As.
    """
    As = np.exp(ln_1e10_As) * 1e-10
    return As

class rawCAMB(Theory):
    """
    Cobaya theory module using polynomial-based emulator for CMB D_ell.
    Converts D_ell → C_ell and returns {"tt": Cls}.
    """

    # Set ℓ_max of the emulator 
    ell_max_emulator = 4000
    ells = np.arange(2, ell_max_emulator + 1)
    ell_factors = 2 * np.pi / (ells * (ells + 1)) #/ (2.7255**2 * 1e12)    # muK2 --> FIRASK2 convention

    def initialize(self):
        self.pars = camb.CAMBparams()
        

    def get_requirements(self):
        return ['omega_b', 'omega_c', 'theta_star', 'logA', 'ns', 'tau'] 
    
    def get_Cl(self, ell_max=4000, **kwargs):
        pars = camb.CAMBparams()
        params = self.provider

        omb = params.get_param("omega_b")
        omc = params.get_param("omega_c")
        thetastar = params.get_param("theta_star")
        logA = params.get_param("logA")
        ns = params.get_param("ns")
        tau =params.get_param("tau")

        # Set cosmological parameters
        pars.set_cosmology(thetastar=thetastar, ombh2=omb, omch2=omc, tau=tau)

        # Initial power spectrum parameters
        As_arr = invert_log_As(logA)
        pars.InitPower.set_params(As=As_arr, ns=ns)

        # Compute lensed CMB power spectra up to lmax
        pars.set_for_lmax(ell_max, lens_potential_accuracy=2)
        results = camb.get_results(pars)
        powers = results.get_cmb_power_spectra(pars, CMB_unit='muK')

        # Extract total TT spectrum (including lensing)
        D_ell_TT = powers['total'][2: self.ell_max_emulator + 1, 0]
        D_ell_EE = powers['total'][2: self.ell_max_emulator + 1, 1]
        D_ell_TE = powers['total'][2: self.ell_max_emulator + 1, 3]

        

        C_ell_TT = D_ell_TT * self.ell_factors
        C_ell_EE = D_ell_EE * self.ell_factors
        C_ell_TE = D_ell_TE * self.ell_factors

        if ell_max > self.ell_max_emulator:
            pad_len = ell_max - self.ell_max_emulator
            C_ell_TT = np.concatenate([C_ell_TT, np.zeros(pad_len)])
            C_ell_EE = np.concatenate([C_ell_EE, np.zeros(pad_len)])
            C_ell_TE = np.concatenate([C_ell_TE, np.zeros(pad_len)])

        return {"tt": C_ell_TT, "ee": C_ell_EE, "te": C_ell_TE}


    def get_can_provide(self):
        return {"Cl": ["tt", "ee", "te"]}

    def must_provide(self, **_):
        return {}
