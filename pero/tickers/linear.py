#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from .. properties import *
from .. formatters import ScalarFormatter
from . utils import *
from . ticker import Ticker


class LinTicker(Ticker):
    """
    
    This type of ticker generates nice looking ticks and labels according to
    linear scale. The major and the minor steps are calculated automatically
    according to current range, however, both can be specified if needed. The
    label 'formatter' is by default set to pero.ScalarFormatter, but can be
    changed if needed.
    
    Properties:
        
        major_step: int, float or UNDEF
            Specifies the fixed step to be used for major ticks and labels. If
            not provided the value is determined automatically base on current
            range.
        
        major_count: int
            Specifies the expected number of major ticks to be generated for
            current range. The final number of ticks should be close but not
            necessary the same.
        
        major_splits: tuple of int
            Specifies the allowed splits to generate nice major ticks.
        
        minor_step: int, float or UNDEF
            Specifies the fixed step to be used for minor ticks. If not provided
            the value is determined automatically base on major ticks range.
        
        minor_count: int
            Specifies the expected number of minor ticks to be generated between
            two major ticks. The final number of ticks should be close but not
            necessary the same.
        
        minor_splits: tuple of int
            Specifies the allowed splits to generate nice minor ticks.
    """
    
    major_step = NumProperty(UNDEF, dynamic=False)
    major_count = IntProperty(7, dynamic=False)
    major_splits = TupleProperty((5, 3, 2, 1), intypes=(int, float), dynamic=False)
    
    minor_step = NumProperty(UNDEF, dynamic=False)
    minor_count = IntProperty(4, dynamic=False)
    minor_splits = TupleProperty((5, 2, 1), intypes=(int, float), dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of LinTicker."""
        
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
        domain = abs(end - start)
        
        # calc major step size
        major_step = self.major_step
        if major_step is UNDEF:
            major_step = step_size(domain, self.major_count, self.major_splits)
        
        # calc minor step size
        minor_step = self.minor_step
        if minor_step is UNDEF:
            minor_step = step_size(major_step, self.minor_count, self.minor_splits)
        
        # make ticks
        major_ticks = make_ticks(start, end, major_step)
        minor_ticks = make_ticks(start, end, minor_step)
        
        # update formatter
        self.formatter.precision = abs(major_step)
        
        return major_ticks, minor_ticks
    
    
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
        
        # calc major step size
        step = self.major_step
        if step is UNDEF:
            step = step_size(abs(end - start), self.major_count, self.major_splits)
        
        # extend range
        start = math.floor(start / step) * step
        end = math.ceil(end / step) * step
        
        return (start, end) if not flip else (end, start)
