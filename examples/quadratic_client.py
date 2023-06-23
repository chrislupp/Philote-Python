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
from philote_mdo.general import ImplicitClient
from philote_mdo.utils import PairDict

client = ImplicitClient()
client._host = 'localhost:50051'

# connect to the server
client.connect_host()

# transfer the stream options to the server
client.stream_options()

# run setup
client.remote_setup()

# define some inputs
inputs = {
    "a": np.array([1.0]),
    "b": np.array([2.0]),
    "c": np.array([2.0])
}
outputs = {
    "x": np.array([1.0])
}

# run a function evaluation
residuals = client.remote_compute_residuals(inputs, outputs)

print(residuals)

# run a gradient evaluation
# partials = PairDict()
# client.remote_setup_partials()
# partials = client.remote_compute_partials(inputs)

# print(partials)
