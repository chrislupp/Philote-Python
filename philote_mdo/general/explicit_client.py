import numpy as np
import grpc
import explicit_pb2
import explicit_pb2_grpc
import options_pb2


class ExplicitClient():
    """
    Client for calling explicit analysis discipline servers.
    """

    def __init__(self):
        # host name
        self.host = ""

        # grpc options
        self.grpc_options = []

        # continuous inputs (names, shapes, units)
        self._vars = []

        # discrete inputs (names, shapes, units)
        self._discrete_vars = []

        # continous outputs (names, shapes, units)
        self._func = []

        # discrete outputs (names, shapes, units)
        self._discrete_func = []

    def setup_connection(self):
        self.channel = grpc.insecure_channel(self.host, options=self.options)
        self.stub = explicit_pb2.ExplicitComponentStub(self.channel)

    def remote_initialize(self):
        options = options_pb2.Options(num_double=1, num_int=1)
        response = self.stub.SetStreamOptions(options)

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
