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
import philote_mdo.generated.explicit_pb2_grpc as explicit_pb2_grpc
import philote_mdo.generated.array_pb2 as array_pb2
from philote_mdo.general.server_base import ServerBase
from philote_mdo.utils import get_chunk_indicies


class ExplicitServer(ServerBase, explicit_pb2_grpc.ExplicitDisciplineServicer):
    """
    Base class for remote explicit components.
    """

    def __init__(self):
        super().__init__()

    def Functions(self, request_iterator, context):
        """
        Computes the function evaluation and sends the result to the client.
        """
        # inputs and outputs
        inputs = {}
        flat_inputs = {}
        discrete_inputs = {}
        flat_disc = {}
        outputs = {}
        discrete_outputs = {}

        # preallocate the input and discrete input arrays
        self.preallocate_inputs(inputs, flat_inputs,
                                discrete_inputs, flat_disc)

        # process inputs
        self.process_inputs(request_iterator, flat_inputs, flat_disc)

        # call the user-defined compute function
        if discrete_inputs or discrete_outputs:
            self.compute(inputs, outputs, discrete_inputs, discrete_outputs)
        else:
            self.compute(inputs, outputs)

        # iterate through all continuous outputs in the dictionary
        for output_name, value in outputs.items():

            # iterate through all chunks needed for the current input
            for b, e in get_chunk_indicies(value.size, self.num_double):
                # create the chunked data
                yield array_pb2.Array(name=output_name,
                                      start=b,
                                      end=e,
                                      continuous=value.ravel()[b:e])

        # iterate through all discrete outputs in the dictionary
        for doutput_name, value in discrete_outputs.items():

            # iterate through all chunks needed for the current input
            for b, e in get_chunk_indicies(value.size, self.num_double):
                # create the chunked data
                yield array_pb2.Array(name=doutput_name,
                                      start=b,
                                      end=e,
                                      discrete=value.ravel()[b:e])

    def Gradient(self, request_iterator, context):
        """
        Computes the gradient evaluation and sends the result to the client.
        """
        # inputs and outputs
        inputs = {}
        flat_inputs = {}
        discrete_inputs = {}
        flat_disc = {}

        # preallocate the input and discrete input arrays
        self.preallocate_inputs(inputs, flat_inputs,
                                discrete_inputs, flat_disc)

        # preallocate the partials
        jac = self.preallocate_partials()

        # process inputs
        self.process_inputs(request_iterator, flat_inputs, flat_disc)

        # call the user-defined compute_partials function
        if discrete_inputs:
            self.compute_partials(inputs, jac, discrete_inputs)
        else:
            self.compute_partials(inputs, jac)

        # iterate through all continuous outputs in the dictionary
        for jac, value in jac.items():

            # iterate through all chunks needed for the current input
            for b, e in get_chunk_indicies(value.size, self.num_double):
                # create and send the chunked data
                yield array_pb2.Array(name=jac[0],
                                      subname=jac[1],
                                      start=b,
                                      end=e,
                                      continuous=value.ravel()[b:e])

    def initialize(self):
        pass

    def setup(self):
        pass

    def compute(self, inputs, outputs, discrete_inputs=None,
                discrete_outputs=None):
        pass

    def compute_partials(self, inputs, partials, discrete_inputs=None):
        pass
