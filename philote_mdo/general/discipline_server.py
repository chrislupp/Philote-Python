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
import numpy as np

import philote_mdo.generated.data_pb2 as data
import philote_mdo.generated.disciplines_pb2_grpc as disc
from philote_mdo.utils import PairDict, get_flattened_view


class DisciplineServer(disc.DisciplineService):
    """
    Base class for all server classes.
    """

    def __init__(self, discipline=None):
        """
        """
        self.verbose = False

        # user/developer supplied discipline
        self._discipline = discipline

        # discipline stream options
        self._stream_opts = data.StreamOptions()

        # variable metadata
        self._var_meta = []

        # partials metadata
        self._partials_meta = []

    def attach_discipline(self, impl):
        """
        Adds a discipline implementation to the server.
        """
        self._discipline = impl

    def add_input(self, name, shape=(1,), units=''):
        """
        Define a continuous input.
        """
        meta = data.VariableMetaData()
        meta.type = data.VariableType.kInput
        meta.shape.extend(shape)
        meta.units = units
        self.var_meta += [meta]

    def add_output(self, name, shape=(1,), units=''):
        """
        Defines a continuous output.
        """
        meta = data.VariableMetaData()
        meta.type = data.VariableType.kOutput
        meta.shape.extend(shape)
        meta.units = units
        self._var_meta += [meta]

    def declare_partials(self, func, var):
        """
        Defines partials that will be determined using the analysis server.
        """
        self._partials_meta += [data.PartialsMetaData(name=func, subname=var)]

    def GetInfo(self, request, context):
        """
        RPC that sends the discipline information/properties to the client.
        """
        yield data.DisciplineProperties(continuous=self.discipline.continuous,
                                        differentiable=self.discipline.differentiable,
                                        provides_gradients=self.discipline.provides_gradients)

    def SetStreamOptions(self, request, context):
        """
        Receives options from the client on how data will be transmitted to and
        received from the client. The options are stores locally for use in the
        compute routines.
        """
        self.stream_opts = request

    def SetOptions(self, request, context):
        """
        RPC that sets the discipline options.
        """
        pass

    def Setup(self, request, context):
        """
        RPC that runs the setup function
        """
        self.discipline.setup()
        self.discipline.setup_partials()

    def GetVariableDefinitions(self, request, context):
        """
        Transmits setup information about the analysis discipline to the client.
        """

        # transmit the continuous input metadata
        for var in self._vars:
            yield data.VariableMetaData(type=data.VariableType.kInput,
                                                name=var['name'],
                                                shape=var['shape'],
                                                units=var['units'])
        # transmit the discrete input metadata
        for var in self.var_meta:
            yield var

    def GetPartialDefinitions(self, request, context):
        for jac in self._partials_meta:
            yield jac

    def preallocate_inputs(self, inputs, flat_inputs,
                           outputs={}, flat_outputs={}):
        """
        Preallocates the inputs before receiving data from the client.

        Note, for implicit disciplines, the function values are considered
        inputs to evaluate the residuals and the partials of the residuals.
        """
        # preallocate the input and discrete input arrays
        for var in self._vars:
            inputs[var['name']] = np.zeros(var['shape'])
            flat_inputs[var['name']] = get_flattened_view(inputs[var['name']])

        # preallocate the output and discrete output arrays
        for out in self._funcs:
            outputs[out['name']] = np.zeros(var['shape'])
            flat_outputs[out['name']] = get_flattened_view(
                outputs[out['name']])

    def preallocate_partials(self):
        """
        Preallocates the partials
        """
        jac = PairDict()

        for pair in self._partials:
            shape = tuple([d['shape']
                           for d in self._funcs if d['name'] == pair[0]])[0]
            shape += tuple([d['shape']
                            for d in self._vars if d['name'] == pair[1]])[0]
            jac[pair] = np.zeros(shape)

        return jac

    def process_inputs(self, request_iterator, flat_inputs,
                       flat_outputs=None):
        """
        Processes the message inputs from a gRPC stream.

        Note, for implicit disciplines, the function values are considered
        inputs to evaluate the residuals and the partials of the residuals.
        """
        # process inputs
        for message in request_iterator:
            # start and end indices for the array chunk
            b = message.start
            e = message.end

            # assign either continuous or discrete data
            if len(message.data) > 0:
                if message.type == data.VariableType.kInput:
                    flat_inputs[message.name][b:e] = message.data
                elif message.type == data.VariableType.kOutput:
                    flat_outputs[message.name][b:e] = message.data
            else:
                raise ValueError('Expected continuous or discrete variables, '
                                 'but arrays were empty for variable %s.' %
                                 (message.name))
