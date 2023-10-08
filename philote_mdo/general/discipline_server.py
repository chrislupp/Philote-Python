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
from google.protobuf.empty_pb2 import Empty
import philote_mdo.generated.data_pb2 as data
from philote_mdo.utils import PairDict, get_flattened_view


class DisciplineServer:
    """
    Base class for all server classes.
    """

    def __init__(self):
        """
        """
        self.verbose = False

        # discipline stream options
        self.stream_opts = data.StreamOptions()

        # variable metadata
        self.var_meta = []

        # partials metadata
        self.partials_meta = []

        # discrete inputs (names, shapes, units)
        self._discrete_vars = []

        # discrete outputs (names, shapes, units)
        self._discrete_funcs = []

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
        self.var_meta += [meta]

    def declare_partials(self, func, var):
        """
        Defines partials that will be determined using the analysis server.
        """
        if isinstance(var, list):
            for val in var:
                if (func, val) not in self._partials:
                    self._partials += [(func, val['name'])]
        elif var == '*':
            for val in self._vars:
                if (func, val) not in self._partials:
                    self._partials += [(func, val['name'])]
        else:
            if (func, var) not in self._partials:
                self._partials += [(func, var)]

    def SetStreamOptions(self, request, context):
        """
        Receives options from the client on how data will be transmitted to and
        received from the client. The options are stores locally for use in the
        compute routines.
        """
        # set the maximum size of arrays that will be sent over the wire in one
        # chunk
        self.stream_opts = request

    def DefineVariables(self, request, context):
        """
        Transmits setup information about the analysis discipline to the client.
        """
        self.setup()

        # transmit the continuous input metadata
        for var in self._vars:
            yield data.VariableMetaData(type=data.VariableType.kInput,
                                                name=var['name'],
                                                shape=var['shape'],
                                                units=var['units'])
        # transmit the discrete input metadata
        for var in self._discrete_vars:
            yield data.VariableMetaData(type=data.VariableType.kDiscreteInput,
                                                name=var['name'],
                                                shape=var['shape'],
                                                units=var['units'])
        # transmit the continuous output metadata
        for func in self._funcs:
            yield data.VariableMetaData(type=data.VariableType.kOutput,
                                                name=func['name'],
                                                shape=func['shape'],
                                                units=func['units'])
        # transmit the discrete output metadata
        for func in self._discrete_funcs:
            yield data.VariableMetaData(type=data.VariableType.kDiscreteOutput,
                                                name=func['name'],
                                                shape=func['shape'],
                                                units=func['units'])

    def DefinePartials(self, request, context):
        self._partials = []

        self.setup_partials()

        # transmit the continuous input metadata
        for jac in self._partials:
            yield data.PartialsMetaData(name=jac[0], subname=jac[1])

    def preallocate_inputs(self, inputs, flat_inputs,
                           discrete_inputs={}, flat_disc_in={},
                           outputs={}, flat_outputs={},
                           discrete_outputs={}, flat_disc_out={}):
        """
        Preallocates the inputs before receiving data from the client.

        Note, for implicit disciplines, the function values are considered
        inputs to evaluate the residuals and the partials of the residuals.
        """
        # preallocate the input and discrete input arrays
        for var in self._vars:
            inputs[var['name']] = np.zeros(var['shape'])
            flat_inputs[var['name']] = get_flattened_view(inputs[var['name']])
        for dvar in self._discrete_vars:
            discrete_inputs[dvar['name']] = np.zeros(dvar['shape'])
            flat_disc_in[dvar['name']] = get_flattened_view(
                discrete_inputs[dvar['name']])

        # preallocate the output and discrete output arrays
        for out in self._funcs:
            outputs[out['name']] = np.zeros(var['shape'])
            flat_outputs[out['name']] = get_flattened_view(
                outputs[out['name']])
        for dout in self._discrete_funcs:
            discrete_outputs[dout['name']] = np.zeros(dout['shape'])
            flat_disc_out[dout['name']] = get_flattened_view(
                discrete_outputs[dout['name']])

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

    def process_inputs(self, request_iterator, flat_inputs, flat_disc_in,
                       flat_outputs=None, flat_disc_out=None):
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
            if len(message.continuous) > 0:
                if message.type == data.VariableType.kInput:
                    flat_inputs[message.name][b:e] = message.continuous
                elif message.type == data.VariableType.kOutput:
                    flat_outputs[message.name][b:e] = message.continuous
            elif len(message.discrete) > 0:
                if message.type == data.VariableType.kDiscreteInput:
                    flat_disc_in[message.name][b:e] = message.discrete
                elif message.type == data.VariableType.kDiscreteOutput:
                    flat_disc_out[message.name][b:e] = message.discrete
            else:
                raise ValueError('Expected continuous or discrete variables, '
                                 'but arrays were empty for variable %s.' %
                                 (message.name))
