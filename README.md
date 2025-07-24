# MomentEmu PolyCAMB Examples

This repository contains comprehensive examples and applications of **MomentEmu** applied to cosmological parameter estimation using CAMB (Code for Anisotropies in the Microwave Background).

## 📖 Overview

This repository demonstrates the **MomentEmu** polynomial emulator package through real-world cosmological applications. For the core **MomentEmu** library, visit: [MomentEmu](https://github.com/zzhang0123/MomentEmu)

## 🎯 Featured Applications

### PolyCAMB-Dℓ
- **Purpose**: Maps six cosmological parameters to the CMB temperature power spectrum
- **Accuracy**: ~0.03% for ℓ ≤ 2510
- **Use case**: Fast cosmological parameter estimation for MCMC chains

### PolyCAMB-peak  
- **Purpose**: Bidirectional mapping between cosmological parameters and acoustic peak features
- **Accuracy**: Sub-percent precision
- **Use case**: Both forward prediction and inverse parameter estimation

## 📁 Repository Structure

```
├── PolyCAMB.py              # Main PolyCAMB emulator implementations
├── visual.py                # Visualization utilities
├── MomentEmu.py            # Core emulator (use pip install instead)
├── notebooks/
│   └── poly_camb.ipynb     # Complete tutorial notebook
├── chains/                 # MCMC chain outputs and configurations
├── cobaya_test/            # Cobaya integration examples
├── emulators/              # Pre-trained emulator files
├── figures/                # Generated plots and visualizations
└── datasets/               # Training data (not included - see below)
```

## 🛠️ Installation

### Prerequisites
```bash
# Install core MomentEmu library
pip install git+https://github.com/zzhang0123/MomentEmu.git

# Install additional dependencies for examples
pip install camb pyDOE tqdm pandas cobaya
```

### Clone Examples Repository
```bash
git clone https://github.com/zzhang0123/MomentEmu-PolyCAMB-examples.git
cd MomentEmu-PolyCAMB-examples
```

## 🚀 Quick Start

### 1. Jupyter Notebook Tutorial
The best way to get started is with the comprehensive notebook:
```bash
jupyter notebook notebooks/poly_camb.ipynb
```

### 2. Using Pre-trained Emulators
```python
import pickle
from MomentEmu import PolyEmu

# Load pre-trained PolyCAMB-Dℓ emulator
with open('emulators/PolyCAMB_Dl_N7.pkl', 'rb') as f:
    polycamb_dl = pickle.load(f)

# Example prediction for new cosmological parameters
new_params = [0.022, 0.12, 67.5, 3.05, 0.96, 0.06]  # [ombh2, omch2, H0, ln(10^10 As), ns, tau]
predicted_Cl = polycamb_dl.forward_emulator(new_params)
```

### 3. Training Your Own Emulator
```python
from PolyCAMB import sample_lcdm_params_lhs, compute_cmb_cl
from MomentEmu import PolyEmu

# Generate training data
params = sample_lcdm_params_lhs(n_samples=1000)
cl_data = compute_cmb_cl(params)

# Train emulator
emulator = PolyEmu(params, cl_data, forward=True, backward=False)
```

## 📖 Citation

If you use these examples in your research, please cite:

```bibtex
@article{Zhang2025MomentEmu,
  title={MomentEmu: A lightweight, interpretable polynomial emulator for smooth mappings},
  author={Zhang, Your Name},
  journal={arXiv preprint arXiv:2507.02179},
  year={2025}
}
```

## 🔗 Related Links

- **Core Library**: [MomentEmu](https://github.com/zzhang0123/MomentEmu)
- **CAMB**: [CAMB cosmology code](https://camb.info/)
- **Paper**: [arXiv:2507.02179](https://arxiv.org/abs/2507.02179)
