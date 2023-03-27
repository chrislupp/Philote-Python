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
from concurrent import futures
import philote_mdo.generated.explicit_pb2_grpc as explicit_pb2_grpc


def run_server(service, port='50051', max_workers=10):
    """
    Helper function for running an analysis server.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

    # add an explicit or implicit server
    if isinstance(service, explicit_pb2_grpc.ExplicitComponentServicer):
        explicit_pb2_grpc.add_ExplicitComponentServicer_to_server(
            service, server)
    else:
        raise ValueError('Unexpected object type provided for variable '
                         '"service".')

    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Started server. Press 'q' and hit enter to stop the server.")

    try:
        while True:
            user_input = input()
            if user_input == 'q':
                break
    except KeyboardInterrupt:
        pass

    print("Stopping the server...")
    server.stop(0)
