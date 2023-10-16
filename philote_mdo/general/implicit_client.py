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
#
#
# This work has been cleared for public release, distribution unlimited, case
# number: AFRL-2023-XXXX. The views expressed are those of the author and do not
# necessarily reflect the official policy or position of the Department of the
# Air Force, the Department of Defense, or the U.S. government.
import grpc
from philote_mdo.general.client_base import ClientBase
import philote_mdo.generated.implicit_pb2_grpc as implicit_pb2_grpc


class ImplicitClient(ClientBase):
    """
    Python client for implicit Philote discipline servers. 
    """

    def __init__(self, channel):
        super().__init__()
        self.stub = implicit_pb2_grpc.ImplicitDisciplineStub(channel)

    def remote_compute_residuals(self, inputs, outputs, discrete_inputs=None,
                                 discrete_outputs=None):
        """
        Requests and receives the residual evaluation from the analysis server
        for a set of inputs and outputs (sent to the server).
        """
        if self.verbose:
            print("Started apply nonlinear method.", end="")

        # assemble the inputs that need to be sent to the server
        messages = self.assemble_input_messages(inputs, discrete_inputs,
                                                outputs, discrete_outputs)

        # stream the messages to the server and receive the stream of results
        responses = self.stub.Residuals(iter(messages))

        # parse the outputs
        residuals = self.recover_residuals(responses)

        if self.verbose:
            print("    [Complete]")

        return residuals

    def remote_solve_nonlinear(self):
        """
        """
        pass

    def remote_linearize(self):
        """
        """
        pass
