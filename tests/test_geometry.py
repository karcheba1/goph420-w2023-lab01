import unittest

import numpy as np

from fem_1d_heat.geometry import (
        global_to_local, gradient_matrix
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


class TestGradientMatrix(unittest.TestCase):
    """This class is setup for the linear case such that the s parameter is unused and such we feed a placeholder value of zero into it."""
    def setUp(self):
        self.s = 0
        self.dz = 2

    def test_valid_float_input(self):
        g_exp = np.ndarray([-.5,.5])
        g_act = gradient_matrix(self.s, self.dz)
        self.assertIsInstance(g_act, np.ndarray)
        self.assertTrue(np.allclose(g_exp,g_act))

    def test_valid_string_input(self):
        g_exp = np.ndarray([-0.2,0.2])
        g_act = gradient_matrix(0, '5')
        self.assertIsInstance(g_act, np.ndarray)
        self.assertTrue(np.allclose(g_exp,g_act))

    def test_correct_shape(self):
        g_act = gradient_matrix(self.s, self.dz)
        self.assertTrue(g_act.shape()==(1,2))
    
    def test_invalid_str_input(self):
        with self.assertRaises(ValueError):
            gradient_matrix('five', self.dz)

if __name__ == "__main__":
    unittest.main()

