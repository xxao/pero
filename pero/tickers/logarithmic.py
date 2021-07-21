#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from .. properties import *
from .. formatters import ScalarFormatter
from . utils import *
from . ticker import Ticker


class LogTicker(Ticker):
    """
    This type of ticker generates nice looking ticks and labels according to
    logarithmic scale.
    
    Properties:
        
        base: int or float
            Specifies the logarithm base.
        
        major_count: int
            Specifies the expected number of major ticks to be generated for
            current range. The final number of ticks should be close but not
            necessary the same.
        
        minor_count: int
            Specifies the expected number of minor ticks to be generated between
            two major ticks. The final number of ticks should be close but not
            necessary the same.
    """
    
    base = NumProperty(10, dynamic=False)
    major_count = IntProperty(7, dynamic=False)
    minor_count = IntProperty(4, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of LogTicker."""
        
        # init formatter
        if 'formatter' not in overrides:
            overrides['formatter'] = ScalarFormatter()
        
        # init base
        super().__init__(**overrides)
    
    
    def make_ticks(self):
        """
        Generates ticks according to current settings.
        
        Returns:
            (float,), (float,)
                Generated major and minor ticks.
        """
        
        # get range
        start, end = self.start, self.end
        
        # check order
        flip = False
        if start > end:
            start, end = end, start
            flip = True
        
        # make major ticks
        major_ticks, step, stage = self._make_major_ticks(start, end, self.major_count, self.base)
        
        # make minor ticks
        minor_ticks = self._make_minor_ticks(start, end, self.minor_count, self.base, step, stage)
        
        # crop ticks to current range
        major_ticks = [x for x in major_ticks if start <= x <= end]
        minor_ticks = [x for x in minor_ticks if start <= x <= end]
        
        # flip order back
        if flip:
            major_ticks.reverse()
            minor_ticks.reverse()
        
        # update formatter
        if step < self.base:
            self.formatter.precision = step
        else:
            self.formatter.precision = end
        
        return tuple(major_ticks), tuple(minor_ticks)
    
    
    def beautify(self, start, end):
        """
        Calculates visually nice range to cover given range.
        
        Args:
            start: int or float
                Minimum value of the range.
            
            end: int or float
                Maximum value of the range.
        
        Returns:
            (float, float)
                New extended range.
        """
        
        # check order
        flip = False
        if start > end:
            start, end = end, start
            flip = True
        
        # recalculate start
        start = math.log(start, self.base)
        start = math.floor(start)
        start = math.pow(self.base, start)
        
        # recalculate end
        end = math.log(end, self.base)
        end = math.ceil(end)
        end = math.pow(self.base, end)
        
        return (start, end) if not flip else (end, start)
    
    
    def _make_major_ticks(self, start, end, count, base):
        """Makes major ticks."""
        
        lo = math.log(start, base)
        hi = math.log(end, base)
        domain = abs(hi - lo)
        
        stage1 = (count-domain)
        stage2 = (count-domain*(base-1))
        
        if domain >= count or abs(stage1) <= abs(stage2):
            
            count = min(domain, count)
            splits = (base, 1) if domain <= count else (1, 2, 5)
            step = step_size(domain, count, splits, base)
            
            ticks = make_ticks(lo, hi, step)
            ticks = tuple(map(lambda t: math.pow(base, t), ticks))
            
            return ticks, math.pow(base, step), 1
        
        domain = abs(end - start)
        splits = (base, 1) if base != 10 else (1, 2, 5)
        step = step_size(domain, count, splits, base)
        stage3 = (count - domain/step)
        
        if stage2 < stage3:
            ticks = make_log_ticks(start, end, base)
            return ticks, step, 2
        
        else:
            ticks = make_ticks(start, end, step)
            return ticks, step, 3
    
    
    def _make_minor_ticks(self, start, end, count, base, step, stage):
        """Makes minor ticks."""
        
        if stage != 1:
            step = step_size(step, count, (base, 1), base)
            return make_ticks(start, end, step)
        
        if step <= base:
            return make_log_ticks(start, end, base)
        
        start = math.log(start, base)
        end = math.log(end, base)
        
        step = math.log(step, base)
        step = step_size(step, count, (1, 2, 5), base)
        step = max(step, 1.)
        
        ticks = make_ticks(start, end, step)
        ticks = tuple(map(lambda t: math.pow(base, t), ticks))
        
        return ticks
