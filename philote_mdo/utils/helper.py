import numpy as np

def get_chunk_indicies(num_values, chunk_size):
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