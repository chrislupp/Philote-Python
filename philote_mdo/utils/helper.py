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
#
#
# This work has been cleared for public release, distribution unlimited, case
# number: AFRL-2023-XXXX. The views expressed are those of the author and do not
# necessarily reflect the official policy or position of the Department of the
# Air Force, the Department of Defense, or the U.S. government.
import numpy as np

def get_chunk_indices(num_values, chunk_size):
    beg_i = np.arange(0, num_values, chunk_size)

    if beg_i.size == 1:
        end_i = [num_values]
    else:
        end_i = np.append(beg_i[1:], [num_values])

    return zip(beg_i, end_i)

def get_flattened_view(arr):
    """
    Returns a flattened view of the input array. Used instead of reshape, ravel, flatten, etc. to guarante a copy is
    not made. If the input array does not support copy-free modification, AttributeError will be thrown
    :param arr: Array to get a flattened view
    :return: A view of the input array, guaranteed to not be a copy
    """
    flat_view = arr.view()
    flat_view.shape = (-1)
    return flat_view