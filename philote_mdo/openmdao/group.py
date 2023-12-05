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
import openmdao.api as om
import philote_mdo.general as pm


class OpenMdaoSubProblem(pm.ExplicitDiscipline):
    """
    PhiloteDiscipline that calls an OpenMDAO group.
    """

    def __init__(self, group=None):
        super().__init__()

        self._prob = None
        self._model = None

        self._input_map = {}
        self._output_map = {}

        self.add_group(group)

    def add_group(self, group):
        """
        Adds an OpenMDAO group to the discipline.

        Warning: This will delete any previous problem settings and attached
        models.
        """
        self._prob = om.Problem(model=group)
        self._model = self._prob.model

    def add_mapped_input(self, local_var, subprob_var):
        """
        Adds an input that is mapped from the discipline to the sub-problem.
        """
        self._input_map[local_var] = subprob_var

    def add_mapped_output(self, local_var, subprob_var):
        """
        Adds an output that is mapped from the discipline to the sub-problem.
        """
        self._output_map[local_var] = subprob_var

    def clear_mapped_variables(self):
        """
        Clears the variable map and sets it to an empty dictionary.
        """
        self._input_map = {}
        self._output_map = {}

    def initialize(self):
        pass

    def setup(self):
        self._prob.setup()

        for local, sub in self._input_map.items():
            self.add_input(local)

        for local, sub in self._output_map.items():
            self.add_output(local)

    def compute(self, inputs, outputs):
        # assign continuous and discrete inputs of the nested group
        for local, sub in self._input_map.items():
            self._prob[sub] = inputs[local]

        self._prob.run_model()

        # assign continuous and discrete outputs of the component
        for local, sub in self._output_map.items():
            outputs[local] = self._prob[sub]

    # def compute_partials(self, inputs, partials, discrete_inputs=None):
    #     # assign continuous and discrete inputs of the nested group
    #     for comp_var, var in enumerate(self._inputs):
    #         self._prob[var] = inputs[comp_var]
    #     for comp_dvar, dvar in enumerate(self._discrete_inputs):
    #         self._prob[dvar] = discrete_inputs[comp_dvar]

    #     # self._prob.compute_totals()
