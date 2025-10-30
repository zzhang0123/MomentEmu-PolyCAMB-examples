#!/usr/bin/env python
"""Test Planck likelihood expectations with built-in CAMB theory"""

# Create a minimal CAMB + Planck setup to see what arrays are passed
test_info = {
    'theory': {
        'camb': {
            'extra_args': {
                'halofit_version': 'mead',
                'dark_energy_model': 'ppf'
            }
        }
    },
    'likelihood': {
        'planck_2018_lowl.TT': {
            'requires': {
                'lmax': 29,
                'Cl': {'tt': None}
            }
        }
    },
    'params': {
        'ombh2': 0.022,
        'omch2': 0.12,
        'H0': 67.5,
        'As': 2.1e-9,
        'ns': 0.965,
        'tau': 0.054
    }
}

# Patch CAMB to intercept what it passes to Planck
from cobaya.model import Model
from cobaya.theories import camb
import numpy as np

original_get_Cl = camb.CAMB.get_Cl

def patched_get_Cl(self, ell_factor=False, units="FIRASmuK2"):
    result = original_get_Cl(self, ell_factor, units)
    
    # Print what CAMB returns
    print(f"\\nCAMB get_Cl returned:")
    for key, value in result.items():
        if isinstance(value, np.ndarray):
            print(f"  {key}: shape={value.shape}, first 5 = {value[:5]}")
        else:
            print(f"  {key}: {value}")
    
    return result

# Monkey patch
camb.CAMB.get_Cl = patched_get_Cl

try:
    print("Creating Cobaya model with CAMB + Planck low-l TT...")
    model = Model(test_info)
    
    print("\\nComputing likelihood (this will show what arrays are passed)...")
    # This will trigger the theory calculation and show us the arrays
    loglike = model.loglike({'ombh2': 0.022, 'omch2': 0.12, 'H0': 67.5, 'As': 2.1e-9, 'ns': 0.965, 'tau': 0.054})
    
    print(f"\\nFinal loglikelihood: {loglike}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()