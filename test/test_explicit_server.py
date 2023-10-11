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

from google.protobuf.empty_pb2 import Empty

from philote_mdo.general import ExplicitDiscipline, ExplicitServer
import philote_mdo.generated.data_pb2 as data


class TestDisciplineServer(unittest.TestCase):
    """
    Unit tests for the discipline server.
    """
    def test_get_info(self):
        """
        Tests the ComputeFunction RPC.
        """
        server = ExplicitServer()
        server._discipline = ExplicitDiscipline()

        # mock arguments
        context = Mock()
        request = Empty()

        response_generator = server.ComputeFunction(request, context)
