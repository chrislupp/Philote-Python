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


class PairDict(dict):
    """
    Jacobian dictionary for storing values with respect to two keys.
    """

    def __setitem__(self, keys, value):
        key1, key2 = keys
        super().__setitem__((key1, key2), value)

    def __getitem__(self, keys):
        key1, key2 = keys
        return super().__getitem__((key1, key2))
