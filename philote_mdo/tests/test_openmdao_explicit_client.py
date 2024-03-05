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
from unittest.mock import Mock, MagicMock, patch
import numpy as np
import philote_mdo.generated.data_pb2 as data
from philote_mdo.openmdao import RemoteExplicitComponent


def mock_get_options(arg):
    return data.OptionsList(options=[], type=[])


class TestOpenMdaoExplicitClient(unittest.TestCase):
    """
    Unit tests for the OpenMDAO explicit component/client.
    """

    # def test_initialize(self):
    #     """
    #     Tests the initialize function of the OpenMDAO Explicit Client.
    #     """
    #     pass

    @patch('philote_mdo.openmdao.utils.client_setup')
    def test_setup(self, mock_openmdao_client_setup):
        """
        Tests the setup function of the OpenMDAO Explicit Client.
        """
        var1 = Mock()
        var1.name = "input1"
        var1.units = "m"
        var1.type = data.kInput
        var1.shape = [1]

        var2 = Mock()
        var2.name = "input2"
        var2.units = None
        var2.type = data.kInput
        var2.shape = [1]

        var3 = Mock()
        var3.name = "output1"
        var3.units = None
        var3.type = data.kOutput
        var3.shape = [1]

        var4 = Mock()
        var4.name = "output2"
        var4.units = None
        var4.type = data.kOutput
        var4.shape = [1]

        mock_channel = Mock()
        component = RemoteExplicitComponent(channel=mock_channel)
        component._client = Mock()
        component._client._var_meta = [var1, var2, var3, var4]

        # call the function
        component.setup()

        # check that the setup utility function was called
        mock_openmdao_client_setup.assert_called_once_with(component)

    @patch('philote_mdo.openmdao.utils.client_setup_partials')
    def test_setup_partials(self, mock_openmdao_client_setup_partials):
        """
        Tests the setup partials function of the OpenMDAO Explicit Client.
        """
        par1 = Mock()
        par1.name = "partial1"
        par1.subname = "subpartial1"

        par2 = Mock()
        par2.name = "partial2"
        par2.subname = "subpartial2"

        mock_channel = Mock()
        component = RemoteExplicitComponent(channel=mock_channel)
        component._client = Mock()
        component._client._partials_meta = [par1, par2]

        # call the function
        component.setup_partials()

        # check that the setup utility function was called
        mock_openmdao_client_setup_partials.assert_called_once_with(component)

    def test_compute_function(self):
        """
        Tests the compute function of the OpenMDAO explicit client.
        """
        var1 = Mock()
        var1.name = "input1"
        var1.units = "m"
        var1.type = data.kInput
        var1.shape = [1]

        var2 = Mock()
        var2.name = "input2"
        var2.units = None
        var2.type = data.kInput
        var2.shape = [1]

        var3 = Mock()
        var3.name = "output1"
        var3.units = None
        var3.type = data.kOutput
        var3.shape = [1]

        var4 = Mock()
        var4.name = "output2"
        var4.units = None
        var4.type = data.kOutput
        var4.shape = [1]

        # Mocking necessary objects
        inputs = {'input1': 10, 'input2': 20}
        outputs = {'output1': None, 'output2': None}
        discrete_inputs = None
        discrete_outputs = None

        # Mocking the client and its methods
        client_mock = MagicMock()
        client_mock._var_meta = [var1, var2, var3, var4]
        client_mock.run_compute.return_value = {'output1': 30, 'output2': 40}

        # Creating instance of the class to be tested
        mock_channel = Mock()
        instance = RemoteExplicitComponent(channel=mock_channel)
        instance._client = client_mock
        # mock the component name
        instance.name = 'test'

        # Calling the function to be tested
        instance.compute(inputs, outputs, discrete_inputs, discrete_outputs)

        # Asserting that the method calls are made correctly
        client_mock.run_compute.assert_called_once_with({'input1': 10, 'input2': 20})
        self.assertEqual(outputs['output1'], 30)
        self.assertEqual(outputs['output2'], 40)

    def test_compute_partials_function(self):
        # Mocking necessary objects
        inputs = {'input1': 10, 'input2': 20}
        partials = {'output1': {'input1': None, 'input2': None},
                    'output2': {'input1': None, 'input2': None}}
        discrete_inputs = None
        discrete_outputs = None

        var1 = Mock()
        var1.name = "input1"
        var1.units = "m"
        var1.type = data.kInput
        var1.shape = [1]

        var2 = Mock()
        var2.name = "input2"
        var2.units = None
        var2.type = data.kInput
        var2.shape = [1]

        var3 = Mock()
        var3.name = "output1"
        var3.units = None
        var3.type = data.kOutput
        var3.shape = [1]

        var4 = Mock()
        var4.name = "output2"
        var4.units = None
        var4.type = data.kOutput
        var4.shape = [1]

        # Mocking the client and its methods
        client_mock = MagicMock()
        client_mock._var_meta = [var1, var2, var3, var4]
        client_mock.run_compute_partials.return_value = {'output1': {'input1': 1, 'input2': 2},
                                                         'output2': {'input1': 3, 'input2': 4}}

        # Creating instance of the class to be tested
        instance = RemoteExplicitComponent(channel=Mock())
        instance._client = client_mock
        # mock the component name
        instance.name = 'test'

        # Calling the function to be tested
        instance.compute_partials(inputs, partials, discrete_inputs, discrete_outputs)

        # Asserting that the method calls are made correctly
        client_mock.run_compute_partials.assert_called_once_with({'input1': 10, 'input2': 20})
        self.assertEqual(partials['output1']['input1'], 1)
        self.assertEqual(partials['output1']['input2'], 2)
        self.assertEqual(partials['output2']['input1'], 3)
        self.assertEqual(partials['output2']['input2'], 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)