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

\

class RemoteParabaloid(pmdo.general.ExplicitServer):

    def setup(self):
        self.define_input('x', shape=(1,), units='m')
        self.define_input('y', shape=(1,), units='m')

        self.define_output('f_xy', shape=(1,), units='m**2')

        self.define_partials('f_xy', '*')

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        x = inputs['x']
        y = inputs['y']

        outputs['f_xy'] = (x - 3.0)**2 + x * y + (y + 4.0)**2 - 3.0

    def compute_partials(self, inputs, partials, discrete_inputs=None):
        x = inputs['x']
        y = inputs['y']

        partials['f_xy', 'x'] = 2.0 * x - 6.0 + y
        partials['f_xy', 'y'] = 2.0 * y + 8.0 + x


pmdo.run_server(RemoteParabaloid())
