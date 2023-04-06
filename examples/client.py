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
from philote_mdo.utils import PairDict

client = ExplicitClient()
client._host = 'localhost:50051'

# connect to the server
client._connect_host()

# transfer the stream options to the server
client._stream_options()

# run setup
client._remote_setup()

# define some inputs
inputs = {
    "x": np.array([1.0]),
    "y": np.array([2.0])
}
outputs = {}

# run a function evaluation
outputs, discrete_outputs = client._remote_compute(inputs)

print(outputs)

# run a gradient evaluation
# partials = PairDict()
client._setup_remote_partials()
partials = client._remote_compute_partials(inputs)

print(partials)
