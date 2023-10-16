# Philote-Python

Python library for using and creating Philote analysis servers.


## Requirements

The installation process requires the following tools to be installed:

- grpc-tools
- protoletariat
- importlib.resources

Additionally, the following dependencies are required by Philote MDO and will be
installed automatically during the installation process (if not process):

- numpy
- grpc


## Installation

The Philote MDO Python bindings require a two step installation process. First,
make sure that `grpc-tools` and `protoletariat` are installed. If not, they can
be installed using pip. Note, that the first step of the installation process
will not complete without these tools. Unlike the other dependencies, pip will
not automatically install them during the package build.
The first step is to compile the protobuf/gRPC files into python files. This is
done by running (from the repository directory):

    python setup.py compile_proto

Once this step completes successfully, the package can be installed using pip:

    pip install .

or

    pip install -e .

for a development install.


## License

This package is licensed under the Apache 2 license:

   Copyright 2022-2023 Christopher A. Lupp

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

This work has been cleared for public release, distribution unlimited, case
number: AFRL-2023-XXXX. The views expressed are those of the author and do not
necessarily reflect the official policy or position of the Department of the
Air Force, the Department of Defense, or the U.S. government.