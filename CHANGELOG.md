# Change Log

## Version 0.4.0
- [feature] Updated API and logic to conform with newer Philote definition.
- [feature] Added unit testing suite.
- [feature] Completed implicit discipline functionality and testing.
- [fix] Fixed unit tests for GetVariableDefinitions and GetPartialsDefinitions.
- [fix] Added edge case handling for partials of variables that are scalar.
- [fix] Corrected the preallocate_inputs function for the implicit case to
  resolve variable copy issues.

## Version 0.3.0

This release is one of the biggest changes to the code to date. It contains a
fundamental reorganization and adds a number of features.

- [feature] Reorganized codebase to reduce code duplication. The clients and
  servers now use base classes.
- [feature] Protobuf/gRPC files are now generated at build time and not commited
  to the repository. This requires grpc-tools and protoletariat to be installed.
- [feature] Added a change log file to the repository.
- [fix] Fixed typo in discrete input parsing.
- [fix] Moved to setup.py, as setuptools is still in beta for pyproject.toml.

## Version 0.2.1

## Version 0.2.0

## Version 0.1.0