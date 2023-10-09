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

from google.protobuf.empty_pb2 import Empty

from philote_mdo.general import Discipline, DisciplineServer
import philote_mdo.generated.data_pb2 as data


class TestDisciplineServer(unittest.TestCase):
    """
    Unit tests for the discipline server.
    """
    def test_get_info(self):
        """
        Tests the GetInfo RPC.
        """
        server = DisciplineServer()
        server._discipline = Discipline()
        server._discipline._is_continuous = True
        server._discipline._is_differentiable = True
        server._discipline._provides_gradients = True

        # mock arguments
        context = Mock()
        request = Empty()

        response_generator = server.GetInfo(request, context)

        # Generate responses and collect them into a list
        responses = list(response_generator)

        # check that there is only one response
        self.assertEqual(len(responses), 1)

        # check the values of the response
        response = responses[0]
        self.assertTrue(response.continuous)
        self.assertTrue(response.differentiable)
        self.assertTrue(response.provides_gradients)

    def test_set_stream_options(self):
        """
        Tests the SetStreamOptions RPC.
        """
        server = DisciplineServer()

        # mock arguments
        context = Mock()
        request = data.StreamOptions(num_double=2)

        server.SetStreamOptions(request, context)

        # check that the streaming options were set properly
        self.assertEqual(server._stream_opts.num_double, 2)

    # def test_set_options(self):
    #     pass

    def test_setup(self):
        """
        Tests the Setup RPC.
        """
        context = Mock()
        request = Empty()

        server = DisciplineServer()

        # mock the 'setup' and 'setup_partials' methods of 'self.discipline'
        server._discipline = Mock()
        server._discipline.setup.return_value = None
        server._discipline.setup_partials.return_value = None

        server.Setup(request, context)

        # assert that the 'setup' and 'setup_partials' methods were called
        server._discipline.setup.assert_called_once()
        server._discipline.setup_partials.assert_called_once()

    def test_get_variable_definitions(self):
        """
        Tests the GetVariableDefinitions RPC.
        """
        server = DisciplineServer()
        server._discipline = Discipline()

        # add an input and an output
        server._discipline.add_input('x', shape=(2, 2), units="m")
        server._discipline.add_output('f', shape=(1,), units="m**2")

        # mock arguments
        context = Mock()
        request = Empty()

        response_generator = server.GetVariableDefinitions(request, context)

        # Generate responses and collect them into a list
        responses = list(response_generator)

        # check that there are two responses (one input, one output)
        self.assertEqual(len(responses), 2)

        # check the response data
        input = responses[0]
        output = responses[1]

        self.assertEqual(input.name, "x")
        self.assertEqual(input.shape, [2, 2])
        self.assertEqual(input.units, "m")
        self.assertEqual(input.type, data.kInput)

        self.assertEqual(output.name, "f")
        self.assertEqual(output.shape, [1,])
        self.assertEqual(output.units, "m**2")
        self.assertEqual(output.type, data.kOutput)

    # def test_preallocate_inputs(self):
    #     pass

    # def test_preallocate_partials(self):
    #     pass

    # def test_process_inputs(self):
    #     pass