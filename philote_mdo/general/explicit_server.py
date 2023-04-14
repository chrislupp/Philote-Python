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
import philote_mdo.generated.metadata_pb2 as metadata_pb2
import philote_mdo.generated.explicit_pb2_grpc as explicit_pb2_grpc
import philote_mdo.generated.array_pb2 as array_pb2
from philote_mdo.utils import PairDict


class ExplicitServer(explicit_pb2_grpc.ExplicitDisciplineServicer):
    """
    Base class for remote explicit components.
    """

    def __init__(self):
        self.verbose = False
        self.num_double = 100
        self.num_int = 100

        # continuous inputs (names, shapes, units)
        self._vars = []

        # discrete inputs (names, shapes, units)
        self._discrete_vars = []

        # continous outputs (names, shapes, units)
        self._funcs = []

        # discrete outputs (names, shapes, units)
        self._discrete_funcs = []

        # list of all defined partials
        self._partials = []

    def define_input(self, name, shape=(1,), units=''):
        """
        Define a continuous input.
        """
        if {'name': name, 'shape': shape, 'units': units} not in self._vars:
            self._vars += [{'name': name, 'shape': shape, 'units': units}]

    def define_discrete_input(self, name, shape=(1,), units=''):
        """
        Define a discrete input.
        """
        if {'name': name, 'shape': shape, 'units': units} not in self._discrete_vars:
            self._discrete_vars += [{'name': name,
                                     'shape': shape,
                                     'units': units}]

    def define_output(self, name, shape=(1,), units=''):
        """
        Defines a continuous output.
        """
        if {'name': name, 'shape': shape, 'units': units} not in self._funcs:
            self._funcs += [{'name': name, 'shape': shape, 'units': units}]

    def define_discrete_output(self, name, shape=(1,), units=''):
        """
        Defines a discrete output.
        """
        if {'name': name, 'shape': shape, 'units': units} not in self._discrete_funcs:
            self._discrete_funcs += [{'name': name,
                                     'shape': shape,
                                      'units': units}]

    def define_partials(self, func, var):
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
        self.num_double = request.num_double
        self.num_int = request.num_int

        return Empty()

    def DefineVariables(self, request, context):
        """
        Transmits setup information about the analysis discipline to the client.
        """
        self.setup()

        # transmit the continuous input metadata
        for var in self._vars:
            yield metadata_pb2.VariableMetaData(discrete=False,
                                                input=True,
                                                name=var['name'],
                                                shape=var['shape'],
                                                units=var['units'])
        # transmit the discrete input metadata
        for var in self._discrete_vars:
            yield metadata_pb2.VariableMetaData(discrete=True,
                                                input=True,
                                                name=var['name'],
                                                shape=var['shape'],
                                                units=var['units'])
        # transmit the continuous output metadata
        for func in self._funcs:
            yield metadata_pb2.VariableMetaData(discrete=False,
                                                input=False,
                                                name=func['name'],
                                                shape=func['shape'],
                                                units=func['units'])
        # transmit the discrete output metadata
        for func in self._discrete_funcs:
            yield metadata_pb2.VariableMetaData(discrete=True,
                                                input=False,
                                                name=func['name'],
                                                shape=func['shape'],
                                                units=func['units'])

    def DefinePartials(self, request, context):
        self._partials = []

        self.setup_partials()

        # transmit the continuous input metadata
        for jac in self._partials:
            yield metadata_pb2.PartialsMetaData(name=jac[0], subname=jac[1])

    def Functions(self, request_iterator, context):
        """
        Computes the function evaluation and sends the result to the client.
        """
        # inputs and outputs
        inputs = {}
        discrete_inputs = {}
        outputs = {}
        discrete_outputs = {}

        # preallocate the input and discrete input arrays
        for var in self._vars:
            inputs[var['name']] = np.zeros(var['shape'])
        for dvar in self._discrete_vars:
            discrete_inputs[dvar['name']] = np.zeros(dvar['shape'])

        # process inputs
        for message in request_iterator:
            # start and end indices for the array chunk
            b = message.start
            e = message.end

            # assign either continuous or discrete data
            if len(message.continuous) > 0:
                inputs[message.name][b:e] = message.continuous
            elif len(message.discrete) > 0:
                discrete_inputs[message.name][b:e] = message.discrete
            else:
                raise ValueError('Expected continuous or discrete variables, '
                                 'but arrays were empty.')

        # call the user-defined compute function
        self.compute(inputs, outputs, discrete_inputs, discrete_outputs)

        # iterate through all continuous outputs in the dictionary
        for output_name, value in outputs.items():
            # get the beginning and end indices of the chunked arrays
            beg_i = np.arange(0, value.size, self.num_double)
            if beg_i.size == 1:
                end_i = [value.size]
            else:
                end_i = beg_i[1:]

            # iterate through all chunks needed for the current input
            for b, e in zip(beg_i, end_i):
                # create the chunked data
                yield array_pb2.Array(name=output_name,
                                      start=b,
                                      end=e,
                                      continuous=value.ravel()[b:e])

        # iterate through all discrete outputs in the dictionary
        for doutput_name, value in discrete_outputs.items():
            # get the beginning and end indices of the chunked arrays
            beg_i = np.arange(0, value.size, self.num_double)
            if beg_i.size == 1:
                end_i = [value.size]
            else:
                end_i = beg_i[1:]

            # iterate through all chunks needed for the current input
            for b, e in zip(beg_i, end_i):
                # create the chunked data
                yield array_pb2.Array(name=doutput_name,
                                      start=b,
                                      end=e,
                                      discrete=value.ravel()[b:e])

    def Gradient(self, request_iterator, context):
        """
        Computes the gradient evaluation and sends the result to the client.
        """
        # inputs and outputs
        inputs = {}
        discrete_inputs = {}

        # preallocate the input and discrete input arrays
        for var in self._vars:
            inputs[var['name']] = np.zeros(var['shape'])
        for dvar in self._discrete_vars:
            discrete_inputs[dvar['name']] = np.zeros(dvar['shape'])

        # process inputs
        for message in request_iterator:
            # start and end indices for the array chunk
            b = message.start
            e = message.end

            # assign either continuous or discrete data
            if len(message.continuous) > 0:
                inputs[message.name][b:e] = message.continuous
            elif len(message.discrete) > 0:
                discrete_inputs[message.name][b:e] = message.discrete
            else:
                raise ValueError('Expected continuous or discrete variables, '
                                 'but arrays were empty.')

        # preallocate the partials
        jac = PairDict()

        for pair in self._partials:
            shape = tuple([d['shape']
                           for d in self._funcs if d['name'] == pair[0]])[0]
            shape += tuple([d['shape']
                            for d in self._vars if d['name'] == pair[1]])[0]
            jac[pair] = np.zeros(shape)

        # call the user-defined compute_partials function
        self.compute_partials(inputs, jac, discrete_inputs)

        # iterate through all continuous outputs in the dictionary
        for jac, value in jac.items():
            # get the beginning and end indices of the chunked arrays
            beg_i = np.arange(0, value.size, self.num_double)
            if beg_i.size == 1:
                end_i = [value.size]
            else:
                end_i = beg_i[1:]

            # iterate through all chunks needed for the current input
            for b, e in zip(beg_i, end_i):
                # create and send the chunked data
                yield array_pb2.Array(name=jac[0],
                                      subname=jac[1],
                                      start=b,
                                      end=e,
                                      continuous=value.ravel()[b:e])

    def initialize(self):
        pass

    def setup(self):
        pass

    def compute(self, inputs, outputs, discrete_inputs=None,
                discrete_outputs=None):
        pass

    def compute_partials(self, inputs, partials, discrete_inputs=None):
        pass
