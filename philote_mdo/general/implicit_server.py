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


class ImplicitServer():
    """
    Base class for creating an implicit discipline server.
    """

    def __init__(self):
        """
        """
        pass

    def Residuals(self, request_iterator, context):
        """
        """
        pass

    def Solve(self, request_iterator, context):
        """
        """
        pass

    def ResidualGradients(self, request_iterator, context):
        """
        """
        pass

    # user defined functions (will be overloaded)

    def initialize(self):
        """
        """
        pass

    def setup(self):
        """
        """
        pass

    def setup_partials(self):
        """
        """
        pass

    def apply_nonlinear(self, inputs, outputs, residuals):
        """
        """
        pass

    def solve_nonlinear(self, inputs, outputs):
        """
        """
        pass

    def linearize(self, inputs, outputs, partials):
        """
        """
        pass

    def apply_linear(self, inputs, outputs,
                     d_inputs, d_outputs, d_residuals, mode):
        """
        """
        pass
