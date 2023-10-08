import pathlib
from setuptools import setup, Command
import importlib.resources as resources

__name__ = 'philote-mdo'
__version__ = '0.3.0'


class CompileProto(Command):
    description = "Compiles the proto files for this package."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import grpc_tools.protoc
        import grpc_tools._proto
        resource_path = resources.path(grpc_tools._proto, '')
        proto_include = str(pathlib.Path(resource_path))

        # proto files
        proto_files = ['data.proto',
                       'disciplines.proto'
                       ]

        # compile the proto files for use in python
        grpc_tools.protoc.main([
            'grpc_tools.protoc',
            '-I{}'.format(proto_include),
            '-I{}'.format("./proto"),
            '--python_out=./philote_mdo/generated/',
            '--pyi_out=./philote_mdo/generated/',
            '--grpc_python_out=./philote_mdo/generated/'
        ] + proto_files)

        import protoletariat.__main__ as protol

        # call protoletariat to convert absolute imports to relative ones
        protol.main([
            '--in-place',
            '--dont-create-package',
            '--python-out=./philote_mdo/generated/',
            'protoc',
            '--proto-path=./proto'] + proto_files)


setup(
    name=__name__,
    version=__version__,
    author="Christopher A. Lupp",
    author_email="christopherlupp@gmail.com",
    license="Apache License 2.0",
    keywords=["mdo", "optimization", "rpc"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "grpc",
    ],
    packages=['philote_mdo'],

    cmdclass={
        'compile_proto': CompileProto
    }
)
