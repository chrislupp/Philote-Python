import grpc
import explicit_pb2
import explicit_pb2_grpc
import metadata_pb2
import array_pb2


class ExplicitServer(explicit_pb2_grpc.ExplicitComponentServicer):
    """
    Base class for remote explicit components.
    """

    def __init__(self):
        self.num_double = 100
        self.num_int = 100

    def SetStreamOptions(self, request, context):
        """
        Receives options from the client on how data will be transmitted to and
        received from the client. The options are stores locally for use in the
        compute routines.
        """
        # set the maximum size of arrays that will be sent over the wire in one
        # chunk
        self.num_double = request.num_double
        self.num_int = request.num_int

        # continuous inputs (names, shapes, units)
        self._vars = []

        # discrete inputs (names, shapes, units)
        self._discrete_vars = []

        # continous outputs (names, shapes, units)
        self._funcs = []

        # discrete outputs (names, shapes, units)
        self._discrete_funcs = []

        return explicit_pb2_grpc.Empty()

    def Setup(self, request, context):
        """
        Transmits setup information about the analysis discipline to the client.
        """
        # transmit the continuous input metadata
        for var in self._vars:
            yield metadata_pb2.VariableMetaData(discrete=False,
                                                input=True,
                                                name=var['name'],
                                                shape=var['shape'],
                                                units=var['units'])
        # transmit the discrete input metadata
        for var in self._discrete_vars:
            yield metadata_pb2.VariableMetaData(discrete=True,
                                                input=True,
                                                name=var['name'],
                                                shape=var['shape'],
                                                units=var['units'])
        # transmit the continuous output metadata
        for func in self._funcs:
            yield metadata_pb2.VariableMetaData(discrete=False,
                                                input=False,
                                                name=func['name'],
                                                shape=func['shape'],
                                                units=func['units'])
        # transmit the discrete output metadata
        for func in self._discrete_funcs:
            yield metadata_pb2.VariableMetaData(discrete=True,
                                                input=False,
                                                name=func['name'],
                                                shape=func['shape'],
                                                units=func['units'])

    def Compute(self, request_iterator, context):
        """
        Computes the function evaluation and sends the result to the client.
        """
        # inputs and outputs
        inputs = {}
        discrete_inputs = {}
        outputs = {}
        discrete_outputs = {}

        # process inputs
        for message in request_iterator:
            # start and end indices for the array chunk
            start = message.start
            end = message.end

            # assign either continuous or discrete data
            if message.continous:
                inputs[message.name][start:end] = message.continuous
            elif message.discrete:
                discrete_inputs[message.name][start:end] = message.discrete
            else:
                raise ValueError('Expected continuous or discrete variables, '
                                 'but arrays were empty.')

        # call the user-defined compute function
        self.compute(inputs, outputs, discrete_inputs, discrete_outputs)

        # send outputs to the client
        # iterate through all continuous outputs in the dictionary
        for output_name, value in outputs.items():
            # iterate through all chunks needed for the current input
            for i in range(value.size() // self.num_double):
                # create and send the chunked data
                yield array_pb2.Array(name=output_name,
                                      start=0,
                                      end=0,
                                      continuous=value.ravel[0:0])

        # iterate through all discrete outputs in the dictionary
        for output_name, value in discrete_outputs.items():
            # iterate through all chunks needed for the current input
            for i in range(value.size() // self.num_double):
                # create and send the chunked data
                yield array_pb2.Array(name=output_name,
                                      start=0,
                                      end=0,
                                      discrete=value.ravel[0:0])

    def ComputePartials(self, request_iterator, context):
        """
        Computes the gradient evaluation and sends the result to the client.
        """
        # inputs and outputs
        inputs = {}
        discrete_inputs = {}
        jacobian = {}

        # process inputs
        for message in request_iterator:
            # start and end indices for the array chunk
            start = message.start
            end = message.end

            # assign either continuous or discrete data
            if message.continous:
                inputs[message.name][start:end] = message.continuous
            elif message.discrete:
                discrete_inputs[message.name][start:end] = message.discrete
            else:
                raise ValueError('Expected continuous or discrete variables, '
                                 'but arrays were empty.')

        # call the user-defined compute_partials function
        self.compute_partials(inputs, discrete_inputs, jacobian)

        # send outputs to the client
        # iterate through all continuous outputs in the dictionary
        for output_name, value in jacobian.items():
            # iterate through all chunks needed for the current input
            for i in range(value.size() // self.num_double):
                # create and send the chunked data
                yield array_pb2.Array(name=output_name,
                                      start=0,
                                      end=0,
                                      continuous=value.ravel[0:0])

    def setup(self):
        pass

    def compute(self, inputs, outputs, discrete_inputs=None,
                discrete_outputs=None):
        pass

    def compute_partials(self, inputs, jacobian, discrete_inputs=None):
        pass
