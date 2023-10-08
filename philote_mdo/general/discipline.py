# Copyright 2022-2023 Christopher A. Lupp
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


class Discipline:
    """
    Base class for defining disciplines
    """

    def __init__(self):
        self.is_continuous = False
        self.is_differentiable = False
        self.provides_gradients = False

    def initialize(self):
        pass

    def setup(self):
        pass

    def setup_partials(self):
        pass

    def configure(self):
        pass