#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math


def split_value(value, splits):
    """
    Splits given value into available units (e.g. time in seconds into days,
    hours, minutes etc.).
    
    Args:
        value: float or int
            Value to split.
        
        splits: {str: float}
            Split names and their unit values.
    
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
            Positive value for which to get the power.
        
        base: float or int
            Power base.
    
    Returns:
        int
            Largest integer power for which base**power <= value.
    """
    
    # get power
    power = math.floor(math.log10(value) / math.log10(base))
    
    # fix floating-point errors
    if base ** (power + 1) <= value:
        return power + 1
    
    if base ** power > value:
        return power - 1
    
    return power


def calc_digits(precision, scale=1, power=1):
    """
    Gets number of decimal places needed to show given precision of values
    scaled by scale**power. The calculation is done in logarithmic space to
    avoid overflow for large powers.
    
    Args:
        precision: float, int or None
            Required precision. If not set, 1 is used.
        
        scale: float or int
            Positive scaling factor.
        
        power: int
            Power of the scaling factor.
    
    Returns:
        int
            Number of decimal places.
    """
    
    # get precision
    precision = abs(precision or 1.)
    
    # get last significant digit
    digit = math.floor(math.log10(precision) - power * math.log10(scale))
    
    return max(0, -digit)


def strip_negative_zero(label, zero):
    """
    Removes the minus sign from given label if it represents zero after
    rounding (e.g. '-0.00 k').
    
    Args:
        label: str
            Formatted label.
        
        zero: str
            Label created by the same formatting applied to zero.
    
    Returns:
        str
            Label without the minus sign of zero.
    """
    
    if label.startswith('-') and label[1:] == zero:
        return label[1:]
    
    return label
