import unittest

import numpy as np

from fem_1d_heat.geometry import (
        global_to_local,
        gradient_matrix,
        shape_matrix,
)


class TestGlobalToLocalValues(unittest.TestCase):
    
    def setUp(self):
        self.z = 3.0
        self.z_e = np.array([0, 6])

    def test_valid_float_input(self):
        s_exp = 0.5
        s_act = global_to_local(self.z, self.z_e)
        self.assertIsInstance(s_act, float)
        self.assertAlmostEqual(s_exp, s_act)

    def test_invalid_str_input(self):
        with self.assertRaises(TypeError):
            global_to_local('two', self.z_e)

class TestShapeMatrix(unittest.TestCase):

    def setUp(self):
        self.s = 0.5
        
    def test_valid_float_input(self):
        x_exp = np.array([[0.5, 0.5]])
        x_act = shape_matrix(self.s)
        self.assertIsInstance(x_act,np.ndarray)
        self.assertTrue(np.allclose(x_exp,x_act))
    
    def test_invalid_str_input(self):
        with self.assertRaises(TypeError):
            shape_matrix('half')

class TestGradientMatrix(unittest.TestCase):
    """This class is setup for the linear case such that the s parameter is 
    unused and such we feed a placeholder value of zero into it."""
    def setUp(self):
        self.s = 0
        self.dz = 2

    def test_valid_float_input(self):
        g_exp = np.array([-.5,.5])
        g_act = gradient_matrix(self.s, self.dz)
        self.assertIsInstance(g_act, np.ndarray)
        self.assertTrue(np.allclose(g_exp,g_act))

    def test_correct_shape(self):
        g_act = gradient_matrix(self.s, self.dz)
        self.assertTrue(g_act.shape==(1,2))
    
    def test_invalid_str_input(self):
        with self.assertRaises(TypeError):
            gradient_matrix(0, 'five')

class TestElement(unittest.TestCase):

    def setUp(self):
        self.nodes = 0
        self.thm_cond = 69
        self.vol_heat_cap = 420

    def test_valid_float_input(self):
        pass

    def test_correct_shape(self):
        pass
    
    def test_invalid_float_input(self):
        with self.assertRaises(ValueError):
            element = Element(nodes, -5, 5)
        
        pass

    

if __name__ == "__main__":
    unittest.main()

