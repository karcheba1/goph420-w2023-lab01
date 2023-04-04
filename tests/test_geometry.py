import unittest

import numpy as np

from fem_1d_heat.geometry import (
        global_to_local,
        shape_matrix
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

if __name__ == "__main__":
    unittest.main()

