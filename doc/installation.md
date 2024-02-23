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

Older versions of this library featured a two-step build process. This has since
been simplified. To install the package run pip:

    pip install -e .

If you want to install the package without editable mode, you will need to run the
two-step process previously described. First, run:

    python utils/compile_proto.py

followed by:

    pip install .