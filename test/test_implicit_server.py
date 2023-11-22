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
import numpy.testing as np_testing
from google.protobuf.empty_pb2 import Empty
from philote_mdo.general import ImplicitDiscipline, ImplicitServer
import philote_mdo.generated.data_pb2 as data


class TestImplicitServer(unittest.TestCase):
    """
    Unit tests for the discipline server.
    """

    def test_compute_residuals(self):
        """
        Tests the ComputeResiduals RPC of the Implicit Server.

        This test does not mock out the utility function calls within the
        compute_residuals function, so that the entire solution process is tests
        (the actual residual function is mocked).
        """
        server = ImplicitServer()
        server._stream_opts.num_double = 1
        discipline = server._discipline = ImplicitDiscipline()
        discipline.add_input("x", shape=(2,), units="m")
        discipline.add_input("y", shape=(2,), units="m")
        discipline.add_output("f", shape=(2,), units="m")

        # mock request iterator
        mock_request_iterator = [
            data.Array(name="x", start=0, end=2, type=data.kInput, data=[1.0, 2.0]),
            data.Array(name="y", start=0, end=2, type=data.kInput, data=[3.0, 4.0]),
            data.Array(name="f", start=0, end=2, type=data.kOutput, data=[5.0, 6.0]),
        ]

        # mock inputs, outputs, and residuals
        mock_inputs = {"x": np.array([1.0, 2.0]), "y": np.array([3.0, 4.0])}
        mock_flat_inputs = {"x": np.array([1.0, 2.0]), "y": np.array([3.0, 4.0])}
        mock_outputs = {"f": np.array([5.0, 6.0])}
        mock_flat_outputs = {"f": np.array([5.0, 6.0])}

        # mock function call
        def compute(inputs, outputs, residuals):
            residuals["f"] = np.array([7.0, 8.0])

        server._discipline.compute_residuals = compute

        # call the ComputeResiduals method
        response_generator = server.ComputeResiduals(mock_request_iterator, None)
        result = list(response_generator)

        # assert that the expected residual messages were yielded
        expected_result = [
            data.Array(
                name="f",
                start=0,
                end=1,
                type=data.VariableType.kResidual,
                data=[7.0],
            ),
            data.Array(
                name="f",
                start=1,
                end=2,
                type=data.VariableType.kResidual,
                data=[8.0],
            ),
        ]
        self.assertEqual(result, expected_result)

    # def test_solve_residuals(self):
    #     """
    #     Tests the SolveResiduals RPC of the Implicit Server.
    #     """
    #     pass

    # def test_residual_gradients(self):
    #     """
    #     Tests the ComputeResiduals RPC of the Implicit Server.
    #     """
    #     pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
