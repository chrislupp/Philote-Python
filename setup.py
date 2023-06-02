from setuptools import setup, Command
import pkg_resources

__name__ = 'philote-mdo'
__version__ = '0.2.0'


class CompileProto(Command):
    description = "Compiles the proto files for this package."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import grpc_tools.protoc

        proto_include = pkg_resources.resource_filename('grpc_tools', '_proto')

        # compile the proto files for use in python
        grpc_tools.protoc.main([
            'grpc_tools.protoc',
            '-I{}'.format(proto_include),
            '-I{}'.format("./proto"),
            '--python_out=./philote_mdo/generated/',
            '--pyi_out=./philote_mdo/generated/',
            '--grpc_python_out=./philote_mdo/generated/',
            'array.proto',
            'explicit.proto',
            'implicit.proto',
            'metadata.proto',
            'options.proto'
        ])

        import protoletariat.__main__ as protol

        # call protoletariat to convert absolute imports to relative ones
        protol.main([
            '--in-place',
            '--dont-create-package',
            '--python-out=./philote_mdo/generated/',
            'protoc',
            '--proto-path=./proto',
            'array.proto',
            'explicit.proto',
            'implicit.proto',
            'metadata.proto',
            'options.proto'
        ])


setup(
    name=__name__,
    version=__version__,
    packages=['philote_mdo'],

    cmdclass={
        'compile_proto': CompileProto
    }
)
