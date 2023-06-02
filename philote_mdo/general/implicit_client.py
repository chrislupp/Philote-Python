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
import grpc
from philote_mdo.general.client_base import ClientBase
import philote_mdo.generated.implicit_pb2_grpc as implicit_pb2_grpc


class ImplicitClient():
    """
    Python client for implicit Philote discipline servers. 
    """

    def __init__():
        """
        """
        super().__init__()

    def connect_host(self):
        self.channel = grpc.insecure_channel(self._host)
        self.stub = implicit_pb2_grpc.ImplicitDisciplineStub(self.channel)

        if self.verbose:
            print("Set up connection.")

    def apply_nonlinear(self):
        """
        """
        pass

    def solve_nonlinear(self):
        """
        """
        pass

    def linearize(self):
        """
        """
        pass
