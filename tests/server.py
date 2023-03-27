
from philote_mdo import run_server
from philote_mdo.general import ExplicitServer
import philote_mdo.general as pmdo
import grpc
from concurrent import futures
import philote_mdo.generated.explicit_pb2_grpc as explicit_pb2_grpc


class Analysis(pmdo.ExplicitServer):

    def setup(self):
        self._vars = [{'name': 'test1', 'shape': (1,), 'units': 'm'},
                      {'name': 'test12', 'shape': (1,), 'units': 'm'}]
        self._discrete_vars = [{'name': 'test2', 'shape': (2,), 'units': 'm2'}]
        self._funcs = [{'name': 'test3', 'shape': (3,), 'units': 'm3'}]
        self._discrete_funcs = [
            {'name': 'test4', 'shape': (4,), 'units': 'm4'}]


run_server(Analysis())
