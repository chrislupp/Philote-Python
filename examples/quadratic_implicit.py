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

import philote_mdo as pmdo


class RemoteQuadratic(pmdo.general.ImplicitServer):

    def setup(self):
        self.define_input('a', shape=(1,))
        self.define_input('b', shape=(1,))
        self.define_input('c', shape=(1,))

        self.define_output('x', shape=(1,))

    def setup_partials(self):
        self.define_partials('x', '*')

    def compute_residuals(self, inputs, outputs, residuals,
                          discrete_inputs=None, discrete_outputs=None):
        a = inputs['a']
        b = inputs['b']
        c = inputs['c']
        x = outputs['x']

        residuals['x'] = a * x ** 2.0 + b * x + c

    # def compute_partials(self, inputs, partials, discrete_inputs=None):
    #     x = inputs['x']
    #     y = inputs['y']

    #     partials['f_xy', 'x'] = 2.0 * x - 6.0 + y
    #     partials['f_xy', 'y'] = 2.0 * y + 8.0 + x


pmdo.run_server(RemoteQuadratic())
