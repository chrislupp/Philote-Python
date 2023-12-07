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
from concurrent import futures
import unittest
import grpc
import numpy as np
import openmdao.api as om
import philote_mdo.general as pmdo
import philote_mdo.openmdao as pmom
from philote_mdo.examples import Paraboloid, QuadradicImplicit, SellarMDA
from philote_mdo.openmdao import OpenMdaoSubProblem

class OpenMdaoIntegrationTests(unittest.TestCase):
    """
    Integration tests for the paraboloid discipline.
    """

    def test_paraboloid_compute(self):
        """
        Tests the OpenMDAO compute function using the Paraboloid.
        """
        # server code
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        discipline = pmdo.ExplicitServer(discipline=Paraboloid())
        discipline.attach_to_server(server)

        server.add_insecure_port("[::]:50051")
        server.start()

        # client code
        prob = om.Problem()
        model = prob.model

        model.add_subsystem(
            "Paraboloid",
            pmom.RemoteExplicitComponent(
                channel=grpc.insecure_channel("localhost:50051")
            ),
            promotes=["*"],
        )

        prob.setup()

        prob["x"] = 1.0
        prob["y"] = 2.0
        prob.run_model()

        self.assertEqual(prob["f_xy"][0], 39.0)

        # stop the server
        server.stop(0)

    def test_paraboloid_compute_partials(self):
        """
        Tests the OpenMDAO compute_partials function using the Paraboloid.
        """
        # server code
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        discipline = pmdo.ExplicitServer(discipline=Paraboloid())
        discipline.attach_to_server(server)

        server.add_insecure_port("[::]:50051")
        server.start()

        # client code
        prob = om.Problem()
        model = prob.model

        model.add_subsystem(
            "Paraboloid",
            pmom.RemoteExplicitComponent(
                channel=grpc.insecure_channel("localhost:50051")
            ),
            promotes=["*"],
        )

        prob.setup()

        prob["x"] = 1.0
        prob["y"] = 2.0
        prob.run_model()

        data = prob.check_partials(out_stream=None)

        # check the data
        self.assertEqual(data["Paraboloid"][("f_xy", "x")]["J_fwd"], -2.0)
        self.assertEqual(data["Paraboloid"][("f_xy", "y")]["J_fwd"], 13.0)

        # stop the server
        server.stop(0)

    def test_paraboloid_opt(self):
        """
        Integration test that checks the ability to run a gradient-based
        optimization with an OpenMDAO explicit component.
        """
        # server code
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        discipline = pmdo.ExplicitServer(discipline=Paraboloid())
        discipline.attach_to_server(server)

        server.add_insecure_port("[::]:50051")
        server.start()

        # client code
        client = pmdo.ExplicitClient(channel=grpc.insecure_channel("localhost:50051"))

        # transfer the stream options to the server
        client.send_stream_options()

        # run setup
        client.run_setup()
        client.get_variable_definitions()
        client.get_partials_definitions()

        # client code
        prob = om.Problem()
        prob.driver = om.ScipyOptimizeDriver()
        prob.driver.options['optimizer'] = 'SLSQP'
        prob.driver.options['disp'] = False
        model = prob.model

        model.add_subsystem(
            "Paraboloid",
            pmom.RemoteExplicitComponent(
                channel=grpc.insecure_channel("localhost:50051")
            ),
            promotes=["*"],
        )
        model.add_design_var("x")
        model.add_design_var("y")

        model.add_objective("f_xy")

        prob.setup()
        prob.set_val('x', 50.0)
        prob.set_val('y', 50.0)

        prob.run_driver()

        # check the optimization results
        self.assertAlmostEqual(prob["x"][0], 6.6666666, 6)
        self.assertAlmostEqual(prob["y"][0], -7.33333333, 6)
        self.assertAlmostEqual(prob["f_xy"][0], -27.3333333333, 6)

        # stop the server
        server.stop(0)

    def test_implicit_quadratic(self):
        """
        Tests the OpenMDAO compute function using the implicit quadratic component.
        """
        # server code
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        discipline = pmdo.ImplicitServer(discipline=QuadradicImplicit())
        discipline.attach_to_server(server)

        server.add_insecure_port("[::]:50051")
        server.start()

        # client code
        prob = om.Problem()
        model = prob.model

        model.add_subsystem(
            "ImplicitQuadratic",
            pmom.RemoteImplicitComponent(
                channel=grpc.insecure_channel("localhost:50051")
            ),
            promotes=["*"],
        )

        prob.setup()

        prob["a"] = 1.0
        prob["b"] = 2.0
        prob["c"] = -2.0
        prob.run_model()

        self.assertAlmostEqual(prob["x"][0], 0.73205081, places=8)

        # stop the server
        server.stop(0)

    def test_sellar_compute(self):
        """
        Integration test for the OpenMDAO sub-problem compute function.
        """
        # server code
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        disc = OpenMdaoSubProblem()

        # add the Sellar group and turn off the solver debug print
        disc.add_group(SellarMDA())

        disc.add_mapped_input("x", "x")
        disc.add_mapped_input("z", "z", shape=(2,))

        disc.add_mapped_output("y1", "y1")
        disc.add_mapped_output("y2", "y2")
        disc.add_mapped_output("obj", "obj")
        disc.add_mapped_output("con1", "con1")
        disc.add_mapped_output("con2", "con2")

        discipline = pmdo.ExplicitServer(discipline=disc)
        discipline.attach_to_server(server)

        server.add_insecure_port("[::]:50051")
        server.start()

        # client code
        prob = om.Problem()
        model = prob.model

        model.add_subsystem(
            "Sellar",
            pmom.RemoteExplicitComponent(
                channel=grpc.insecure_channel("localhost:50051")
            ),
            promotes=["*"],
        )

        prob.setup()

        prob["x"] = np.array([2.0])
        prob["z"] = np.array([-1., -1.])

        prob.run_model()

        self.assertAlmostEqual(prob["y1"][0], 2.10951651, 5)
        self.assertAlmostEqual(prob["y2"][0], -0.54758253, 5)
        self.assertAlmostEqual(prob["obj"][0], 6.8385845, 5)
        self.assertAlmostEqual(prob["con1"][0], 1.05048349, 5)
        self.assertAlmostEqual(prob["con2"][0], -24.54758253, 5)

        # stop the server
        server.stop(0)

    def test_sellar_compute_partials(self):
        """
        Integration test for the OpenMDAO sub-problem compute_partials function.
        """
        # server code
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        disc = OpenMdaoSubProblem()

        # add the Sellar group and turn off the solver debug print
        disc.add_group(SellarMDA())

        disc.add_mapped_input("x", "x")
        disc.add_mapped_input("z", "z", shape=(2,))

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

        discipline = pmdo.ExplicitServer(discipline=disc)
        discipline.attach_to_server(server)

        server.add_insecure_port("[::]:50051")
        server.start()

        # client code
        prob = om.Problem()
        model = prob.model

        model.add_subsystem(
            "Sellar",
            pmom.RemoteExplicitComponent(
                channel=grpc.insecure_channel("localhost:50051")
            ),
            promotes=["*"],
        )

        prob.setup()

        prob["x"] = np.array([2.0])
        prob["z"] = np.array([-1., -1.])

        prob.run_model()

        data = prob.check_partials(out_stream=None)

        j = data["Sellar"]

        self.assertAlmostEqual(j[("y1", "x")]["J_fwd"][0, 0], 0.9353804990265645, 3)
        self.assertAlmostEqual(j[("y1", "z")]["J_fwd"][0, 0], -2.0585057709335794, 3)
        self.assertAlmostEqual(j[("y1", "z")]["J_fwd"][0, 1], 0.7481210608200559, 3)

        self.assertAlmostEqual(j[("y2", "x")]["J_fwd"][0, 0], 0.32195231245910344, 3)
        self.assertAlmostEqual(j[("y2", "z")]["J_fwd"][0, 0], 0.2914151146554633, 3)
        self.assertAlmostEqual(j[("y2", "z")]["J_fwd"][0, 1], 1.2574391012932133, 3)

        self.assertAlmostEqual(j[("obj", "x")]["J_fwd"][0, 0], 4.378703060615849, 3)
        self.assertAlmostEqual(j[("obj", "z")]["J_fwd"][0, 0], -2.5623823180578524, 3)
        self.assertAlmostEqual(j[("obj", "z")]["J_fwd"][0, 1], -0.42607664106566956, 3)

        self.assertAlmostEqual(j[("con1", "x")]["J_fwd"][0, 0], -0.9353804990265645, 3)
        self.assertAlmostEqual(j[("con1", "z")]["J_fwd"][0, 0], 2.0585057709335794, 3)
        self.assertAlmostEqual(j[("con1", "z")]["J_fwd"][0, 1], -0.7481210608200559, 3)

        self.assertAlmostEqual(j[("con2", "x")]["J_fwd"][0, 0], 0.32195231245910344, 3)
        self.assertAlmostEqual(j[("con2", "z")]["J_fwd"][0, 0], 0.2914151146554633, 3)
        self.assertAlmostEqual(j[("con2", "z")]["J_fwd"][0, 1], 1.2574391012932133, 3)

        # stop the server
        server.stop(0)




if __name__ == "__main__":
    unittest.main(verbosity=2)
