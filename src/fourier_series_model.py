"""
    THIS IS THE FUNCTIONAL PART OF THIS APPLICATION, WHICH WILL PROVIDE THE
    FOURIER SERIES BY OBTAINING ITS COEFFICIENTS. IN THIS PROJECT WHICH IS
    USING MVC DESIGN PATTERN, THIS PART WILL BE THE MODEL LAYER AND I WILL
    KEEP IT EFFICIENT AS POSIBLE SO THE PROGRAM RUNS SMOOTHLY!
"""

import numpy as np
# IMPORTING THE MODULES TO EVALUATE THE INPUT TO A PYTHON FUNCTION
from numpy import (
    cos, cosh, arccos, sin, sinh, arcsin, tan, tanh, arctan, log, log2, log10, sqrt, pi, exp
)
from scipy import integrate

class FourierSeries:
    def __init__ (self, T, T1, T2, m, input_xt):
        # DEFINING THE INPUTS FOR SYNTHESIS AND ANALYSIS EQUATIONS OF CT-FOURIER SERIES
        self.T = T
        self.T1 = T1
        self.T2 = T2
        self.m = m
        # EVALUATING THE STRING INPUT OF USE TO PYTHON EXPRESSION
        self.input_xt = input_xt

    def _ak_0 (self):
        # 
        ak_0_result = (1/self.T) * integrate.fixed_quad (lambda t: self.input_xt (t), self.T1, self.T2)[0]
        return ak_0_result

    def _ak_m (self, k):
        ak_m_result = (1/self.T) * integrate.fixed_quad (lambda t: self.input_xt (t) * self._exp_func(-t, k), self.T1, self.T2, n=1000)[0]
        return ak_m_result

    def _exp_func (self, t, k):
        return exp(1j * 2*pi* k * t / self.T)
    
    def xt (self, t):
        xt_result = self._ak_0 () +  np.real (sum ([self._ak_m (k) * self._exp_func (t, k) for k in range (-self.m, self.m) if k != 0]))
        return xt_result