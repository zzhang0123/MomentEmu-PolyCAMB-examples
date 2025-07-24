# Datasets Information

The `datasets/` directory contains training data used in the PolyCAMB examples. Due to file size constraints, these datasets are not included in the repository.

## Missing Dataset Files

The following files are referenced in the code but not included:
- `camb_outputs_7.npy` - CAMB power spectrum outputs  
- `camb_outputs_narr_6.npy` - Narrow range CAMB outputs
- `camb_outputs_narr_7.npy` - Narrow range CAMB outputs (N=7)
- `camb_params_7.npy` - Cosmological parameter samples
- `camb_params_narr_6.npy` - Narrow range parameter samples  
- `camb_params_narr_7.npy` - Narrow range parameter samples (N=7)
- `perturbed_LCDM_Dell.npy` - Power spectrum perturbation data
- `perturbed_LCDM_Dell_narrow.npy` - Narrow range perturbation data
- `perturbed_LCDM_params.npy` - Parameter perturbation data
- `perturbed_LCDM_params_narrow.npy` - Narrow range parameter perturbation data

## Generating Your Own Datasets

You can generate these datasets by running the training data generation functions in `PolyCAMB.py`:

```python
from PolyCAMB import sample_lcdm_params_lhs, compute_cmb_cl
import numpy as np

# Generate parameter samples
params = sample_lcdm_params_lhs(n_samples=1000, bound='narrow')  # or 'wide'
# Generate corresponding CMB data  
cl_data = compute_cmb_cl(params)

# Save datasets
np.save('datasets/camb_params_custom.npy', params)
np.save('datasets/camb_outputs_custom.npy', cl_data)
```

## Pre-trained Emulators

The `emulators/` directory contains pre-trained models that can be used directly without regenerating the datasets:
- `PolyCAMB_Dl_N7.pkl` - CMB power spectrum emulator
- `PolyCAMB_peak_N7.pkl` - Acoustic peak features emulator
