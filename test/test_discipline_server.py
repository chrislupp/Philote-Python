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


class TestDisciplineServer(unittest.TestCase):
    def test_get_info(self):
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
        self.assertEqual(response.continuous, True)
        self.assertEqual(response.differentiable, True)
        self.assertEqual(response.provides_gradients, True)



    def test_set_stream_options(self):
        pass

    def test_set_options(self):
        pass

    def test_setup(self):
        pass

    def test_get_variable_definitions(self):
        pass

    def test_preallocate_inputs(self):
        pass

    def test_preallocate_partials(self):
        pass

    def test_process_inputs(self):
        pass