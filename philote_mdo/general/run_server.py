import grpc
from concurrent import futures
import philote_mdo.generated.explicit_pb2_grpc as explicit_pb2_grpc


def run_server(service, port='50051', max_workers=10):
    """
    Helper function for running an analysis server.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

    # add an explicit or implicit server
    if isinstance(service, explicit_pb2_grpc.ExplicitComponentServicer):
        explicit_pb2_grpc.add_ExplicitComponentServicer_to_server(
            service, server)
    else:
        raise ValueError('Unexpected object type provided for variable '
                         '"service".')

    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Started server. Press 'q' and hit enter to stop the server.")

    try:
        while True:
            user_input = input()
            if user_input == 'q':
                break
    except KeyboardInterrupt:
        pass

    print("Stopping the server...")
    server.stop(0)
