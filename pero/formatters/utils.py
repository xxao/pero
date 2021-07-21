#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import TIME_FACTORS


def split_time(seconds):
    """
    Splits given time in seconds into available units.
    
    Args:
        seconds: float or int
            Time in seconds.
    
    Returns:
        dict
            Value for each available time unit.
    """
    
    # get available units
    units = sorted(TIME_FACTORS.items(), key=lambda d: d[1], reverse=True)
    
    # init parts
    parts = {u[0]: 0.0 for u in units}
    
    # split time
    value = seconds
    for unit, f in units:
        count, rest = divmod(value, f)
        parts[unit] = count
        value = rest
    
    return parts


def round_time(seconds, units, rounding):
    """
    Rounds given time into specific units.
    
    Args:
        seconds: float or int
            Time in seconds.
        
        units: pero.TIME
            Specifies the rounding units as eny item from the pero.TIME enum.
        
        rounding: pero.ROUNDING
            Specifies the rounding style as any item from the pero.ROUNDING
            enum.
    
    Returns:
        float
            Rounded time in seconds.
    """
    
    pass
