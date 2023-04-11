import numpy as np


def global_to_local(z, z_e):
    """Converts global coordinate to local (element) coordinate.

    Parameters
    ----------
    z : float
        The global coordinate to convert to local coordinate
    z_e : array_like, shape = (2, ), dtype=float_like
        Nodal coordinates of the element,
        will be flattened prior to checking shape

    Returns
    -------
    float
        The local coordinate

    Raises
    ------
    ValueError
        If z is not convertible to float
        If z_e values are not convertible to float
        If len(z_e) is not 2
    """
    z = float(z)
    z_e = np.array(z_e, dtype=float).flatten()
    if len(z_e) != 2:
        raise ValueError(f"z_e contains {len(z_e)} entries, should be 2")
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

    Raises
    ------
    ValueError
        If s is not convertible to float
        If s is not between 0.0 and 1.0
    """
    s = float(s)
    if s < 0.0 or s > 1.0:
        raise ValueError(f"s == {s} is not between 0.0 and 1.0")
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

    Raises
    ------
    ValueError
        If s is not convertible to float
        If s is not between 0.0 and 1.0
        If dz is not convertible to float
        If dz is negative
    """
    s = float(s)
    if s < 0.0 or s > 1.0:
        raise ValueError(f"s == {s} is not between 0.0 and 1.0")
    dz = float(dz)
    if dz < 0.0:
        raise ValueError(f"dz == {dz} is negative")
    return np.array([[-1.0, 1.0]]) / dz


class Point:
    """Stores the depth coordinate of a Point in one dimension

    Parameters
    ----------
    z : float, optional, default=0.0
        Depth of the Point
    """

    def __init__(self, z=0.0):
        self.z = z

    @property
    def z(self):
        """The depth of the Point

        Parameters
        ----------
        value : float
             Value to set the depth of the Point

        Returns
        -------
        z : float
             The depth of the Point

        Raises
        ------
        ValueError
            If the value to be assigned is not convertible to float
        """
        return self._z

    @z.setter
    def z(self, value):
        value = float(value)
        self._z = value


class Node(Point):
    """Store the temperature at coordinate z.

    Parameters
    ----------
    z : float, optional, default=0.0
        Depth of the Node
    temp : float, optional, default=0.0
        Temperature of the Node
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
    nodes : tuple or iterable, len = 2
        Node objects to be contained in the element,
        will be converted to tuple
    thm_cond : float, optional, default=0.0
        Thermal conductivity of the element
    vol_heat_cap : float, optional, default=0.0
        Volumetric heat capacity of the element

    Raises
    ------
    TypeError
        If nodes is not iterable (i.e. convertible to tuple)
        If nodes contains any non-Node objects
    ValueError
        If len(nodes) != 2
    """

    # Gauss quadrature points and weights [0, 1] domain
    _int_pts = np.array([0.21132486540518708, 0.7886751345948129])
    _int_wts = np.array([0.5, 0.5])

    def __init__(self, nodes, thm_cond=0.0, vol_heat_cap=0.0):
        nodes = tuple(nodes)
        if len(nodes) != 2:
            raise ValueError(f"len(nodes) = {len(nodes)} is not equal to 2")
        for nd in nodes:
            if not isinstance(nd, Node):
                raise TypeError(
                    f"nodes contains {type(nd)} which is not a Node")
        self._nodes = nodes
        self.thm_cond = thm_cond
        self.vol_heat_cap = vol_heat_cap

    @property
    def nodes(self):
        """Node objects contained in the element.

        Returns
        -------
        nodes : tuple, len = 2
            Tuple of Node objects in the element
        """
        return self._nodes

    @property
    def dz(self):
        """Element thickness.

        Returns
        -------
        float
            The thickness or length of the element.
        """
        return np.abs(self.nodes[1].z - self.nodes[0].z)

    @property
    def thm_cond(self):
        """Thermal conductivity of the element.

        Parameters
        ----------
        value : float
            The thermal conductivity to be assigned to the element

        Returns
        -------
        thm_cond : float
            The thermal conductivity of the element

        Raises
        ------
        ValueError
            If the input value is not convertible to a float
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
            The volumetric heat capacity to be assigned to the element

        Returns
        -------
        thm_cond : float
            The volumetric heat capacity of the element

        Raises
        ------
        ValueError
            If the input value is not convertible to a float
            If the input value is less than 0.0
        """
        return self._vol_heat_cap

    @vol_heat_cap.setter
    def vol_heat_cap(self, value):
        value = float(value)
        if value < 0.0:
            raise ValueError(f"{value} < 0.0 is not valid")
        self._vol_heat_cap = value

    def conductivity_matrix(self):
        """conductivity matrix of the element.

        Parameters
        ----------
        value : float
                the gradient matix
        value : float
                thm_cond
        value : float
                dz

        Returns
        -------
        conductivity matrix: float
            conductivity matrix of the element
        Raises
        ------
        ValueError
            If the input value is not convertible to a float
            If the input value is less than 0.0
        """
        return self.conductivity_matrix

    def storage_matrix(self):
        """storage matrix of the element.
        Parameters
        -------
        none

        Returns
        -------
        np.ndarray, shape = (2,2)
            storage matrix of the element
        """
        
        n_nodes = len(self._nodes)
        K = np.zeros((n_nodes,n_nodes))

        for s,w in zip(Element._int_pts,Element._int_wts):
            N = shape_matrix(s)
            K += N.T@N*self.dz*w*self.vol_heat_cap

        return K

    