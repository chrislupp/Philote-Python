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

from philote_mdo.general import Discipline
import philote_mdo.generated.data_pb2 as data


class TestDiscipline(unittest.TestCase):
    """
    Unit tests for the discipline base class.
    """

    def test_add_input(self):
        """
        Tests the add input member function.
        """
        disc = Discipline()

        disc.add_input("test", shape=(2, 2), units="m**2")

        # check if the variable meta data contains one entry
        self.assertEqual(len(disc._var_meta), 1)

        # check the meta data values
        self.assertEqual(disc._var_meta[0].name, "test")
        self.assertEqual(disc._var_meta[0].shape, [2, 2])
        self.assertEqual(disc._var_meta[0].units, "m**2")
        self.assertEqual(disc._var_meta[0].type, data.kInput)

    def test_add_output(self):
        """
        Tests the add output member function.
        """
        disc = Discipline()

        disc.add_output("test", shape=(2, 2), units="m**2")

        # check if the variable meta data contains one entry
        self.assertEqual(len(disc._var_meta), 1)

        # check the meta data values
        self.assertEqual(disc._var_meta[0].name, "test")
        self.assertEqual(disc._var_meta[0].shape, [2, 2])
        self.assertEqual(disc._var_meta[0].units, "m**2")
        self.assertEqual(disc._var_meta[0].type, data.kOutput)

    def test_declare_partials(self):
        """
        Tests the declare partials member function.
        """
        disc = Discipline()

        disc.declare_partials("f", "x")

        # check if the variable meta data contains one entry
        self.assertEqual(len(disc._partials_meta), 1)

        # check the meta data values
        self.assertEqual(disc._partials_meta[0].name, "f")
        self.assertEqual(disc._partials_meta[0].subname, "x")


if __name__ == "__main__":
    unittest.main(verbosity=2)
