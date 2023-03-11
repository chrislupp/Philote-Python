import numpy as np


class ExplicitClient():
    """
    Client for calling explicit analysis discipline servers.
    """

    def __init__(self):
        # continuous inputs (names, shapes, units)
        self._vars = []
        self._vars_shape = {}
        self._vars_units = {}

        # discrete inputs (names, shapes, units)
        self._discrete_vars = []
        self._discrete_vars_shape = {}
        self._discrete_vars_units = {}

        # continous outputs (names, shapes, units)
        self._func = []
        self._func_shape = {}
        self._func_units = {}

        # discrete outputs (names, shapes, units)
        self._discrete_func = []
        self._discrete_func_shape = {}
        self._discrete_func_units = {}

    def remote_setup(self):
        pass

    def remote_compute(self, inputs, outputs):
        array = np.array([])
        shape = list(array.shape)
        data = array.flatten().tolist()

    def remote_partials(self, inputs, jacobian):
        array = np.array([])
        shape = list(array.shape)
        data = array.flatten().tolist()
