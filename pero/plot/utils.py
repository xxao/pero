#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
import numpy


def calc_histogram(x, bins, minimum=None, maximum=None, cumulative=False, base=None):
    """
    Calculates histogram from given data.
    
    Args:
        x: (float,)
            Data from which to calculate the histogram.
        
        bins: int or (float,)
            If integer value is provided, it specifies number of equal bins to
            create using specified range or given data range. If a collection
            of values is provided, it specifies the ranges of individual bins.
        
        minimum: float or None
            Specifies the minimum value to be used for bins calculation. If set
            to None, minimum of given data is used. This value is ignored if
            exact bins definitions is provided.
        
        maximum: float or None
            Specifies the maximum value to be used for bins calculation. If set
            to None, maximum of given data is used. This value is ignored if
            exact bins definitions is provided.
        
        cumulative: bool
            If se to True, returned histogram is cumulative, i.e. every value
            contains the sum of all previous values as well.
        
        base: int or None
            Specifies logarithm base to create logarithmic bins. This value is
            ignored if exact bins definitions is provided.
    
    Returns:
        hist: numpy.ndarray
            Histogram y data.
        
        bins: numpy.ndarray
            Bins definition.
    """
    
    # ensure numpy array
    if not isinstance(x, numpy.ndarray):
        x = numpy.array(x)
    
    # get range
    if minimum is None:
        minimum = x.min()
    
    if maximum is None:
        maximum = x.max()
    
    # make bins
    if isinstance(bins, (int, float)):
        
        # use log scale
        if base is not None:
            minimum = math.log(minimum, base)
            maximum = math.log(maximum, base)
            bins = numpy.logspace(minimum, maximum, num=bins, endpoint=True, base=base)
        
        # use lin scale
        else:
            bins = numpy.linspace(minimum, maximum, num=bins, endpoint=True)
    
    # calc histogram
    hist, bins = numpy.histogram(x, bins=bins)
    
    # make cumulative
    if cumulative:
        hist = numpy.cumsum(hist)
    
    return hist, bins
