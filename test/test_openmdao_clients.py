# Philote-Python
#
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
# number: AFRL-2023-5713.
#
# The views expressed are those of the authors and do not reflect the
# official guidance or position of the United States Government, the
# Department of Defense or of the United States Air Force.
#
# Statement from DoD: The Appearance of external hyperlinks does not
# constitute endorsement by the United States Department of Defense (DoD) of
# the linked websites, of the information, products, or services contained
# therein. The DoD does not exercise any editorial, security, or other
# control over the information you may find at these locations.
import unittest
from unittest.mock import patch, Mock
from philote_mdo.openmdao import RemoteExplicitComponent
import philote_mdo.generated.data_pb2 as data


class TestOpenMdaoClients(unittest.TestCase):
    """
    Unit tests for the OpenMDAO clients/components.
    """

    @patch('philote_mdo.openmdao.utils.assign_global_outputs')
    def test_compute_after_setup(self, mock_assign_global_outputs):
        # Mock gRPC channel
        channel_mock = Mock()

        # Create an instance of RemoteExplicitComponent
        comp = RemoteExplicitComponent(channel=channel_mock)

        # Mock client and set the _var_meta attribute
        comp._client = Mock()
        comp._client._var_meta = [
            data.VariableMetaData(name="x", type=data.kInput),
            data.VariableMetaData(name="y", type=data.kOutput),
        ]

        # Mock inputs and outputs dictionaries
        inputs = {'x': 1}
        outputs = {'y': None}

        # Configure the Mock object to support iteration
        comp._client.run_compute.return_value = {'y': 42}

        # Call the compute method
        comp.compute(inputs, outputs)

        # Assert that the necessary methods were called
        comp._client.run_compute.assert_called_once_with({'x': 1})
        self.assertEqual(outputs["y"], 42.0)


    @patch('philote_mdo.openmdao.utils.assign_global_outputs')
    def test_compute_partials_after_setup(self, mock_assign_global_outputs):
        # Mock gRPC channel
        channel_mock = Mock()

        # Create an instance of RemoteExplicitComponent
        comp = RemoteExplicitComponent(channel=channel_mock)

        # Mock client and set the _var_meta attribute
        comp._client = Mock()
        comp._client._var_meta = [
            data.VariableMetaData(name="x", type=data.kInput),
            data.VariableMetaData(name="y", type=data.kOutput),
        ]

        # Mock inputs and partials dictionaries
        inputs = {'x': 1}
        partials = {'y': None}

        # Configure the Mock object to support iteration
        comp._client.run_compute_partials.return_value = {('y', 'x'): 42}

        # Call the compute_partials method
        comp.compute_partials(inputs, partials)

        # Assert that the necessary methods were called
        comp._client.run_compute_partials.assert_called_once_with({'x': 1})
        self.assertEqual(partials[("y", "x")], 42.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)