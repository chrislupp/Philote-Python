# Copyright 2022-2023 Christopher A. Lupp
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
#
# This work has been cleared for public release, distribution unlimited, case
# number: AFRL-2023-XXXX. The views expressed are those of the author and do not
# necessarily reflect the official policy or position of the Department of the
# Air Force, the Department of Defense, or the U.S. government.
import numpy as np
from google.protobuf.empty_pb2 import Empty
import philote_mdo.generated.data_pb2 as data
import philote_mdo.generated.disciplines_pb2_grpc as disc
import philote_mdo.utils as utils



class DisciplineClient:
    """
    Base class for analysis discipline clients.
    """

    def __init__(self, channel):
        # verbose outputs
        self.verbose = True

        # grpc options
        self.grpc_options = []

        # discipline properties
        self._is_continuous = False
        self._is_differentiable = False
        self._provides_gradients = False

        # discipline client stub
        self._disc_stub = disc.DisciplineServiceStub(channel)

        # streaming options
        self._stream_options = data.StreamOptions(num_double=1000)

        # variable and partials metadata
        self._var_meta = []
        self._partials_meta = []

    def get_discipline_info(self):
        """
        Gets the discipline properties from the analysis server.
        """
        response = self._disc_stub.GetInfo(Empty())
        self._is_continuous = response[0].continuous
        self._is_differentiable = response[0].differentiable
        self._provides_gradients = response[0].provides_gradients

    def send_stream_options(self):
        """
        Transmits the stream options for the remote analysis to the server.
        """
        self._disc_stub.SetStreamOptions(self._stream_options)

    def send_options(self):
        """
        Sends the discipline options to the analysis server.
        """
        pass

    def run_setup(self):
        """
        Runs the setup function on the analysis server.
        """
        self._disc_stub.Setup(Empty())

    def get_variable_definitions(self):
        """
        Requests the input and output metadata from the server.
        """
        for message in self._disc_stub.DefineVariables(Empty()):
            self._var_meta += [message]

    def get_partials_definitions(self):
        """
        Requests metadata information on the partials from the analysis server.
        """
        for message in self._disc_stub.DefinePartials(Empty()):
            if message.name not in self._partials_meta:
                self._partials_meta += [message]

    def _assemble_input_messages(self, inputs, outputs=None):
        """
        Assembles the messages for transmitting the input variables to the
        server.
        """
        messages = []

        for input_name, value in inputs.items():
            for b, e in utils.get_chunk_indices(value.size, self._stream_options.num_double):
                messages += [data.Array(name=input_name,
                                        start=b,
                                        end=e-1,
                                        type=data.VariableType.kInput,
                                        data=value.ravel()[b:e])]

        if outputs:
            for output_name, value in outputs.items():
                for b, e in utils.get_chunk_indices(value.size, self._stream_options.num_double):
                    messages += [data.Array(name=output_name,
                                            start=b,
                                            end=e-1,
                                            type=data.VariableType.kOutput,
                                            data=value.ravel()[b:e])]

        return messages

    def _recover_outputs(self, responses):
        """
        Recovers the outputs from the stream of responses.
        """
        outputs = {}
        flat_outputs = {}

        discrete_outputs = None
        flat_disc = None

        for out in self._funcs:
            outputs[out['name']] = np.zeros(out['shape'])
            flat_outputs[out['name']] = utils.get_flattened_view(
                outputs[out['name']])

        for dout in self._discrete_funcs:
            discrete_outputs[dout['name']] = np.zeros(dout['shape'])
            flat_disc[dout['name']] = utils.get_flattened_view(
                discrete_outputs[dout['name']])

        for message in responses:
            b = message.start
            e = message.end + 1

            if len(message.data) > 0:
                flat_outputs[message.name][b:e] = message.data
            else:
                raise ValueError('Expected continuous variables, '
                                 'but array is empty.')

        return outputs, discrete_outputs

    def _recover_residuals(self, responses):
        """
        Recovers the residuals from the stream of responses.
        """
        residuals = {}
        flat_residuals = {}

        for res in self._res:
            residuals[res['name']] = np.zeros(res['shape'])
            flat_residuals[res['name']] = utils.get_flattened_view(
                residuals[res['name']])

        for message in responses:
            b = message.start
            e = message.end + 1

            if len(message.data) > 0:
                flat_residuals[message.name][b:e] = message.data
            else:
                raise ValueError('Expected continuous variables for residuals, '
                                 'but array is empty.')

        return residuals

    def _recover_partials(self, responses):
        """
        Recovers the partials from the stream of responses.
        """
        partials = utils.PairDict()
        flat_p = utils.PairDict()

        for pair in self._partials:
            shape = tuple([d['shape']
                           for d in self._funcs if d['name'] == pair[0]])[0]
            shape += tuple([d['shape']
                            for d in self._vars if d['name'] == pair[1]])[0]
            partials[pair] = np.zeros(shape)
            flat_p[pair] = utils.get_flattened_view(partials[pair])

        for message in responses:
            b = message.start
            e = message.end + 1

            if len(message.continuous) > 0:
                flat_p[message.name, message.subname][b:e] = message.data
            else:
                raise ValueError('Expected continuous outputs for the partials,'
                                 ' but array was empty.')

        return partials
