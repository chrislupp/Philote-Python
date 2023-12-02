# Philote-Python
#
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

# general unit tests
from test_discipline import TestDiscipline

from test_discipline_server import TestDisciplineServer
from test_explicit_server import TestExplicitServer
from test_implicit_server import TestImplicitServer

from test_discipline_client import TestDisciplineClient
from test_explicit_client import TestExplicitClient
from test_implicit_client import TestImplicitClient

# openmdao unit tests
from test_openmdao_utils import TestOpenMdaoUtils

# example unit tests
from test_paraboloid import TestParaboloid
from test_quadratic import TestQuadradicImplicit

# integrations tests
from test_integration import IntegrationTests


if __name__ == "__main__":
    unittest.main(verbosity=2)
