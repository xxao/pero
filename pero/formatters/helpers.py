#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from ..enums import TIME_FACTORS


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
    units = sorted(TIME_FACTORS.items(), key=lambda x:x[1], reverse=True)
    
    # init parts
    parts = {x[0]: 0.0 for x in units}
    
    # split time
    value = seconds
    for unit, f in units:
        count, rest = divmod(value, f)
        parts[unit] = count
        value = rest
    
    return parts
