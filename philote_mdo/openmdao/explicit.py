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
import grpc
import openmdao.api as om
import philote_mdo as pm


class RemoteExplicitComponent(om.ExplicitComponent):
    """
    An OpenMDAO component that acts as a client to an explicit analysis server.
    """

    def initialize(self):
        # host and port
        self.options.declare('channel')

    def setup(self):
        # create the client
        self.client = pm.ExplicitClient(channel=self.channel)

        # set up the remote server
        self.client.remote_setup()

        # define inputs
        for input in self.client._vars:
            self.add_input(input['name'], shape=input['shape'],
                           units=input['units'])

        # define discrete inputs
        for dinput in self.client._vars:
            self.add_discrete_input(dinput['name'], shape=dinput['shape'],
                                    units=dinput['units'])

        # define outputs
        for out in self.client._funcs:
            self.add_output(input['name'], shape=input['shape'],
                            units=input['units'])

        # define discrete outputs
        for dout in self.client._funcs:
            self.add_discrete_output(input['name'], shape=input['shape'],
                                     units=input['units'])

    def setup_partials(self):
        # setup the partials on the server
        self.client.setup_remote_partials()

    def compute(self, inputs, discrete_inputs, outputs, discrete_outputs):
        # call the remote compute method
        out, discrete_out = self.client.remote_compute(inputs, discrete_inputs,
                                                       discrete_outputs)

        # assign the values to the openmdao dict type
        for key, val in out.items():
            outputs[key] = val

        # assign the values to the openmdao dict type
        for key, val in discrete_out.items():
            discrete_outputs[key] = val

    def compute_partials(self, inputs, discrete_inputs, partials):
        # call the remote analysis to get the partials
        jac = self.client.remote_compute_partials(inputs, discrete_inputs)

        # assign the values to the openmdao partials type
        for key, val in jac.items():
            partials[key] = val
