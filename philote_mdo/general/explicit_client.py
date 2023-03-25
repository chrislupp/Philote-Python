import numpy as np
import grpc
import explicit_pb2
import explicit_pb2_grpc
import options_pb2
import array_pb2


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

        # maximum number of double values transmitted in one data message
        self.num_double = 100

        # maximum number of integer values transmitted in one data message
        self.num_int = 100

    def _setup_connection(self):
        self.channel = grpc.insecure_channel(self.host, options=self.options)
        self.stub = explicit_pb2_grpc.ExplicitComponentStub(self.channel)

    def _stream_options(self):
        """
        Transmits the stream options for the remote analysis to the server.
        """
        options = options_pb2.Options(num_double=1, num_int=1)
        response = self.stub.SetStreamOptions(options)

    def _setup(self):
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

    def _compute(self, inputs, outputs):
        """
        Requests and receives the function evaluation from the analysis server
        for a set of inputs (sent to the server).
        """
        # array of messages used for the send command
        messages = []

        # iterate through all continuous inputs in the dictionary
        for input_name, value in inputs.items():
            # iterate through all chunks needed for the current input
            for i in range(value.size() // self.num_double):
                # create the chunked data
                messages += [array_pb2.Array(name=input_name,
                                             start=0,
                                             end=0,
                                             continuous=value[0])]

        # iterate through all discrete inputs in the dictionary
        for input_name, value in inputs.items():
            # iterate through all chunks needed for the current input
            for i in range(value.size() // self.num_double):
                # create the chunked data
                messages += [array_pb2.Array(name=input_name,
                                             start=0,
                                             end=0,
                                             continuous=value[0])]

        # stream the messages to the server and receive the stream of results
        results = self.stub.Compute(iter(messages))

    def _compute_partials(self, inputs, jacobian):
        """
        Requests and receives the gradient evaluation from the analysis server
        for a set of inputs (sent to the server).
        """
        # array of messages used for the send command
        messages = []

        # iterate through all continuous inputs in the dictionary
        for input_name, value in inputs.items():
            # iterate through all chunks needed for the current input
            for i in range(value.size() // self.num_double):
                # create the chunked data
                messages += [array_pb2.Array(name=input_name,
                                             start=0,
                                             end=0,
                                             continuous=value[0])]

        # iterate through all discrete inputs in the dictionary
        for input_name, value in inputs.items():
            # iterate through all chunks needed for the current input
            for i in range(value.size() // self.num_double):
                # create the chunked data
                messages += [array_pb2.Array(name=input_name,
                                             start=0,
                                             end=0,
                                             continuous=value[0])]

        # stream the messages to the server and receive the stream of results
        results = self.stub.ComputePartials(iter(messages))
