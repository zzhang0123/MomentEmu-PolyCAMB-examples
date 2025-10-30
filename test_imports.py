#!/usr/bin/env python
"""Test script to verify MomentEmu imports work correctly"""

import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    from MomentEmu import PolyEmu
    print("✓ MomentEmu.PolyEmu imported successfully")
    
    # Test loading a pickle file
    import pickle
    with open("emulators/PolyCAMB_Dl_TT.pkl", "rb") as f:
        emulator = pickle.load(f)
    print("✓ Successfully loaded TT emulator")
    print(f"  Emulator type: {type(emulator)}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()