#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math


def split_value(value, splits):
    """
    Splits given time in seconds into available units.
    
    Args:
        value: float or int
            Value to split.
        
        splits: {str: float}
            Split names and thresholds values.
    
    Returns:
        {str: float}
            Value for each available split.
    """
    
    # get available units
    units = sorted(splits.items(), key=lambda d: d[1], reverse=True)
    
    # init parts
    parts = {u[0]: 0.0 for u in units}
    
    # split time
    rest = value
    for unit, f in units:
        count, rest = divmod(rest, f)
        parts[unit] = count
    
    return parts


def calc_power(value, base=10):
    """
    Gets integer power of base for given value.
    
    Args:
        value: float or int
            Value to split.
        
        base: float or int
            Power base.
    
    Returns:
        {str: float}
            Value for each available split.
    """
    
    # get power
    power = math.floor(math.log10(value) / math.log10(base))
    
    # fix floating-point errors
    if base ** (power + 1) <= value:
        return power + 1
    
    if base ** power > value:
        return power - 1
    
    return power
