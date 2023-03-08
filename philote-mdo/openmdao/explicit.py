
import openmdao.api as om
import philote_mdo as pm


class RemoteExplicitComponent(om.ExplicitComponent, pm.ExplicitServer):
    """
    An OpenMDAO component that acts as a client to an explicit analysis server.
    """

    def setup(self):
        pass

    def setup_partials(self):
        pass

    def configure(self):
        pass

    def compute(self, inputs, discrete_inputs, outputs, discrete_outputs):
        pass

    def compute_partials(self, inputs, discrete_inputs, J):
        pass
