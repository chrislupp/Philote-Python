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
import openmdao.api as om
import philote_mdo.general as pm


class OmGroupServer(pm.ExplicitServer):
    """PhiloteDiscipline that calls an OpenMDAO group.
    """

    def __init__(self):
        super().__init__()

        self._prob = om.Problem()
        self.model = self._prob.model

        self._inputs = {}
        self._discrete_inputs = {}

        self._outputs = {}
        self._discrete_outputs = {}

    def initialize(self):
        pass

    def setup(self):
        self._prob.setup()

    def compute(self, inputs, outputs, discrete_inputs=None,
                discrete_outputs=None):

        # assign continuous and discrete inputs of the nested group
        for comp_var, var in enumerate(self._inputs):
            self._prob[var] = inputs[comp_var]
        for comp_dvar, dvar in enumerate(self._discrete_inputs):
            self._prob[dvar] = discrete_inputs[comp_dvar]

        self._prob.run_model()

        # assign continuous and discrete outputs of the component
        for comp_out, out in enumerate(self._outputs):
            outputs[comp_out] = self._prob[out]
        for comp_dout, dout in enumerate(self._discrete_outputs):
            discrete_outputs[comp_dout] = self._prob[dout]

    def compute_partials(self, inputs, partials, discrete_inputs=None):
        # assign continuous and discrete inputs of the nested group
        for comp_var, var in enumerate(self._inputs):
            self._prob[var] = inputs[comp_var]
        for comp_dvar, dvar in enumerate(self._discrete_inputs):
            self._prob[dvar] = discrete_inputs[comp_dvar]

        # self._prob.compute_totals()

    def define_input(self, name, model_input):
        self._inputs[name] = model_input

    def define_discrete_input(self, name, model_input):
        self._discrete_inputs[name] = model_input

    def define_output(self, name, model_output):
        self._outputs[name] = model_output

    def define_discrete_output(self, name, model_output):
        self._discrete_outputs[name] = model_output
