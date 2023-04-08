import unittest

import numpy as np

from fem_1d_heat.geometry import (
    global_to_local,
    gradient_matrix,
    shape_matrix,
    Node,
    Element,
)


class TestGlobalToLocal(unittest.TestCase):

    def setUp(self):
        self.z_e = np.array([0.0, 6.0])

    def test_valid_float_output(self):
        s_act = global_to_local(3.0, self.z_e)
        self.assertIsInstance(s_act, float)

    def test_valid_input_beg(self):
        s_exp = 0.0
        s_act = global_to_local(self.z_e[0], self.z_e)
        self.assertAlmostEqual(s_act, s_exp)

    def test_valid_input_mid(self):
        s_exp = 0.5
        s_act = global_to_local(np.mean(self.z_e), self.z_e)
        self.assertAlmostEqual(s_act, s_exp)

    def test_valid_input_end(self):
        s_exp = 1.0
        s_act = global_to_local(self.z_e[1], self.z_e)
        self.assertAlmostEqual(s_act, s_exp)

    def test_invalid_str_input_z(self):
        with self.assertRaises(ValueError):
            global_to_local('two', self.z_e)

    def test_invalid_str_input_ze(self):
        with self.assertRaises(ValueError):
            global_to_local(3.0, "two")

    def test_invalid_len_ze(self):
        with self.assertRaises(ValueError):
            global_to_local(3.0, [0.0])


class TestShapeMatrix(unittest.TestCase):

    def test_valid_input(self):
        x_exp = np.array([[0.2, 0.8]])
        x_act = shape_matrix(0.8)
        self.assertIsInstance(x_act, np.ndarray)
        self.assertTrue(np.allclose(x_exp, x_act))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            shape_matrix('half')
        with self.assertRaises(ValueError):
            shape_matrix(-0.1)
        with self.assertRaises(ValueError):
            shape_matrix(1.1)


class TestGradientMatrix(unittest.TestCase):
    """This class is setup for the linear case such that the s parameter is
    unused and such we feed a placeholder value of zero into it."""

    def setUp(self):
        self.dummy_s = 0.0
        self.dz = 2.0

    def test_valid_input(self):
        exp_result = np.array([-.5, .5])
        exp_shape = (1, 2)
        act_result = gradient_matrix(self.dummy_s, self.dz)
        self.assertIsInstance(act_result, np.ndarray)
        self.assertEqual(act_result.shape, exp_shape)
        self.assertTrue(np.allclose(act_result, exp_result))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            gradient_matrix('five', self.dz)
        with self.assertRaises(ValueError):
            gradient_matrix(-0.1, self.dz)
        with self.assertRaises(ValueError):
            gradient_matrix(1.1, self.dz)
        with self.assertRaises(ValueError):
            gradient_matrix(self.dummy_s, 'five')
        with self.assertRaises(ValueError):
            gradient_matrix(self.dummy_s, -0.5)


# TODO: implement Point tests
class TestPoint(unittest.TestCase):
    pass


# TODO: implement Node tests
class TestNode(unittest.TestCase):
    pass


class TestElement(unittest.TestCase):

    def setUp(self):
        self.nodes = (Node(0.0), Node(1.5))
        self.thm_cond = 6.9e1
        self.vol_heat_cap = 4.2e2

    def test_valid_input(self):
        e = Element(self.nodes, self.thm_cond, self.vol_heat_cap)
        self.assertIsInstance(e.nodes, tuple)
        self.assertEqual(len(e.nodes), 2)
        self.assertIs(e.nodes[0], self.nodes[0])
        self.assertIs(e.nodes[1], self.nodes[1])
        self.assertEqual(e.dz, self.nodes[1].z - self.nodes[0].z)
        self.assertAlmostEqual(e.thm_cond, self.thm_cond)
        self.assertAlmostEqual(e.vol_heat_cap, self.vol_heat_cap)

    def test_invalid_nodes(self):
        with self.assertRaises(TypeError):
            Element(0.0)
        with self.assertRaises(TypeError):
            Element([0.0, 1.5])
        with self.assertRaises(ValueError):
            Element((Node(0.0), Node(1.5), Node(3.0)))

    def test_default_properties(self):
        e = Element(self.nodes)
        self.assertAlmostEqual(e.thm_cond, 0.0)
        self.assertAlmostEqual(e.vol_heat_cap, 0.0)

    def test_invalid_properties(self):
        e = Element(self.nodes)
        with self.assertRaises(ValueError):
            e.thm_cond = "five"
        with self.assertRaises(ValueError):
            e.thm_cond = -0.1
        with self.assertRaises(ValueError):
            e.vol_heat_cap = "five"
        with self.assertRaises(ValueError):
            e.vol_heat_cap = -0.1


if __name__ == "__main__":
    unittest.main()
