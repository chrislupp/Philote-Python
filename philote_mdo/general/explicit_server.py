import grpc
import explicit_pb2
import explicit_pb2_grpc


class ExplicitServer(explicit_pb2_grpc.ExplicitComponentServicer):
    """
    Base class for remote explicit components.
    """

    def __init__(self):
        self.num_double = 100
        self.num_int = 100

    def SetStreamOptions(self, request, context):
        """
        Receives options from the client on how data will be transmitted to and
        received from the client. The options are stores locally for use in the
        compute routines.
        """
        # set the maximum size of arrays that will be sent over the wire in one
        # chunk
        self.num_double = request.num_double
        self.num_int = request.num_int

    def Setup(self, request, context):
        """
        Transmits setup information about the analysis discipline to the client.
        """
        pass

    def Compute(self, request_iterator, context):
        """
        Computes the function evaluation and sends the result to the client.
        """
        pass

    def ComputePartials(self, request_iterator, context):
        """
        Computes the gradient evaluation and sends the result to the client.
        """
        pass

    def setup(self):
        pass

    def compute(self):
        pass

    def compute_partials(self):
        pass
