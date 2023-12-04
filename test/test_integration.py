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
from openmdao.utils.assert_utils import assert_check_partials
import philote_mdo.general as pmdo
import philote_mdo.openmdao as pmom
from philote_mdo.examples import Paraboloid, QuadradicImplicit


class IntegrationTests(unittest.TestCase):
    """
    Integration tests for the paraboloid discipline.
    """

    def test_paraboloid_compute(self):
        """
        Integration test for the Paraboloid compute function.
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

        # define some inputs
        inputs = {"x": np.array([1.0]), "y": np.array([2.0])}

        # run a function evaluation
        outputs = client.run_compute(inputs)

        self.assertEqual(outputs["f_xy"][0], 39.0)

        # stop the server
        server.stop(0)

    def test_paraboloid_compute_partials(self):
        """
        Integration test for the Paraboloid compute function.
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

        # define some inputs
        inputs = {"x": np.array([1.0]), "y": np.array([2.0])}

        # run a function evaluation
        jac = client.run_compute_partials(inputs)

        self.assertEqual(jac["f_xy", "x"][0], -2.0)
        self.assertEqual(jac["f_xy", "y"][0], 13.0)

        # stop the server
        server.stop(0)

    def test_openmdao_paraboloid_compute(self):
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
        client = pmdo.ExplicitClient(channel=grpc.insecure_channel("localhost:50051"))

        # transfer the stream options to the server
        client.send_stream_options()

        # run setup
        client.run_setup()
        client.get_variable_definitions()
        client.get_partials_definitions()

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

    def test_openmdao_paraboloid_compute_partials(self):
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

    def test_openmdao_paraboloid_opt(self):
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

    def test_quadratic_compute_residuals(self):
        """
        Integration test for the QuadraticImplicit compute function.
        """
        # server code
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        discipline = pmdo.ImplicitServer(discipline=QuadradicImplicit())
        discipline.attach_to_server(server)

        server.add_insecure_port("[::]:50051")
        server.start()

        # client code
        client = pmdo.ImplicitClient(channel=grpc.insecure_channel("localhost:50051"))

        # transfer the stream options to the server
        client.send_stream_options()

        # run setup
        client.run_setup()
        client.get_variable_definitions()
        client.get_partials_definitions()

        # define some inputs
        inputs = {"a": np.array([1.0]), "b": np.array([2.0]), "c": np.array([-2.0])}
        outputs = {"x": np.array([4.0])}

        # run a function evaluation
        residuals = client.run_compute_residuals(inputs, outputs)

        self.assertEqual(residuals["x"][0], 22.0)

        # stop the server
        server.stop(0)

    def test_quadratic_solve_residuals(self):
        """
        Integration test for the QuadraticImplicit compute function.
        """
        # server code
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        discipline = pmdo.ImplicitServer(discipline=QuadradicImplicit())
        discipline.attach_to_server(server)

        server.add_insecure_port("[::]:50051")
        server.start()

        # client code
        client = pmdo.ImplicitClient(channel=grpc.insecure_channel("localhost:50051"))

        # transfer the stream options to the server
        client.send_stream_options()

        # run setup
        client.run_setup()
        client.get_variable_definitions()
        client.get_partials_definitions()

        # define some inputs
        inputs = {"a": np.array([1.0]), "b": np.array([2.0]), "c": np.array([-2.0])}

        # run a function evaluation
        outputs = client.run_solve_residuals(inputs)

        self.assertAlmostEqual(outputs["x"][0], 0.73205081, places=8)

        # stop the server
        server.stop(0)

    def test_quadratic_residual_gradients(self):
        """
        Integration test for the QuadraticImplicit residual gradients function.
        """
        # server code
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        discipline = pmdo.ImplicitServer(discipline=QuadradicImplicit())
        discipline.attach_to_server(server)

        server.add_insecure_port("[::]:50051")
        server.start()

        # client code
        client = pmdo.ImplicitClient(channel=grpc.insecure_channel("localhost:50051"))

        # transfer the stream options to the server
        client.send_stream_options()

        # run setup
        client.run_setup()
        client.get_variable_definitions()
        client.get_partials_definitions()

        # define some inputs
        inputs = {"a": np.array([1.0]), "b": np.array([2.0]), "c": np.array([-2.0])}
        outputs = {"x": np.array([4.0])}

        # run a function evaluation
        jac = client.run_residual_gradients(inputs, outputs)

        self.assertEqual(jac[("x", "a")][0], 16.0)
        self.assertEqual(jac[("x", "b")][0], 4.0)
        self.assertEqual(jac[("x", "c")][0], 1.0)
        self.assertEqual(jac[("x", "x")][0], 10.0)

        # stop the server
        server.stop(0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
