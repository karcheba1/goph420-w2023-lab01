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
    """

    def __init__(self, thm_cond=0.0, vol_heat_cap=0.0):
        self.thm_cond = thm_cond
        self.vol_heat_cap = vol_heat_cap

    @property
    def nodes(self):
        """Returns a tuple of Node objects contained in the element.
        """
        pass

    @property
    def dz(self):
        pass

    @property
    def thm_cond(self):
        """Heat conductivity of the element.

        Parameters
        ----------
        value : float
            The heat conductivity to be assigned to the element

        Returns
        -------
        thm_cond : float
            The heat conductivity of the element

        Raises
        ------
        ValueError
            If the input value is less than 0.0
        """
        return self._thm_cond

    @thm_cond.setter
    def thm_cond(self, value):
        value = float(value)
        if value < 0.0:
            raise ValueError(f"{value} < 0.0 is not valid")
        self._thm_cond = value

    @property
    def vol_heat_cap(self):
        """Volumetric heat capacity of the element.

        Parameters
        ----------
        value : float
            The Volumetric heat capacity to be assigned to the element

        Returns
        -------
        thm_cond : float
            The Volumetric heat capacity of the element

        Raises
        ------
        ValueError
            If the input value is less than 0.0
        """
        return self._vol_heat_cap

    @vol_heat_cap.setter
    def vol_heat_cap(self, value):
        value = float(value)
        if value < 0.0:
            raise ValueError(f"{value} < 0.0 is not valid")
        self._vol_heat_cap = value