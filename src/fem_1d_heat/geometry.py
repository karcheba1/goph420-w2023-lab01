import numpy as np


def global_to_local(z, z_e):
    """Converts global coordinate to local (element) coordinate.

    Parameters
    ----------
    z : float
        The global coordinate to convert to local coordinate
    z_e : array_like, shape = (2,)
        Nodal coordinates of the element

    Returns
    -------
    float
        The local coordinate
    """
    return (z - z_e[0]) / (z_e[1] - z_e[0])


def shape_matrix(s):
    """Calculate the shape function matrix for 1d linear interpolation.

    Parameters
    ----------
    s : float
        The local coordinate in the element

    Returns
    -------
    numpy.ndarray, shape = (1, 2)
        The shape function matrix
    """
    return np.array([[(1 - s), s]])


def gradient_matrix(s, dz):
    """Calculate the gradient matrix for 1d linear interpolation.

    Parameters
    ----------
    s : float
        The local coordinate in the element
    dz : float
        The scaling factor from global to local coordinates

    Returns
    -------
    numpy.ndarray, shape = (1, 2)
        The gradient matrix
    """
    return np.array([[-1, 1]]) / dz


class Point:
    """ Store the depth as a coordinate.

    Parameters
    ----------
    z : float
        depth value
    """

    def __init__(self, z=0.0):
        self.z = z

    @property
    def z(self):
        """Gets the depth of the Point object

        Parameters
        ----------
        value : float
             Sets the depth of the element

        Returns
        -------
        z : float
             Gets the depth of the element
        """
        return self._z

    @z.setter
    def z(self, value):
        value = float(value)
        self._z = value


class Node(Point):
    """ Store the temperature at coordinate z.

    Parameters
    ----------
    z : float
        depth value
    temp : float
        temperature value
    """

    def __init__(self, z=0.0, temp=0.0):
        self.temp = temp
        self.z = z

    @property
    def temp(self):
        """The temperature of the Node 

        Parameters
        ----------
        value : float
            The temperature to be assigned to the Node

        Returns
        -------
        temp : float
            The temperature of the Node

        Raises
        ------
        ValueError
            If the input value is not convertible to a float
        """
        return self._temp

    @temp.setter
    def temp(self, value):
        value = float(value)
        self._temp = value


class Element:
    """Stores a set of Nodes and material property information.
        
        Parameters
        ----------
        nodes : tuple
            Node objects with length 2

    """

    def __init__(self, nodes):
        nodes = tuple(nodes)
        if len(nodes) != 2:
            raise ValueError(f"len of nodes {len(nodes)} is not equal to 2")
        for nd in nodes:
            if not isinstance(nd, Node):
                raise TypeError(f"nodes contains {type(nd)} which is not a Node")
        self._nodes = nodes

    @property
    def nodes(self):
        """Returns a tuple of Node objects contained in the element.
        
        Returns
        -------
        nodes : tuple
            Node objects with length 2
        """
        return self._nodes

    @property
    def dz(self):
        return abs(self.nodes[1].z - self.nodes[0].z)

    @property
    def thm_cond(self):
        pass

    @thm_cond.setter
    def thm_cond(self, value):
        pass
