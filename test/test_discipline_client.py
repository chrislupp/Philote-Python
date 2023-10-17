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
# number: AFRL-2023-XXXX. The views expressed are those of the author and do not
# necessarily reflect the official policy or position of the Department of the
# Air Force, the Department of Defense, or the U.S. government.
import unittest
from unittest.mock import Mock, patch

import numpy as np

from google.protobuf.empty_pb2 import Empty

from philote_mdo.general import Discipline, DisciplineClient
import philote_mdo.generated.data_pb2 as data


class TestDisciplineClient(unittest.TestCase):
    """
    Unit tests for the discipline client.
    """
    @patch('philote_mdo.generated.disciplines_pb2_grpc.DisciplineServiceStub')
    def test_get_discipline_info(self, mock_discipline_stub):
        """
        Tests the get_discipline_info function of the Discipline Client.
        """
        mock_channel = Mock()
        mock_stub = mock_discipline_stub.return_value
        mock_stub.GetInfo.return_value = [data.DisciplineProperties(
            continuous=True, differentiable=True, provides_gradients=True
        )]

        client = DisciplineClient(mock_channel)
        client.get_discipline_info()

        # check the values of the response
        self.assertTrue(client._is_continuous)
        self.assertTrue(client._is_differentiable)
        self.assertTrue(client._provides_gradients)

    @patch('philote_mdo.generated.disciplines_pb2_grpc.DisciplineServiceStub')
    def test_send_stream_options(self, mock_discipline_stub):
        """
        Tests the set_stream_options function of the Discipline Client.
        """
        mock_channel = Mock()
        mock_stub = mock_discipline_stub.return_value


        client = DisciplineClient(mock_channel)
        expected_num_double = 10
        client._stream_options = expected_options = data.StreamOptions(
            num_double=expected_num_double,
        )
        client.send_stream_options()

        # check that the streaming options were set properly
        expected_options = data.StreamOptions(
            num_double=expected_num_double,
        )
        self.assertTrue(mock_stub.SetStreamOptions.called)
        mock_stub.SetStreamOptions.assert_called_with(expected_options)

    # def test_set_options(self):
    #     pass

    @patch('philote_mdo.generated.disciplines_pb2_grpc.DisciplineServiceStub')
    def test_run_setup(self, mock_discipline_stub):
        """
        Tests the run_setup function of the Discipline Client.
        """
        mock_channel = Mock()
        mock_stub = mock_discipline_stub.return_value
        client = DisciplineClient(mock_channel)
        client.run_setup()

        # assert that the 'setup' and 'setup_partials' methods were called
        self.assertTrue(mock_stub.Setup.called)
        mock_stub.Setup.assert_called_with(Empty())

    @patch('philote_mdo.generated.disciplines_pb2_grpc.DisciplineServiceStub')
    def test_get_variable_definitions(self, mock_discipline_stub):
        """
        Tests the get_variable_definitions function of the Discipline Client.
        """
        mock_channel = Mock()
        mock_stub = mock_discipline_stub.return_value
        client = DisciplineClient(mock_channel)

        input_definition = data.VariableMetaData(
            name="x", shape=[2, 2], units="m", type=data.VariableType.kInput
        )
        output_definition = data.VariableMetaData(
            name="f", shape=[1], units="m**2", type=data.VariableType.kOutput
        )

        # configure the stub to return the mock input and output definitions
        mock_stub.DefineVariables.return_value = [input_definition, output_definition]

        # call the get_variables_definitions method
        client.get_variable_definitions()

        # assert that the gRPC call was made
        self.assertTrue(mock_stub.DefineVariables.called)

        # assert that the _var_meta attribute is updated with the expected input
        # and output definitions
        self.assertEqual(len(client._var_meta), 2)

        # check the response data for input definition
        input = client._var_meta[0]
        self.assertEqual(input.name, "x")
        self.assertEqual(input.shape, [2, 2])
        self.assertEqual(input.units, "m")
        self.assertEqual(input.type, data.kInput)

        # check the response data for output definition
        output = client._var_meta[1]
        self.assertEqual(output.name, "f")
        self.assertEqual(output.shape, [1])
        self.assertEqual(output.units, "m**2")
        self.assertEqual(output.type, data.kOutput)

    @patch('philote_mdo.generated.disciplines_pb2_grpc.DisciplineServiceStub')
    def test_get_partial_definitions(self, mock_discipline_stub):
        """
        Tests the get_partial_definitions function of the Discipline Client.
        """
        mock_channel = Mock()
        mock_stub = mock_discipline_stub.return_value
        client = DisciplineClient(mock_channel)

        partials_metadata = [
            data.PartialsMetaData(name="input1", subname="output1"),
            data.PartialsMetaData(name="input2", subname="output2"),
        ]

        mock_stub.DefinePartials.return_value = partials_metadata

        client.get_partials_definitions()

        # check that the client function was called
        self.assertTrue(mock_stub.DefinePartials.called)

        # check that the number of entries is correct
        self.assertEqual(len(client._partials_meta), 2)

        # check the values
        self.assertEqual(client._partials_meta[0].name, "input1")
        self.assertEqual(client._partials_meta[0].subname, "output1")
        self.assertEqual(client._partials_meta[1].name, "input2")
        self.assertEqual(client._partials_meta[1].subname, "output2")


    def test_assemble_input_messages(self):
        mock_channel = Mock()
        client = DisciplineClient(mock_channel)
        client._stream_options.num_double = 2

        input_data = {
            "x": np.array([1.0, 2.0, 3.0, 4.0]).reshape(2, 2),
        }
        output_data = {
            "f": np.array([5.0, 6.0, 7.0]).reshape(1, 3),
        }

        # expected messages based on input and output data
        expected_messages = [
            data.Array(
                name="x",
                start=0,
                end=1,
                type=data.VariableType.kInput,
                data=[1.0, 2.0]
            ),
            data.Array(
                name="x",
                start=2,
                end=3,
                type=data.VariableType.kInput,
                data=[3.0, 4.0]
            ),
            data.Array(
                name="f",
                start=0,
                end=1,
                type=data.VariableType.kOutput,
                data=[5.0, 6.0]
            ),
            data.Array(
                name="f",
                start=2,
                end=2,
                type=data.VariableType.kOutput,
                data=[7.0]
            )
        ]

        messages = client._assemble_input_messages(input_data, output_data)

        # check that the resulting messages match the expected messages
        self.assertEqual(len(messages), len(expected_messages))
        for msg, expected_msg in zip(messages, expected_messages):
            self.assertEqual(msg, expected_msg)