#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math


def step_size(domain, count=7, splits=(5, 3, 2, 1), base=10):
    """
    Calculates visually nice step size for given range.
    
    Args:
        domain: int or float
            Absolute value of current range.
        
        count: int
            Expected number of ticks.
        
        splits: (float,)
            Allowed splits.
        
        base: int
            Log base.
    
    Returns:
        float
            Step size.
    """
    
    ideal = math.fabs(domain) / float(max(1, count))
    log = math.log(ideal, base)
    power = math.floor(log)
    fraction = log - power
    error = float('inf')  # fraction
    
    factor = 1.
    for split in splits:
        e = math.fabs(fraction - math.log(split, base))
        if e < error:
            factor = split
            error = e
    
    step = factor * math.pow(base, power)
    
    return step


def make_ticks(start, end, step):
    """
    Makes equidistant ticks for given range and step size.
    
    Args:
        start: int or float
            Minimum value of the range.
        
        end: int or float
            Maximum value of the range.
        
        step: float
            Step size.
    
    Returns:
        (float,)
            Ticks values.
    """
    
    # init buffer
    ticks = []
    
    # ascending
    if start < end:
        tick = math.ceil(float(start) / step) * step
        while tick <= end:
            ticks.append(tick)
            tick += step
    
    # descending
    else:
        tick = math.floor(float(start) / step) * step
        while tick >= end:
            ticks.append(tick)
            tick -= step
    
    return tuple(ticks)


def make_log_ticks(start, end, base):
    """pass"""
    
    ticks = []
    
    lo = round(math.log(start, base)) - 1
    hi = round(math.log(end, base)) + 1
    
    while lo < hi:
        
        p = math.pow(base, lo)
        lo += 1
        
        b = 1
        while b < base:
            
            t = p*b
            b += 1
            
            if t < start:
                continue
            if t > end:
                break
            
            ticks.append(t)
    
    return ticks
