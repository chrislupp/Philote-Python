# Philote-Python
#
# Copyright 2022-2024 Christopher A. Lupp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# This work has been cleared for public release, distribution unlimited, case
# number: AFRL-2023-5713.
#
# The views expressed are those of the authors and do not reflect the
# official guidance or position of the United States Government, the
# Department of Defense or of the United States Air Force.
#
# Statement from DoD: The Appearance of external hyperlinks does not
# constitute endorsement by the United States Department of Defense (DoD) of
# the linked websites, of the information, products, or services contained
# therein. The DoD does not exercise any editorial, security, or other
# control over the information you may find at these locations.
import os
from setuptools import setup, Command, find_packages
import importlib.resources as resources

__name__ = "philote-mdo"
__version__ = "0.3.0"


class CompileProto(Command):
    description = "Compiles the proto files for this package."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import grpc_tools.protoc

        proto_include = os.path.join(resources.files("grpc_tools"), "_proto")

        # proto files
        proto_files = ["data.proto", "disciplines.proto"]

        # compile the proto files for use in python
        grpc_tools.protoc.main(
            [
                "grpc_tools.protoc",
                "-I{}".format(proto_include),
                "-I{}".format("./proto"),
                "--python_out=./philote_mdo/generated/",
                "--pyi_out=./philote_mdo/generated/",
                "--grpc_python_out=./philote_mdo/generated/",
            ]
            + proto_files
        )

        import protoletariat.__main__ as protol

        # call protoletariat to convert absolute imports to relative ones
        protol.main(
            [
                "--in-place",
                "--dont-create-package",
                "--python-out=./philote_mdo/generated/",
                "protoc",
                "--proto-path=./proto",
            ]
            + proto_files
        )


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
    install_requires=["numpy", "grpcio", "grpcio-tools", "protoletariat"],
    packages=find_packages(exclude=["*test"]),
    cmdclass={"compile_proto": CompileProto},
)
