import numpy as np
import grpc
from google.protobuf.empty_pb2 import Empty
import philote_mdo.generated.explicit_pb2_grpc as explicit_pb2_grpc
import philote_mdo.generated.options_pb2 as options_pb2
import philote_mdo.generated.array_pb2 as array_pb2


class ExplicitClient():
    """
    Client for calling explicit analysis discipline servers.
    """

    def __init__(self):
        # verbose outputs
        self.verbose = True

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
        self.channel = grpc.insecure_channel(self.host)
        self.stub = explicit_pb2_grpc.ExplicitComponentStub(self.channel)

        if self.verbose:
            print("Set up connection.")

    def _stream_options(self):
        """
        Transmits the stream options for the remote analysis to the server.
        """
        # send the options
        options = options_pb2.Options(num_double=1, num_int=1)
        response = self.stub.SetStreamOptions(options)

        if self.verbose:
            print("Streaming options sent to server.")

    def _setup(self):
        """
        Requests the input and output metadata from the server.
        """
        # stream back the metadata
        for message in self.stub.Setup(Empty()):
            if message.input:
                if message.discrete:
                    self._discrete_vars += [{"name": message.name,
                                            "shape": tuple(message.shape),
                                             "units": message.units}]
                else:
                    self._vars += [{"name": message.name,
                                   "shape": tuple(message.shape),
                                    "units": message.units}]
            else:
                if message.discrete:
                    self._discrete_funcs += [{"name": message.name,
                                             "shape": tuple(message.shape),
                                              "units": message.units}]
                else:
                    self._funcs += [{"name": message.name,
                                    "shape": tuple(message.shape),
                                     "units": message.units}]

        if self.verbose:
            print("Variable metadata received from server.")

            print("Inputs:")
            if self._vars:
                for vars in self._vars:
                    print("    ", vars)
            else:
                print("    None")

            print("Discrete Inputs:")
            if self._discrete_vars:
                for vars in self._discrete_vars:
                    print("    ", vars)
            else:
                print("    None")
            print("Outputs:")
            if self._funcs:
                for func in self._funcs:
                    print("    ", func)
            else:
                print("    None")
            print("Discrete Outputs:")
            if self._discrete_funcs:
                for func in self._discrete_funcs:
                    print("    ", func)
            else:
                print("    None")

    def _compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        """
        Requests and receives the function evaluation from the analysis server
        for a set of inputs (sent to the server).
        """
        if self.verbose:
            print("Started compute method.", end="    ")

        # array of messages used for the send command
        messages = []

        # iterate through all continuous inputs in the dictionary
        for input_name, value in inputs.items():
            # get the beginning and end indices of the chunked arrays
            beg_i = np.arange(0, value.size, self.num_double)

            if beg_i.size == 1:
                end_i = [value.size]
            else:
                end_i = beg_i[1:]

            # iterate through all chunks needed for the current input
            for b, e in zip(beg_i, end_i):
                # create the chunked data
                messages += [array_pb2.Array(name=input_name,
                                             start=b,
                                             end=e,
                                             continuous=value.ravel()[b:e])]

        # iterate through all discrete inputs in the dictionary
        if discrete_inputs:
            for input_name, value in discrete_inputs.items():
                # get the beginning and end indices of the chunked arrays
                beg_i = np.arange(0, value.size, self.num_double)

                if beg_i.size == 1:
                    end_i = [value.size]
                else:
                    end_i = beg_i[1:]

                # iterate through all chunks needed for the current input
                for b, e in zip(beg_i, end_i):
                    # create the chunked data
                    messages += [array_pb2.Array(name=input_name,
                                                 start=b,
                                                 end=e,
                                                 discrete=value.ravel()[b:e])]

        # stream the messages to the server and receive the stream of results
        responses = self.stub.Compute(iter(messages))

        # preallocate outputs and discrete output arrays
        for out in self._funcs:
            outputs[out['name']] = np.zeros(out['shape'])
        for dout in self._discrete_funcs:
            discrete_outputs[dout['name']] = np.zeros(dout['shape'])

        # iterate through the results
        for message in responses:
            # start and end indices for the array chunk
            b = message.start
            e = message.end

            # assign either continuous or discrete data
            if len(message.continuous) > 0:
                outputs[message.name][b:e] = message.continuous
            elif len(message.discrete) > 0:
                discrete_outputs[message.name][b:e] = message.discrete
            else:
                raise ValueError('Expected continuous or discrete variables, '
                                 'but arrays were empty.')

        if self.verbose:
            print("[Complete]")

    def _compute_partials(self, inputs, discrete_inputs, jacobian):
        """
        Requests and receives the gradient evaluation from the analysis server
        for a set of inputs (sent to the server).
        """
        if self.verbose:
            print("Started compute partials method.", end="    ")

        # array of messages used for the send command
        messages = []

        # iterate through all continuous inputs in the dictionary
        for input_name, value in inputs.items():
            # get the beginning and end indices of the chunked arrays
            beg = np.arange(0, value.size, self.num_double)
            end = beg[1:]

            # iterate through all chunks needed for the current input
            for beg, end in zip(beg, end):
                # create the chunked data
                messages += [array_pb2.Array(name=input_name,
                                             start=beg,
                                             end=end,
                                             continuous=value.ravel()[beg:end])]

        # iterate through all discrete inputs in the dictionary
        if discrete_inputs:
            for input_name, value in discrete_inputs.items():
                # get the beginning and end indices of the chunked arrays
                beg = np.arange(0, value.size, self.num_double)
                end = beg[1:]

                # iterate through all chunks needed for the current input
                for beg, end in zip(beg, end):
                    # create the chunked data
                    messages += [array_pb2.Array(name=input_name,
                                                 start=beg,
                                                 end=end,
                                                 discrete=value.ravel()[beg:end])]

        # stream the messages to the server and receive the stream of results
        results = self.stub.ComputePartials(iter(messages))

        # iterate through the results

        if self.verbose:
            print("[Complete]")
