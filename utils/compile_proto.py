import os
import importlib.resources as resources
import grpc_tools.protoc
import protoletariat.__main__ as protol


def main():

    print("Compiling proto files.")

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


if __name__ == "__main__":
    main()