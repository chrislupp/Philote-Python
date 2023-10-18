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

from test_discipline import TestDiscipline

from test_discipline_server import TestDisciplineServer
from test_explicit_server import TestExplicitServer

from test_discipline_client import TestDisciplineClient
from test_explicit_client import TestExplicitClient

from test_paraboloid import TestParaboloid, TestParaboloidIntegration


if __name__ == "__main__":
    unittest.main(verbosity=2)