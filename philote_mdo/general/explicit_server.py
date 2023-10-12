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
from philote_mdo.utils import get_chunk_indices


class ExplicitServer(DisciplineServer, disc.ExplicitServiceServicer):
    """
    Base class for remote explicit components.
    """

    def __init__(self):
        super().__init__()

    def ComputeFunction(self, request_iterator, context):
        """
        Computes the function evaluation and sends the result to the client.
        """
        inputs = {}
        flat_inputs = {}
        outputs = {}

        self.preallocate_inputs(inputs, flat_inputs)
        self.process_inputs(request_iterator, flat_inputs)
        self._discipline.compute(inputs, outputs)

        for output_name, value in outputs.items():
            # iterate through all chunks needed for the current output
            for b, e in get_chunk_indices(value.size, self._stream_opts.num_double):
                yield data.Array(name=output_name,
                                 start=b,
                                 end=e-1,
                                 data=value.ravel()[b:e])

    def ComputeGradient(self, request_iterator, context):
        """
        Computes the gradient evaluation and sends the result to the client.
        """
        inputs = {}
        flat_inputs = {}
        self.preallocate_inputs(inputs, flat_inputs)
        jac = self.preallocate_partials()
        self.process_inputs(request_iterator, flat_inputs)
        self.compute_partials(inputs, jac)

        for jac, value in jac.items():
            # iterate through all chunks needed for the current partials
            for b, e in get_chunk_indices(value.size, self.num_double):
                yield data.Array(name=jac[0],
                                 subname=jac[1],
                                 start=b,
                                 end=e-1,
                                 data=value.ravel()[b:e])
