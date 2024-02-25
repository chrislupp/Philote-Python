# Philote-Python
#
# Copyright 2022-2024 Christopher A. Lupp
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
from unittest.mock import Mock
import numpy as np

from philote_mdo.generated.data_pb2 import kInput, kOutput
from philote_mdo.openmdao.utils import openmdao_client_setup, create_local_inputs


class TestOpenMdaoUtils(unittest.TestCase):
    """
    Tests the utility functions used by the OpenMDAO clients and servers.
    """

    def test_openmdao_client_setup(self):
        self.comp = Mock()
        var1 = Mock()
        var1.name = "var1"
        var1.units = "m"
        var1.type = kInput
        var1.shape = [2]

        var2 = Mock()
        var2.name = "var2"
        var2.units = None
        var2.type = kOutput
        var2.shape = [1]

        self.comp._client._var_meta = [var1, var2]

        openmdao_client_setup(self.comp)

        self.comp._client.run_setup.assert_called_once()
        self.comp._client.get_variable_definitions.assert_called_once()

        expected_calls = [
            ("add_input", ("var1",), {"shape": (2,), "units": "m"}),
            ("add_output", ("var2",), {"shape": (1,), "units": None})
        ]
        for call in expected_calls:
            getattr(self.comp, call[0]).assert_called_once_with(*call[1], **call[2])

    def test_create_local_inputs(self):
        # Define sample inputs and var_meta
        inputs = {'parent.var1': 10, 'parent.var2': 20, 'parent.var3': 30}

        # case 1: 3 inputs
        # ----------------

        # create variable metadata
        var1 = Mock()
        var1.name = "var1"
        var1.type = kInput

        var2 = Mock()
        var2.name = "var2"
        var2.type = kInput

        var3 = Mock()
        var3.name = "var3"
        var3.type = kInput

        var_meta = [var1, var2, var3]

        # Call the function
        local_inputs = create_local_inputs("parent", inputs, var_meta)

        # Assert that only relative variable names are included in local_inputs
        self.assertIn('var1', local_inputs)
        self.assertIn('var2', local_inputs)
        self.assertIn('var3', local_inputs)
        self.assertEqual(local_inputs['var1'], 10)
        self.assertEqual(local_inputs['var2'], 20)
        self.assertEqual(local_inputs['var3'], 30)

        # case 2: 2 inputs, 1 output
        # --------------------------

    # def test_create_local_outputs(self):
    #     pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
