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
import philote_mdo.generated.data_pb2 as data


class Discipline:
    """
    Base class for defining disciplines
    """

    def __init__(self):
        # discipline properties
        self._is_continuous = False
        self._is_differentiable = False
        self._provides_gradients = False

        # variable metadata
        self._var_meta = []

        # partials metadata
        self._partials_meta = []

        # flag that indicates the discipline is implicit
        self._is_implicit = False

    def add_input(self, name, shape=(1,), units=""):
        """
        Define a continuous input.
        """
        meta = data.VariableMetaData()
        meta.type = data.VariableType.kInput
        meta.name = name
        meta.shape.extend(shape)
        meta.units = units
        self._var_meta += [meta]

    def add_output(self, name, shape=(1,), units=""):
        """
        Defines a continuous output.
        """
        out_meta = data.VariableMetaData()
        out_meta.type = data.VariableType.kOutput
        out_meta.name = name
        out_meta.shape.extend(shape)
        out_meta.units = units
        self._var_meta += [out_meta]

        if self._is_implicit:
            res_meta = data.VariableMetaData()
            res_meta.type = data.VariableType.kOutput
            res_meta.name = name
            res_meta.shape.extend(shape)
            res_meta.units = units
            res_meta.type = data.VariableType.kResidual
            self._var_meta += [res_meta]

    def declare_partials(self, func, var):
        """
        Defines partials that will be determined using the analysis server.
        """
        self._partials_meta += [data.PartialsMetaData(name=func, subname=var)]

    def initialize(self, options):
        pass

    def setup(self):
        pass

    def setup_partials(self):
        pass

    def configure(self):
        pass

    def _clear_data(self):
        """
        Clears all meta data of the discipline.

        This function is invoked from the Setup function of the server.
        """
        self._var_meta = []
        self._partials_meta = []
