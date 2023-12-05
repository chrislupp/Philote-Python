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
import unittest
import numpy as np
import openmdao.api as om
from openmdao.test_suite.components.sellar import SellarDis1, SellarDis2
from philote_mdo.openmdao import OpenMdaoSubProblem


class SellarMDA(om.Group):
    """
    This is the Sellar MDO problem as implemented in the OpenMDAO codebase,
    licensed under the Apache 2 open source license:

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this software except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    It was included here so that the solver debug print statments could
    be turned off.
    """

    def setup(self):
        cycle = self.add_subsystem('cycle', om.Group(), promotes=['*'])
        cycle.add_subsystem('d1', SellarDis1(),
                            promotes_inputs=['x', 'z', 'y2'],
                            promotes_outputs=['y1'])
        cycle.add_subsystem('d2', SellarDis2(),
                            promotes_inputs=['z', 'y1'],
                            promotes_outputs=['y2'])

        cycle.set_input_defaults('x', 1.0)
        cycle.set_input_defaults('z', np.array([5.0, 2.0]))

        # Nonlinear Block Gauss Seidel is a gradient free solver
        cycle.nonlinear_solver = om.NonlinearBlockGS(iprint=0)

        self.add_subsystem('obj_cmp', om.ExecComp('obj = x**2 + z[1] + y1 + exp(-y2)',
                                                  z=np.array([0.0, 0.0]), x=0.0),
                           promotes=['x', 'z', 'y1', 'y2', 'obj'])

        self.add_subsystem('con_cmp1', om.ExecComp('con1 = 3.16 - y1'),
                           promotes=['con1', 'y1'])
        self.add_subsystem('con_cmp2', om.ExecComp('con2 = y2 - 24.0'),
                           promotes=['con2', 'y2'])


class TestOpenMdaoGroup(unittest.TestCase):
    """
    Unit tests for the OpenMDAO group discipline.
    """

    def test_compute(self):
        """
        Unit test for the OpenMDAO group discipline compute function.
        """
        disc = OpenMdaoSubProblem()

        # add the Sellar group and turn off the solver debug print
        disc.add_group(SellarMDA())

        disc.add_mapped_input("x", "x")
        disc.add_mapped_input("z", "z")

        disc.add_mapped_output("y1", "y1")
        disc.add_mapped_output("y2", "y2")
        disc.add_mapped_output("obj", "obj")
        disc.add_mapped_output("con1", "con1")
        disc.add_mapped_output("con2", "con2")

        disc.setup()

        inputs = {
            "x": np.array([2.0]),
            "z": np.array([-1., -1.])
        }
        outputs = {
            "y1": np.array([0.0]),
            "y2": np.array([0.0]),
            "obj": np.array([0.0]),
            "con1": np.array([0.0]),
            "con2": np.array([0.0])
        }

        disc.compute(inputs, outputs)

        self.assertAlmostEqual(outputs["y1"][0], 2.10951651, 5)
        self.assertAlmostEqual(outputs["y2"][0], -0.54758253, 5)
        self.assertAlmostEqual(outputs["obj"][0], 6.8385845, 5)
        self.assertAlmostEqual(outputs["con1"][0], 1.05048349, 5)
        self.assertAlmostEqual(outputs["con2"][0], -24.54758253, 5)

    def test_compute_partials(self):
        """
        Unit test for the OpenMDAO group discipline compute_partials function.
        """
        disc = OpenMdaoSubProblem()

        # add the Sellar group and turn off the solver debug print
        disc.add_group(SellarMDA())

        disc.add_mapped_input("x", "x")
        disc.add_mapped_input("z", "z")

        disc.add_mapped_output("y1", "y1")
        disc.add_mapped_output("y2", "y2")
        disc.add_mapped_output("obj", "obj")
        disc.add_mapped_output("con1", "con1")
        disc.add_mapped_output("con2", "con2")

        disc.declare_subproblem_partial("y1", "x")
        disc.declare_subproblem_partial("y1", "z")
        disc.declare_subproblem_partial("y2", "x")
        disc.declare_subproblem_partial("y2", "z")
        disc.declare_subproblem_partial("obj", "x")
        disc.declare_subproblem_partial("obj", "z")
        disc.declare_subproblem_partial("con1", "x")
        disc.declare_subproblem_partial("con1", "z")
        disc.declare_subproblem_partial("con2", "x")
        disc.declare_subproblem_partial("con2", "z")

        disc.setup()

        inputs = {
            "x": np.array([2.0]),
            "z": np.array([-1., -1.])
        }
        partials = {
            ("y1", "x"): np.array([0.0]),
            ("y1", "z"): np.zeros(2),
            ("y2", "x"): np.array([0.0]),
            ("y2", "z"): np.zeros(2),
            ("obj", "x"): np.array([0.0]),
            ("obj", "z"): np.zeros(2),
            ("con1", "x"): np.array([0.0]),
            ("con1", "z"): np.zeros(2),
            ("con2", "x"): np.array([0.0]),
            ("con2", "z"): np.zeros(2)
        }

        disc.compute_partials(inputs, partials)

        self.assertAlmostEqual(partials[("y1", "x")][0, 0], 0.99982674, 5)
        self.assertAlmostEqual(partials[("y1", "z")][0, 0], -2.00017226, 5)
        self.assertAlmostEqual(partials[("y1", "z")][0, 1], 0.99982674, 5)

        self.assertAlmostEqual(partials[("y2", "x")][0, 0], 0.34413432, 5)
        self.assertAlmostEqual(partials[("y2", "z")][0, 0], 0.31149316, 5)
        self.assertAlmostEqual(partials[("y2", "z")][0, 1], 1.34407468, 5)

        self.assertAlmostEqual(partials[("obj", "x")][0, 0], 4.40479511, 5)
        self.assertAlmostEqual(partials[("obj", "z")][0, 0], -2.53876511, 5)
        self.assertAlmostEqual(partials[("obj", "z")][0, 1], -0.32416976, 5)

        self.assertAlmostEqual(partials[("con1", "x")][0, 0], -0.99982674, 5)
        self.assertAlmostEqual(partials[("con1", "z")][0, 0], 2.00017226, 5)
        self.assertAlmostEqual(partials[("con1", "z")][0, 1], -0.99982674, 5)

        self.assertAlmostEqual(partials[("con2", "x")][0, 0], 0.34413432, 5)
        self.assertAlmostEqual(partials[("con2", "z")][0, 0], 0.31149316, 5)
        self.assertAlmostEqual(partials[("con2", "z")][0, 1], 1.34407468, 5)

if __name__ == "__main__":
    unittest.main(verbosity=2)