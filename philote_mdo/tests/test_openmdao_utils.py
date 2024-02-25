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

import philote_mdo.generated.data_pb2
from philote_mdo.openmdao.utils import openmdao_client_setup


class TestOpenMdaoUtils(unittest.TestCase):
    """
    Tests the utility functions used by the OpenMDAO clients and servers.
    """

    def test_openmdao_client_setup(self):
        self.comp = Mock()
        var1 = Mock()
        var1.name = "var1"
        var1.units = "m"
        var1.type = philote_mdo.generated.data_pb2.kInput
        var1.shape = [2]

        var2 = Mock()
        var2.name = "var2"
        var2.units = None
        var2.type = philote_mdo.generated.data_pb2.kOutput
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
