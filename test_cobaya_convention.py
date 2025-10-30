#!/usr/bin/env python
"""Test script to understand Cobaya Cl array conventions"""

import numpy as np
from cobaya.theory import Theory

class TestTheory(Theory):
    def get_requirements(self):
        return []
    
    def get_Cl(self, ell_max=30, **kwargs):
        print(f"TestTheory.get_Cl called with ell_max = {ell_max}")
        
        # Create a simple test array
        # Test different conventions to see what works
        
        # Convention 1: Array indexed from ell=0 (length = ell_max + 1)
        cls_v1 = np.zeros(ell_max + 1)
        for ell in range(2, ell_max + 1):
            cls_v1[ell] = 1000.0 / (ell * (ell + 1))  # Simple test spectrum
            
        # Convention 2: Array indexed from ell=2 (length = ell_max - 1)  
        cls_v2 = np.array([1000.0 / (ell * (ell + 1)) for ell in range(2, ell_max + 1)])
        
        print(f"  Convention 1 (ell=0 indexed): length = {len(cls_v1)}")
        print(f"  Convention 2 (ell=2 indexed): length = {len(cls_v2)}")
        print(f"  cls_v1[2:5] = {cls_v1[2:5]}")
        print(f"  cls_v2[0:3] = {cls_v2[0:3]}")
        
        # Return Convention 2 for now (ell=2 indexed)
        return {"tt": cls_v2}
    
    def get_can_provide(self):
        return {"Cl": ["tt"]}
    
    def must_provide(self, **_):
        return {}

if __name__ == "__main__":
    # Test with a simple likelihood request
    theory = TestTheory({})
    theory.initialize()
    
    # Simulate what low-l likelihood would request
    cls_29 = theory.get_Cl(ell_max=29)
    print(f"For ell_max=29, returned array length: {len(cls_29['tt'])}")
    
    cls_100 = theory.get_Cl(ell_max=100) 
    print(f"For ell_max=100, returned array length: {len(cls_100['tt'])}")