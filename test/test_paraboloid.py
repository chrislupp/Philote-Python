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

import philote_mdo.examples.paraboloid as par


class TestParaboloid(unittest.TestCase):
    """
    Unit tests for the paraboloid example discipline.
    """
    def test_setup(self):
        """
        Tests the setup function for the paraboloid.
        """
        parab = par.Parabaloid()
        parab.setup()

    def test_setup_partials(self):
        """
        Tests the setup_partials function for the paraboloid.
        """
        parab = par.Parabaloid()
        parab.setup_partials()

    def test_compute(self):
        """
        Tests the compute function for the paraboloid.
        """
        parab = par.Parabaloid()
        parab.compute()

    def test_compute_partials(self):
        """
        Tests the compute_partials function for the paraboloid.
        """
        parab = par.Parabaloid()
        parab.compute_partials()