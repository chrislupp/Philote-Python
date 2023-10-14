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
import philote_mdo.general as pmdo
from philote_mdo.utils import get_chunk_indices


class ImplicitServer(pmdo.DisciplineServer, disc.ImplicitDisciplineServicer):
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
        residuals = {}

        # preallocate the inputs for the implicit discipline
        self.preallocate_inputs(inputs, flat_inputs, outputs, flat_outputs)
        self.process_inputs(request_iterator, flat_inputs, flat_outputs)

        # call the user-defined compute function
        self._discipline.compute_residuals(inputs, outputs, residuals)

        for res_name, value in residuals.items():
            for b, e in get_chunk_indices(value.size, self.num_double):
                yield data.Array(name=res_name,
                                      start=b,
                                      end=e,
                                      type=data.kResidual,
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

        self.preallocate_inputs(inputs, flat_inputs, outputs, flat_outputs)

        self.process_inputs(request_iterator, flat_inputs, flat_outputs)

        # call the user-defined compute function
        self._discipline.solve_residuals(inputs, outputs)

        for output_name, value in outputs.items():
            for b, e in get_chunk_indices(value.size, self.num_double):
                yield data.Array(name=output_name,
                                      start=b,
                                      end=e,
                                      continuous=value.ravel()[b:e])

    def ResidualGradients(self, request_iterator, context):
        """
        Computes the residual gradients and sends the results to the client.
        """
        # inputs and outputs
        inputs = {}
        flat_inputs = {}
        outputs = {}
        flat_outputs = {}

        # preallocate the input and discrete input arrays
        self.preallocate_inputs(inputs, flat_inputs, outputs, flat_outputs)
        jac = self.preallocate_partials()
        self.process_inputs(request_iterator, flat_inputs, flat_outputs)

        # call the user-defined compute_partials function
        self._discipline.linearize(inputs, jac)

        for jac, value in jac.items():
            for b, e in get_chunk_indices(value.size, self.num_double):
                yield data.Array(name=jac[0],
                                      subname=jac[1],
                                      start=b,
                                      end=e,
                                      continuous=value.ravel()[b:e])

    # def MatrixFreeGradients(self, request_iterator, context):
    #     """
    #     """
    #     pass