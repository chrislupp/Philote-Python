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
import philote_mdo.generated.explicit_pb2_grpc as explicit_pb2_grpc


class ExplicitClient(ClientBase):
    """
    Client for calling explicit analysis discipline servers.
    """

    def __init__(self, channel):
        super().__init__()

        self.stub = explicit_pb2_grpc.ExplicitDisciplineStub(channel)

    def remote_compute(self, inputs, discrete_inputs=None):
        """
        Requests and receives the function evaluation from the analysis server
        for a set of inputs (sent to the server).
        """
        if self.verbose:
            print("Started compute method.")

        # assemble the inputs that need to be sent to the server
        messages = self.assemble_input_messages(inputs, discrete_inputs)

        # stream the messages to the server and receive the stream of results
        responses = self.stub.Functions(iter(messages))

        # parse the outputs
        outputs, discrete_outputs = self.recover_outputs(responses)

        if self.verbose:
            print("    [Complete]")

        return outputs, discrete_outputs

    def remote_compute_partials(self, inputs, discrete_inputs=None):
        """
        Requests and receives the gradient evaluation from the analysis server
        for a set of inputs (sent to the server).
        """
        if self.verbose:
            print("Started compute partials method.")

        # assemble the inputs that need to be sent to the server
        messages = self.assemble_input_messages(inputs, discrete_inputs)

        # stream the messages to the server and receive the stream of results
        responses = self.stub.Gradient(iter(messages))

        # recover the partials from the stream responses
        partials = self.recover_partials(responses)

        if self.verbose:
            print("    [Complete]")

        return partials
