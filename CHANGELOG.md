# Change Log

## Version 0.4.0

This version only expands the package documentation.


## Version 0.3.0

This release is one of the biggest changes to the code to date. It contains a
fundamental reorganization and adds a number of features. Notably, it adds
unit and integration testing of almost all the code.

- [feature] Reorganized codebase to reduce code duplication. The clients and
  servers now use base classes.
- [feature] Protobuf/gRPC files are now generated at build time and not commited
  to the repository. This requires grpc-tools and protoletariat to be installed.
  See the readme for details.
- [feature] Added a change log file to the repository.
- [feature] Updated API and logic to conform with newer Philote definition.
- [feature] Added unit testing suite.
- [feature] Added integration test suite (based on examples).
- [feature] Completed implicit discipline functionality and testing.
- [fix] Fixed unit tests for GetVariableDefinitions and GetPartialsDefinitions.
- [fix] Added edge case handling for partials of variables that are scalar.
- [fix] Corrected the preallocate_inputs function for the implicit case to
  resolve variable copy issues.
- [fix] Fixed typo in discrete input parsing.
- [fix] Moved to setup.py, as setuptools is still in beta for pyproject.toml.
- [doc] Added jupyter book for documentation.
- [doc] Added a quick start guide.


## Version 0.2.1

This is purely a bugfix release. Thanks to Alex Xu for finding these bugs and fixing them.

### Features

- None

### Bug Fixes

- Fixed bug that prevented proper chunking of array data
- Fixed flat view of arrays used during variable transfer


## Version 0.2.0

This version augments the Philote MDO version to 0.3.0.

### Features

- Moved to Philote version 0.3.0
- Renamed RPC function from Compute to Functions for Philote 0.3.0 compatibility
- Renamed RPC function from ComputePartials to Gradient for Philote 0.3.0 compatibility

### Bug Fixes

- Added flattened views for the ndarrays received. The previous version would 
  error for n-dimensional arrays, as the slices would not work unless the array
  was flattened.


## Version 0.1.0

Initial release of the Philote MDO Python bindings. Includes working remote 
explicit disciplines. Only the generic API currently works, so there is no
framework support for OpenMDAO or CSDL.

### Features

- Implemented a remote explicit discipline analysis server API.
- Implemented a corresponding client for explicit analyses.
- Added a simple parabaloid example to demonstrate the server/client in
action.

### Bug Fixes

- None, as this is the first release.

### Note

All versions starting with a 0 as the major version number should be
considered pre-release. While they may work in production environments,
it is expected that bugs may surface and that several features are still
missing. Because of this, the API may still change frequently before version
1.0.0 is released.
