# Copyright 2022-2023 Christopher A. Lupp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import grpc
from google.protobuf.empty_pb2 import Empty
import philote_mdo.generated.explicit_pb2_grpc as explicit_pb2_grpc
import philote_mdo.generated.options_pb2 as options_pb2
import philote_mdo.generated.array_pb2 as array_pb2
from philote_mdo.utils import PairDict, get_chunk_indicies, get_flattened_view

class ExplicitClient:
    """
    Client for calling explicit analysis discipline servers.
    """

    def __init__(self):
        # verbose outputs
        self.verbose = True

        # host name
        self._host = ""

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

        # list of all defined partials
        self._partials = []

        # maximum number of double values transmitted in one data message
        self.num_double = 100

        # maximum number of integer values transmitted in one data message
        self.num_int = 100

    def _connect_host(self):
        self.channel = grpc.insecure_channel(self._host)
        self.stub = explicit_pb2_grpc.ExplicitDisciplineStub(self.channel)

        if self.verbose:
            print("Set up connection.")

    def _stream_options(self):
        """
        Transmits the stream options for the remote analysis to the server.
        """
        # send the options
        options = options_pb2.Options(num_double=self.num_double, num_int=self.num_int)
        response = self.stub.SetStreamOptions(options)

        if self.verbose:
            print("Streaming options sent to server.")

    def _remote_setup(self):
        """
        Requests the input and output metadata from the server.
        """
        # stream back the metadata
        for message in self.stub.DefineVariables(Empty()):
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

    def _setup_remote_partials(self):
        """
        Requests metadata information on the partials from the analysis server.
        """
        for message in self.stub.DefinePartials(Empty()):
            if (message.name, message.subname) not in self._partials:
                self._partials += [(message.name, message.subname)]

    def _remote_compute(self, inputs, discrete_inputs=None):
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

            # iterate through all chunks needed for the current input
            for b, e in get_chunk_indicies(value.size, self.num_double):
                # create the chunked data
                messages += [array_pb2.Array(name=input_name,
                                             start=b,
                                             end=e,
                                             continuous=value.ravel()[b:e])]

        # iterate through all discrete inputs in the dictionary
        if discrete_inputs:
            for input_name, value in discrete_inputs.items():

                # iterate through all chunks needed for the current input
                for b, e in get_chunk_indicies(value.size, self.num_double):
                    # create the chunked data
                    messages += [array_pb2.Array(name=input_name,
                                                 start=b,
                                                 end=e,
                                                 discrete=value.ravel()[b:e])]

        # stream the messages to the server and receive the stream of results
        responses = self.stub.Functions(iter(messages))

        outputs = {}
        flat_outputs = {}

        discrete_outputs = None
        flat_disc = None

        # preallocate outputs and discrete output arrays
        for out in self._funcs:
            outputs[out['name']] = np.zeros(out['shape'])
            flat_outputs[out['name']] = get_flattened_view(outputs[out['name']])

        for dout in self._discrete_funcs:
            discrete_outputs[dout['name']] = np.zeros(dout['shape'])
            flat_disc[dvar['name']] = get_flattened_view(discrete_outputs[dout['name']])

        # iterate through the results
        for message in responses:
            # start and end indices for the array chunk
            b = message.start
            e = message.end

            # assign either continuous or discrete data
            if len(message.continuous) > 0:
                flat_outputs[message.name][b:e] = message.continuous
            elif len(message.discrete) > 0:
                flat_disc[message.name][b:e] = message.discrete
            else:
                raise ValueError('Expected continuous or discrete variables, '
                                 'but arrays were empty.')

        if self.verbose:
            print("[Complete]")

        return outputs, discrete_outputs

    def _remote_compute_partials(self, inputs, discrete_inputs=None):
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

            # iterate through all chunks needed for the current input
            for b, e in get_chunk_indicies(value.size, self.num_double):
                # create the chunked data
                messages += [array_pb2.Array(name=input_name,
                                             start=b,
                                             end=e,
                                             continuous=value.ravel()[b:e])]

        # iterate through all discrete inputs in the dictionary
        if discrete_inputs:
            for input_name, value in discrete_inputs.items():

                # iterate through all chunks needed for the current input
                for b, e in get_chunk_indicies(value.size, self.num_double):
                    # create the chunked data
                    messages += [array_pb2.Array(name=input_name,
                                                 start=b,
                                                 end=e,
                                                 discrete=value.ravel()[b:e])]

        # stream the messages to the server and receive the stream of results
        responses = self.stub.Gradient(iter(messages))

        # preallocate the partials
        partials = PairDict()
        flat_p = PairDict()

        for pair in self._partials:
            shape = tuple([d['shape']
                           for d in self._funcs if d['name'] == pair[0]])[0]
            shape += tuple([d['shape']
                            for d in self._vars if d['name'] == pair[1]])[0]
            partials[pair] = np.zeros(shape)
            flat_p[pair] = get_flattened_view(partials[pair])


        # iterate through the results
        for message in responses:
            # start and end indices for the array chunk
            b = message.start
            e = message.end

            # assign either continuous or discrete data
            if len(message.continuous) > 0:
                flat_p[message.name, message.subname][b:e] = message.continuous
            else:
                raise ValueError('Expected continuous outputs for the partials,'
                                 ' but arrays were empty.')

        if self.verbose:
            print("[Complete]")

        return partials
