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
from unittest.mock import patch
from philote_mdo.openmdao.utils import client_setup, create_local_inputs, assign_global_outputs
import philote_mdo.generated.data_pb2 as data


class TestOpenMdaoUtils(unittest.TestCase):
    """
    Unit tests for the OpenMDAO utilities.
    """

    @patch('philote_mdo.general.DisciplineClient')
    @patch('philote_mdo.openmdao.RemoteExplicitComponent', autospec=True)
    def test_client_setup(self, mock_component_class, mock_discipline_client):
        """
        Tests the client setup utility function.
        """
        # Create an instance of YourComponentClass with a mock client
        comp = mock_component_class.return_value
        comp._client = mock_discipline_client

        # Mock variable and partial metadata
        mock_var_metadata = [data.VariableMetaData(name="x", shape=[2, 2], units="m", type=data.VariableType.kInput)]
        mock_partial_metadata = [data.PartialsMetaData(name="x", subname="y")]

        # configure the mock client to return the mock metadata
        comp._client.get_variable_definitions.return_value = mock_var_metadata
        comp._client._var_meta = mock_var_metadata
        comp._client.get_partials_definitions.return_value = mock_partial_metadata
        comp._client._partials_meta = mock_partial_metadata

        # call the client_setup function
        client_setup(comp)

        # assert that the necessary methods on the mock client were called
        comp._client.run_setup.assert_called_once()
        comp._client.get_variable_definitions.assert_called_once()
        comp._client.get_partials_definitions.assert_called_once()

        # assert that the inputs and outputs were added based on the variable metadata
        comp.add_input.assert_called_once_with("x", shape=(2, 2), units="m")

        # assert that the declare_partials method was called based on the partials metadata
        comp.declare_partials.assert_called_once_with("x", "y")

    def test_create_local_inputs(self):
        """
        Tests the function for creating local inputs.
        """
        # mock input data and variable metadata
        inputs = {'x': 1, 'y': 2, 'z': 3}
        var_meta = [
            data.VariableMetaData(name="x", type=data.VariableType.kInput),
            data.VariableMetaData(name="y", type=data.VariableType.kOutput),  # should be ignored
            data.VariableMetaData(name="z", type=data.VariableType.kInput),
        ]

        # call the create_local_inputs function
        result = create_local_inputs(inputs, var_meta)

        # assert that the local inputs dictionary contains only the expected variables
        self.assertEqual(result, {'x': 1, 'z': 3})

    def test_assign_global_outputs(self):
        """
        Tests the function for assigning global outputs.
        """
        # mock output data and OpenMDAO outputs dictionary
        out = {'x': 1, 'y': 2, 'z': 3}
        outputs = {'x': None, 'y': None, 'z': None}

        # call the assign_global_outputs function
        assign_global_outputs(out, outputs)

        # assert that the OpenMDAO outputs dictionary has been updated
        self.assertEqual(outputs, {'x': 1, 'y': 2, 'z': 3})



if __name__ == "__main__":
    unittest.main(verbosity=2)