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
import philote_mdo.general as pmdo


class ImplicitDiscipline(pmdo.Discipline):
    """
    """

    def __init__(self):
        pass

    def compute_residuals(self, inputs, outputs, residuals):
        raise NotImplementedError('compute_residuals not implemented')

    def solve_residuals(self, inputs, outputs):
        raise NotImplementedError('solve_residuals not implemented')

    def residual_partials(self, inputs, outputs, partials):
        raise NotImplementedError('residual_partials not implemented')

    def apply_linear(self, inputs, outputs, mode):
        """
        """
        raise NotImplementedError('apply_linear not implemented')