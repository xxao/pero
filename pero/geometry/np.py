#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy


def stack(arrays, axis=1):
    """Defines the missing numpy.stack function."""
    
    sl = (slice(None),) * axis + (numpy.newaxis,)
    expanded = [arr[sl] for arr in arrays]
    return numpy.concatenate(expanded, axis=axis)


def flip(array, axis=1):
    """Defines the missing numpy.flip function."""
    
    indexer = [slice(None)] * array.ndim
    indexer[axis] = slice(None, None, -1)
    return array[tuple(indexer)]


# set to numpy if not available
if not hasattr(numpy, 'stack'):
    numpy.stack = stack

if not hasattr(numpy, 'flip'):
    numpy.flip = flip
