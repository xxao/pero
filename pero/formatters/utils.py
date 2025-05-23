#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.


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
