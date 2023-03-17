import numpy as np


class ExplicitClient():
    """
    Client for calling explicit analysis discipline servers.
    """

    def __init__(self):
        # continuous inputs (names, shapes, units)
        self._vars = []

        # discrete inputs (names, shapes, units)
        self._discrete_vars = []

        # continous outputs (names, shapes, units)
        self._func = []

        # discrete outputs (names, shapes, units)
        self._discrete_func = []

    def remote_setup(self):
        messages = []
        input = True
        discrete = True
        name = ""
        shape = (1,)
        units = ''

        for m in messages:
            if input:
                if discrete:
                    self._discrete_vars += {"name": name,
                                            "shape": shape,
                                            "units": units}
                else:
                    self._vars += {"name": name,
                                   "shape": shape,
                                   "units": units}
            else:
                if discrete:
                    self._discrete_funcs += {"name": name,
                                             "shape": shape,
                                             "units": units}
                else:
                    self._funcs += {"name": name,
                                    "shape": shape,
                                    "units": units}

    def remote_compute(self, inputs, outputs):
        array = np.array([])
        shape = list(array.shape)
        data = array.flatten().tolist()

    def remote_partials(self, inputs, jacobian):
        array = np.array([])
        shape = list(array.shape)
        data = array.flatten().tolist()
