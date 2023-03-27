
import philote_mdo as pmdo


class RemoteParabaloid(pmdo.general.ExplicitServer):

    def setup(self):
        self._vars = [{'name': 'x', 'shape': (1,), 'units': 'm'},
                      {'name': 'y', 'shape': (1,), 'units': 'm'}]

        self._funcs = [{'name': 'f_xy', 'shape': (1,), 'units': 'm**2'}]

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        x = inputs['x']
        y = inputs['y']

        outputs['f_xy'] = (x - 3.0)**2 + x * y + (y + 4.0)**2 - 3.0

    def compute_partials(self, inputs, partials, discrete_inputs=None):
        x = inputs['x']
        y = inputs['y']

        partials['f_xy', 'x'] = 2.0*x - 6.0 + y
        partials['f_xy', 'y'] = 2.0*y + 8.0 + x


pmdo.run_server(RemoteParabaloid())
