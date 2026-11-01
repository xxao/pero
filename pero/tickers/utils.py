#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math


def snap(x):
    """Snaps value to nearest integer."""
    
    n = round(x)
    return n if abs(x - n) <= min(4 * math.ulp(x), 1e-7) else x


def calc_step_size(domain, count=7, splits=(5, 3, 2, 1), base=10, exact=False):
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
        
        exact: bool
            If set to True, the final step should fit the domain exactly.
    
    Returns:
        float
            Step size.
    """
    
    domain = abs(domain)
    count = max(1, count)
    ideal = domain / count
    pw = base ** math.floor(math.log(ideal, base))
    
    steps = [
        split * scale
        for scale in (pw, pw * base)
        for split in splits]
    
    if exact:
        
        fitting = []
        for step in steps:
            intervals = snap(domain / step)
            if intervals >= 1 and intervals == round(intervals):
                fitting.append(step)
        
        if not fitting:
            return domain / count
        
        steps = fitting
    
    return min(steps, key=lambda step: (
        abs(domain / step - count),
        abs(math.log(step / ideal, base))))


def calc_precision(ticks):
    """
    Finds decimal precision for finite ticks.
    
    Args:
        ticks: (float,)
            Ticks to analyze.
    
    Returns:
        float
            Precision.
    """
    
    # iit digits
    smallest = min((abs(t) for t in ticks if t), default=1.0)
    digits = -math.floor(math.log10(smallest))
    
    # increase digits until rounding preserves all ticks
    count = len(set(ticks))
    while True:
        
        # round and count
        rounded = [round(x, digits) for x in ticks]
        
        # not all ticks retained
        if len(set(rounded)) != count:
            digits += 1
            continue
        
        # check resolution
        merged = zip(ticks, rounded)
        if all((t == 0 or rt != 0) and abs(t - rt) <= 4 * math.ulp(t) for t, rt in merged):
            return max(10.0 ** -digits, math.ulp(0.0))
        
        # add digit
        digits += 1


def make_lin_ticks(start, end, step):
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
    
    # reversed
    if start > end:
        return make_lin_ticks(end, start, step)[::-1]
    
    # init buffer
    ticks = []
    
    # init range
    first = math.ceil(snap(start / step))
    last = math.floor(snap(end / step))
    count = max(0, last - first + 1)
    
    # add ticks
    for i in range(count):
        tick = (first + i) * step
        tick = min(end, max(start, tick))
        if not ticks or tick != ticks[-1]:
            ticks.append(tick)
    
    return tuple(ticks)


def make_log_ticks(start, end, base):
    """
    Makes logarithmic ticks for given range and base.
    
    Args:
        start: int or float
            Minimum value of the range.
        
        end: int or float
            Maximum value of the range.
        
        base: float
            Logarithm base.
    
    Returns:
        (float,)
            Ticks values.
    """
    
    ticks = []
    
    lo = math.floor(snap(math.log(start, base)))
    hi = math.floor(snap(math.log(end, base))) + 1
    
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
