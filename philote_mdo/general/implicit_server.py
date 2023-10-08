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
import philote_mdo.generated.disciplines_pb2_grpc as disc
import philote_mdo.generated.data_pb2 as data
from philote_mdo.general.discipline_server import DisciplineServer
from philote_mdo.utils import get_chunk_indicies


class ImplicitServer(DisciplineServer, disc.ImplicitDisciplineServicer):
    """
    Base class for creating an implicit discipline server.
    """

    def __init__(self):
        super().__init__()
        self._implicit = True

    def Residuals(self, request_iterator, context):
        """
        Computes the residuals and sends the results to the client.
        """
        # inputs and outputs
        inputs = {}
        flat_inputs = {}
        outputs = {}
        flat_outputs = {}
        discrete_inputs = {}
        flat_disc_in = {}
        discrete_outputs = {}
        flat_disc_out = {}
        residuals = {}

        # preallocate the inputs for the implicit discipline
        self.preallocate_inputs(inputs, flat_inputs,
                                discrete_inputs, flat_disc_in,
                                outputs, flat_outputs,
                                discrete_outputs, flat_disc_out)

        # process inputs
        self.process_inputs(request_iterator, flat_inputs, flat_disc_in,
                            flat_outputs, flat_disc_out)

        # call the user-defined compute function
        if discrete_inputs or discrete_outputs:
            self.compute_residuals(inputs, outputs, residuals,
                                   discrete_inputs, discrete_outputs)
        else:
            self.compute_residuals(inputs, outputs, residuals)

        # iterate through all continuous outputs in the dictionary
        for res_name, value in residuals.items():
            # iterate through all chunks needed for the current input
            for b, e in get_chunk_indicies(value.size, self.num_double):
                # create the chunked data
                yield array_pb2.Array(name=res_name,
                                      start=b,
                                      end=e,
                                      type=VariableType.kResidual,
                                      continuous=value.ravel()[b:e])

    def Solve(self, request_iterator, context):
        """
        Solves the implicit discipline so that the residuals are driven to zero.
        """
        # inputs and outputs
        inputs = {}
        flat_inputs = {}
        outputs = {}
        flat_outputs = {}
        discrete_inputs = {}
        flat_disc_in = {}
        discrete_outputs = {}
        flat_disc_out = {}

        # preallocate the inputs for the implicit discipline
        self.preallocate_inputs(inputs, flat_inputs,
                                discrete_inputs, flat_disc_in,
                                outputs, flat_outputs,
                                discrete_outputs, flat_disc_out)

        # process inputs for the implicit discipline
        self.process_inputs(request_iterator, flat_inputs, flat_disc_in,
                            flat_outputs, flat_disc_out)

        # call the user-defined compute function
        self.solve_nonlinear(inputs, outputs,
                             discrete_inputs, discrete_outputs)

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

    def ResidualGradients(self, request_iterator, context):
        """
        Computes the residual gradients and sends the results to the client.
        """
        # inputs and outputs
        inputs = {}
        flat_inputs = {}
        outputs = {}
        flat_outputs = {}
        discrete_inputs = {}
        flat_disc_in = {}
        flat_disc_out = {}

        # preallocate the input and discrete input arrays
        self.preallocate_inputs(inputs, flat_inputs,
                                discrete_inputs, flat_disc_in,
                                outputs, flat_outputs)

        # preallocate the partials
        jac = self.preallocate_partials()

        # process inputs for the implicit discipline
        self.process_inputs(request_iterator, flat_inputs, flat_disc_in,
                            flat_outputs, flat_disc_out)

        # call the user-defined compute_partials function
        self.linearize(inputs, jac, discrete_inputs)

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

    # def MatrixFreeGradients(self, request_iterator, context):
    #     """
    #     """
    #     pass

    # user defined functions (will be overloaded)

    def initialize(self):
        """
        """
        pass

    def setup(self):
        """
        """
        pass

    def setup_partials(self):
        """
        """
        pass

    def compute_residuals(self, inputs, outputs, residuals,
                          discrete_inputs=None, discrete_outputs=None):
        """
        """
        pass

    def solve_nonlinear(self, inputs, outputs):
        """
        """
        pass

    def linearize(self, inputs, outputs, partials):
        """
        """
        pass

    def apply_linear(self, inputs, outputs,
                     d_inputs, d_outputs, d_residuals, mode):
        """
        """
        pass
