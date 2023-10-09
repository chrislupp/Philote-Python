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

from philote_mdo.general import Discipline
import philote_mdo.generated.data_pb2 as data


class TestDiscipline(unittest.TestCase):

    def test_add_input(self):
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
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)