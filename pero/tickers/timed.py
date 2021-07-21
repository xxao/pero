#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. formatters import TimeFormatter
from .. formatters.utils import *
from . utils import *
from . ticker import Ticker


class TimeTicker(Ticker):
    """
    This type of ticker generates nice looking ticks and labels for time data
    assuming all given data are in seconds. The major and the minor steps are
    calculated automatically according to current range, however, both can be
    specified if needed. The label 'formatter' is by default set to
    pero.TimeFormatter, but can be changed if needed.
    
    Properties:
        
        major_step: int, float or UNDEF
            Specifies the fixed step in seconds to be used for major ticks and
            labels. If not provided the value is determined automatically base
            on current range.
        
        major_count: int
            Specifies the expected number of major ticks to be generated for
            current range. The final number of ticks should be close but not
            necessary the same.
        
        minor_step: int, float or UNDEF
            Specifies the fixed step in seconds to be used for minor ticks. If
            not provided the value is determined automatically base on major
            ticks range.
        
        minor_count: int
            Specifies the expected number of minor ticks to be generated between
            two major ticks. The final number of ticks should be close but not
            necessary the same.
    """
    
    major_step = NumProperty(UNDEF, dynamic=False)
    major_count = IntProperty(7, dynamic=False)
    
    minor_step = NumProperty(UNDEF, dynamic=False)
    minor_count = IntProperty(5, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of TimeTicker."""
        
        # init formatter
        if 'formatter' not in overrides:
            overrides['formatter'] = TimeFormatter(rounding=ROUNDING.HALFUP)
        
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
            major_step = self._calc_step(domain, self.major_count)
        
        # calc minor step size
        minor_step = self.minor_step
        if minor_step is UNDEF:
            minor_step = self._calc_step(major_step, self.minor_count)
        
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
            step = self._calc_step(abs(end - start), self.major_count)
        
        # extend range
        start = math.floor(start / step) * step
        end = math.ceil(end / step) * step
        
        return (start, end) if not flip else (end, start)
    
    
    def _calc_step(self, domain, count):
        """Calculates minor step size."""
        
        # split time
        parts = split_time(domain)
        
        # get split
        if parts["h"] or parts["m"] or parts["s"]:
            splits = (30, 15, 10, 5, 2, 1)
            base = 60
        
        else:
            splits = (5, 2, 1)
            base = 10
        
        # calc step size
        step = step_size(domain, count, splits, base)
        
        return step
