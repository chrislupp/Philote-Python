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
import unittest
from unittest.mock import Mock

import numpy as np
from scipy.optimize import rosen, rosen_der

from google.protobuf.empty_pb2 import Empty

from philote_mdo.general import ExplicitDiscipline, ExplicitServer
import philote_mdo.generated.data_pb2 as data


class TestExplicitServer(unittest.TestCase):
    """
    Unit tests for the discipline server.
    """
    def test_compute_function(self):
        """
        Tests the ComputeFunction RPC of the Explicit Server.
        """
        server = ExplicitServer()
        discipline = server._discipline = ExplicitDiscipline()
        server._stream_opts.num_double = 3
        discipline.add_input('x', shape=(5,), units="")
        discipline.add_output('f', shape=(2,), units="")

        context = Mock()
        request_iterator = [
            data.Array(start=0, end=2, data=[0.5, 1.5, 3.5],
                       type=data.VariableType.kInput, name="x"),
            data.Array(start=3, end=4, data=[4.5, 5.5],
                       type=data.VariableType.kInput, name="x")
        ]

        # mock function call
        def compute(inputs, outputs):
            outputs["f"] = np.array([rosen(inputs['x']), rosen(inputs['x'].T - 2.0)])
        server._discipline.compute = compute

        # call the function
        response_generator = server.ComputeFunction(request_iterator, context)
        responses = list(response_generator)

        # check that there is only one response
        self.assertEqual(len(responses), 1)

        # check the function value
        response = responses[0]
        self.assertEqual(response.name, "f")
        self.assertEqual(response.start, 0)
        self.assertEqual(response.end, 1)
        self.assertEqual(response.data[0], 28094.0)
        self.assertEqual(response.data[1], 1686.0)
