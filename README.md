![Philote](doc/graphics/philote-python.svg)

[![Unit and Regression Tests](https://github.com/chrislupp/Philote-Python/actions/workflows/tests.yaml/badge.svg)](https://github.com/chrislupp/Philote-Python/actions/workflows/tests.yaml)
# Philote-Python

Python library for using and creating Philote analysis servers.

Documentation can be found at:

https://chrislupp.github.io/Philote-Python


## Requirements

The installation process requires the following tools to be installed:

- grpcio-tools
- protoletariat
- importlib.resources

Additionally, the following dependencies are required by Philote MDO and will be
installed automatically during the installation process (if not process):

- numpy
- grpcio


## Installation

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
number: AFRL-2023-5713.

The views expressed are those of the authors and do not reflect the official
guidance or position of the United States Government, the Department of Defense
or of the United States Air Force.

Statement from DoD: The Appearance of external hyperlinks does not constitute
endorsement by the United States Department of Defense (DoD) of the linked
websites, of the information, products, or services contained therein. The DoD
does not exercise any editorial, security, or other control over the information
you may find at these locations.
