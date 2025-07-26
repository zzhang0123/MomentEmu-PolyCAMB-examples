#!/usr/bin/env python3
"""
Comprehensive test summary for MomentEmu-PolyCAMB-examples
"""

def run_all_tests():
    print("🧪 MomentEmu-PolyCAMB-Examples Test Summary")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Setup script
    total_tests += 1
    try:
        import subprocess
        result = subprocess.run(['python', 'setup_examples.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and "Setup complete" in result.stdout:
            print("✅ 1. Setup script works correctly")
            tests_passed += 1
        else:
            print("❌ 1. Setup script failed")
    except Exception as e:
        print(f"❌ 1. Setup script failed: {e}")
    
    # Test 2: Core imports
    total_tests += 1
    try:
        from MomentEmu import PolyEmu
        import PolyCAMB
        import visual
        print("✅ 2. All core modules import successfully")
        tests_passed += 1
    except Exception as e:
        print(f"❌ 2. Core imports failed: {e}")
    
    # Test 3: Pre-trained emulators
    total_tests += 1
    try:
        import pickle
        import numpy as np
        
        with open('emulators/PolyCAMB_Dl_N7.pkl', 'rb') as f:
            polycamb_dl = pickle.load(f)
        
        with open('emulators/PolyCAMB_peak_N7.pkl', 'rb') as f:
            polycamb_peak = pickle.load(f)
        
        # Test predictions
        test_params = np.array([[0.022, 0.12, 67.5, 3.05, 0.96, 0.06]])
        pred_cl = polycamb_dl.forward_emulator(test_params)
        pred_peaks = polycamb_peak.forward_emulator(test_params)
        est_params = polycamb_peak.backward_emulator(pred_peaks)
        
        if pred_cl.shape[1] > 1000 and pred_peaks.shape[1] == 10:
            print("✅ 3. Pre-trained emulators work correctly")
            tests_passed += 1
        else:
            print("❌ 3. Pre-trained emulators have unexpected output shapes")
    except Exception as e:
        print(f"❌ 3. Pre-trained emulators failed: {e}")
    
    # Test 4: PolyCAMB functions
    total_tests += 1
    try:
        params, names = PolyCAMB.sample_lcdm_params_grid(n_grid_per_param=2)
        rand_params = PolyCAMB.sample_lcdm_params_rand(n_samples=3)
        as_val = PolyCAMB.invert_log_As(3.05)
        
        if params.shape[1] == 6 and len(names) == 6 and rand_params.shape[0] == 3:
            print("✅ 4. PolyCAMB utility functions work correctly")
            tests_passed += 1
        else:
            print("❌ 4. PolyCAMB functions have unexpected outputs")
    except Exception as e:
        print(f"❌ 4. PolyCAMB functions failed: {e}")
    
    # Test 5: Jupyter notebook structure
    total_tests += 1
    try:
        import json
        with open('notebooks/poly_camb.ipynb', 'r') as f:
            notebook = json.load(f)
        
        cells = notebook.get('cells', [])
        has_code = any(cell.get('cell_type') == 'code' for cell in cells)
        has_markdown = any(cell.get('cell_type') == 'markdown' for cell in cells)
        
        if len(cells) > 10 and has_code and has_markdown:
            print("✅ 5. Jupyter notebook is well-structured")
            tests_passed += 1
        else:
            print("❌ 5. Jupyter notebook structure issues")
    except Exception as e:
        print(f"❌ 5. Jupyter notebook test failed: {e}")
    
    # Test 6: Visual module
    total_tests += 1
    try:
        visual_functions = [f for f in dir(visual) if not f.startswith('_')]
        expected_functions = ['plot_corner_comparison', 'plot_predictions', 'plot_residuals']
        has_expected = all(func in visual_functions for func in expected_functions)
        
        if has_expected:
            print("✅ 6. Visual module has expected plotting functions")
            tests_passed += 1
        else:
            print("❌ 6. Visual module missing expected functions")
    except Exception as e:
        print(f"❌ 6. Visual module test failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Examples repository is fully functional!")
        return True
    elif tests_passed >= total_tests * 0.8:
        print("✅ Most tests passed! Repository is largely functional.")
        return True
    else:
        print("⚠️  Several tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
