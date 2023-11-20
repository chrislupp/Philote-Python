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
import philote_mdo.generated.data_pb2 as data


class RemoteImplicitComponent(om.ImplicitComponent):
    """
    An OpenMDAO component that acts as a client to an implicit analysis server.
    """

    def initialize(self):
        # host and port
        self.options.declare("channel")

    def setup(self):
        # create the client
        self._client = pm.ImplicitClient(channel=self.options["channel"])

        # set up the remote discipline and get the variable definitions
        self._client.run_setup()
        self._client.get_variable_definitions()

        # define inputs and outputs based on the discipline meta data
        for var in self._client._var_meta:
            if not var.units:
                units = None
            else:
                units = var.units

            if var.type == data.kInput:
                self.add_input(var.name, shape=tuple(var.shape), units=units)

            if var.type == data.kOutput:
                self.add_output(var.name, shape=tuple(var.shape), units=units)

        # set up the remote discipline and get the variable definitions
        self._client.get_partials_definitions()

        # declare partials based on the discipline meta data
        for partial in self._client._partials_meta:
            self.declare_partials(partial.name, partial.subname)

    def apply_nonlinear(self, inputs, residuals):
        # need to assign a local input dictionary, as the openmdao Vector class
        # returns the absolute variable name (including all parent system). The
        # remote client is unaware of any of the parent systems, so the relative
        # name of all variables is required.
        local_inputs = {}
        for var in self._client._var_meta:
            if var.type == data.kInput:
                local_inputs[var.name] = inputs[var.name]

        res = self._client.run_compute_residuals(local_inputs)

        # assign the outputs reference dictionary
        # note: merely assigning the outputs from the run_compute function will
        # overwrite the outputs reference and therefore not work
        for key, val in res.items():
            residuals[key] = val

    def solve_nonlinear(self, inputs, outputs):
        pass

    def linearize(self, inputs, outputs, jacobian):
        pass
