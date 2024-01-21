# Philote-Python
#
# Copyright 2022-2024 Christopher A. Lupp
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
from .utils import client_setup, create_local_inputs, assign_global_outputs


class RemoteImplicitComponent(om.ImplicitComponent):
    """
    An OpenMDAO component that acts as a client to an implicit analysis server.
    """

    def initialize(self):
        # gRPC channel
        self.options.declare("channel")

    def setup(self):
        self._client = pm.ImplicitClient(channel=self.options["channel"])
        client_setup(self)

    def apply_nonlinear(self, inputs, outputs, residuals):
        local_inputs = create_local_inputs(
            inputs, self._client._var_meta, type=data.kInput
        )
        local_outputs = create_local_inputs(
            outputs, self._client._var_meta, type=data.kOutput
        )
        res = self._client.run_compute_residuals(local_inputs, local_outputs)
        assign_global_outputs(res, residuals)

    def solve_nonlinear(self, inputs, outputs):
        local_inputs = create_local_inputs(inputs, self._client._var_meta)
        out = self._client.run_solve_residuals(local_inputs)
        assign_global_outputs(out, outputs)

    def linearize(self, inputs, outputs, partials):
        local_inputs = create_local_inputs(
            inputs, self._client._var_meta, type=data.kInput
        )
        local_outputs = create_local_inputs(
            outputs, self._client._var_meta, type=data.kOutput
        )
        jac = self._client.run_residual_gradients(local_inputs, local_outputs)
        assign_global_outputs(jac, partials)
