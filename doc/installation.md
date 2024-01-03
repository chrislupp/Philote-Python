# Installation

Philote-Python is a pure Python library. However, the installation process requires a few extra steps,
as the gRPC/protobuf definitions must first be compiled into 


## Requirements

The installation process requires the following tools to be installed:

- grpcio-tools
- protoletariat
- importlib.resources

Additionally, the following dependencies are required by Philote MDO and will be
installed automatically during the installation process:

- numpy
- grpcio


## Compiling Definitions and Installation

The Philote MDO Python bindings require a two step installation process. First,
make sure that `grpcio-tools` and `protoletariat` are installed. If not, they
can be installed using pip. Note, that the first step of the installation
process will not complete without these tools. Unlike the other dependencies,
pip will not automatically install them during the package build. The first step
is to compile the protobuf/gRPC files into python files. This is done by running
(from the repository directory):

    python setup.py compile_proto

Once this step completes successfully, the package can be installed using pip:

    pip install .

or

    pip install -e .

for a development install.