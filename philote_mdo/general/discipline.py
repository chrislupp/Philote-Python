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
import philote_mdo.generated.data_pb2 as data


class Discipline:
    """
    Base class for defining disciplines
    """

    def __init__(self):
        self.is_continuous = False
        self.is_differentiable = False
        self.provides_gradients = False

        # variable metadata
        self._var_meta = []

        # partials metadata
        self._partials_meta = []

    def add_input(self, name, shape=(1,), units=''):
        """
        Define a continuous input.
        """
        meta = data.VariableMetaData()
        meta.type = data.VariableType.kInput
        meta.name = name
        meta.shape.extend(shape)
        meta.units = units
        self._var_meta += [meta]

    def add_output(self, name, shape=(1,), units=''):
        """
        Defines a continuous output.
        """
        meta = data.VariableMetaData()
        meta.type = data.VariableType.kOutput
        meta.name = name
        meta.shape.extend(shape)
        meta.units = units
        self._var_meta += [meta]

    def declare_partials(self, func, var):
        """
        Defines partials that will be determined using the analysis server.
        """
        self._partials_meta += [data.PartialsMetaData(name=func, subname=var)]

    def initialize(self):
        pass

    def setup(self):
        pass

    def setup_partials(self):
        pass

    def configure(self):
        pass
    