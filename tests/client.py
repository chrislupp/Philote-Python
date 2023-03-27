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
from philote_mdo.general import ExplicitClient


client = ExplicitClient()
client.host = 'localhost:50051'

# connect to the server
client._setup_connection()

# transfer the stream options to the server
client._stream_options()

# run setup
client._setup()

# define some inputs
inputs = {
    "x": np.array([1.0]),
    "y": np.array([2.0])
}
outputs = {}

client._compute(inputs, outputs)

print(outputs)
