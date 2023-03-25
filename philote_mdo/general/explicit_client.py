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
        self._funcs = []

        # discrete outputs (names, shapes, units)
        self._discrete_funcs = []

    def setup_connection(self):
        self.channel = grpc.insecure_channel(self.host, options=self.options)
        self.stub = explicit_pb2_grpc.ExplicitComponentStub(self.channel)

    def transmit_stream_options(self):
        """
        Transmits the stream options for the remote analysis to the server.
        """
        options = options_pb2.Options(num_double=1, num_int=1)
        response = self.stub.SetStreamOptions(options)

    def remote_setup(self):
        """
        Requests the input and output metadata from the server.
        """
        # stream back the metadata
        for message in self.stub.Setup(explicit_pb2_grpc.Empty()):
            if message.input:
                if message.discrete:
                    self._discrete_vars += {"name": message.name,
                                            "shape": message.shape,
                                            "units": message.units}
                else:
                    self._vars += {"name": message.name,
                                   "shape": message.shape,
                                   "units": message.units}
            else:
                if message.discrete:
                    self._discrete_funcs += {"name": message.name,
                                             "shape": message.shape,
                                             "units": message.units}
                else:
                    self._funcs += {"name": message.name,
                                    "shape": message.shape,
                                    "units": message.units}

    def remote_compute(self, inputs, outputs):
        array = np.array([])
        shape = list(array.shape)
        data = array.flatten().tolist()

    def remote_partials(self, inputs, jacobian):
        array = np.array([])
        shape = list(array.shape)
        data = array.flatten().tolist()
