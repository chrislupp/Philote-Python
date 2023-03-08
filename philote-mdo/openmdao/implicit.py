
import openmdao.api as om
import philote_mdo as pm


class RemoteImplicitComponent(om.ImplicitComponent, pm.ImplicitServer):
    """
    An OpenMDAO component that acts as a client to an implicit analysis server.
    """

    def setup(self):
        pass

    def setup_partials(self):
        pass

    def configure(self):
        pass
