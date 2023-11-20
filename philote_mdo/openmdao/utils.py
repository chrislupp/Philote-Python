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
import philote_mdo.generated.data_pb2 as data


def create_local_inputs(inputs, var_meta):
    """
    Creates a Philote-Python local inputs dictionary from OpenMDAO inputs.

    We need to assign a local input dictionary, as the openmdao Vector class
    returns the absolute variable name (including all parent system). The
    remote client is unaware of any of the parent systems, so the relative
    name of all variables is required.
    """

    local_inputs = {}
    for var in var_meta:
        if var.type == data.kInput:
            local_inputs[var.name] = inputs[var.name]

    return local_inputs


def assign_global_outputs(out, outputs):
    """
    Assigns a OpenMDAO outputs from a Philote-Python output/residual dictionary.

    note: merely assigning the outputs from the compute (etc.) function will
    overwrite the OpenMDAO outputs variable reference and therefore not work.
    """
    for key, val in out.items():
        outputs[key] = val
