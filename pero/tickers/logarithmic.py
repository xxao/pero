#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from .. enums import *
from ..properties import IntProperty, FloatRangeProperty
from ..formatters import ScalarFormatter
from .ticker import Ticker
from .utils import *


class LogTicker(Ticker):
    """
    This type of ticker generates nice looking ticks and labels according to
    logarithmic scale.
    
    Properties:
        
        base: int or float
            Specifies the logarithm base, greater than 1.
        
        major_count: int
            Specifies the expected number of major ticks to be generated for
            current range. The final number of ticks should be close but not
            necessary the same.
        
        minor_count: int
            Specifies the expected number of minor ticks to be generated between
            two major ticks. The final number of ticks should be close but not
            necessary the same.
    """
    
    base = FloatRangeProperty(10, minimum=1, minimum_incl=False, dynamic=False)
    major_count = IntProperty(7, dynamic=False)
    minor_count = IntProperty(4, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of LogTicker."""
        
        # init formatter
        if 'formatter' not in overrides:
            overrides['formatter'] = ScalarFormatter(trim_zeros=True)
        
        # init base
        super().__init__(**overrides)
        
        # lock formatter
        self.lock_property('formatter')
        
        # set base
        self.formatter.base = self.base
        
        # bind event
        self.bind(EVT_PROPERTY_CHANGED, self._on_log_ticker_property_changed)
    
    
    def make_ticks(self):
        """
        Generates ticks according to current settings.
        
        Returns:
            (float,), (float,)
                Generated major and minor ticks.
        """
        
        # normalize range
        start, end = sorted((self.start, self.end))
        
        # convert to exponents
        lo, hi = (snap(math.log(x, self.base)) for x in (start, end))
        
        # linear range
        if snap(hi - lo) < 1:
            major_ticks, minor_ticks, precision = self._make_linear_ticks(start, end)
        
        # exponent range
        else:
            major_ticks, minor_ticks, precision = self._make_exponent_ticks(start, end, lo, hi)
        
        # restore direction
        if self.start > self.end:
            major_ticks = major_ticks[::-1]
            minor_ticks = minor_ticks[::-1]
        
        # update formatter
        self.formatter.precision = precision
        self.formatter.domain = start if abs(lo) > abs(hi) else end
        
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
        
        # extend range
        lo, hi = extend_log_range(start, end, self.base)
        
        # extend constant range
        if lo == hi:
            lo, hi = lo / self.base, hi * self.base
        
        return lo, hi
    
    
    def _make_linear_ticks(self, start, end):
        """Makes ticks for linear range."""
        
        # make major ticks
        count = max(1, self.major_count)
        major_step = calc_step_size(end - start, count, (1, 2, 5))
        major_ticks = make_lin_ticks(start, end, major_step)
        
        # retry with finer spacing to avoid single tick
        while len(major_ticks) < 2 and count < 100:
            count += 1
            major_step = calc_step_size(end - start, count, (1, 2, 5))
            major_ticks = make_lin_ticks(start, end, major_step)
        
        # make major ticks
        minor_step = calc_step_size(major_step, self.minor_count, exact=True)
        minor_ticks = make_lin_ticks(start, end, minor_step)
        
        return major_ticks, minor_ticks, major_step
    
    
    def _make_exponent_ticks(self, start, end, lo, hi):
        """Makes ticks for exponent range."""
        
        # calc step
        count = max(1, self.major_count)
        step_base = 2 if self.base == 2 else 10
        splits = (1, 2, 3, 5)
        major_step = max(1, calc_step_size(hi - lo, count, splits))
        
        # make major
        major_ticks = make_power_ticks(start, end, self.base, major_step)
        
        # generate subdivisions or consecutive powers
        if self.base == int(self.base):
            dense = make_log_ticks(start, end, self.base)
        else:
            dense = make_power_ticks(start, end, self.base)
        
        # prefer dense ticks when their count is closer
        if abs(len(dense) - count) < abs(len(major_ticks) - count):
            major_ticks, major_step = dense, 1
        
        # make sure enough ticks available
        if len(major_ticks) < 2:
            major_ticks, major_step = make_power_ticks(start, end, self.base), 1
        if len(major_ticks) < 2:
            major_ticks = dense
        if len(major_ticks) < 2:
            return self._make_linear_ticks(start, end)
        
        # subdivide power intervals at unit exponent steps
        if major_step == 1:
            minor_ticks = make_log_ticks(start, end, self.base, self._calc_multiplier_step())
        
        # use finer ticks for sparse grids
        else:
            minor_step = calc_step_size(major_step, self.minor_count, splits, step_base, exact=True)
            minor_step = max(1, minor_step)
            minor_ticks = make_power_ticks(start, end, self.base, minor_step)
        
        # calc precision
        precision = calc_precision(major_ticks)
        
        return major_ticks, minor_ticks, precision
    
    
    def _calc_multiplier_step(self):
        """Calculates multiplier step to subdivide single power interval."""
        
        # use integer multipliers if dense enough (e.g. 2-9 for base 10)
        if self.base == int(self.base) and self.base - 1 >= self.minor_count:
            return 1
        
        # use fractional multipliers (e.g. 1.25, 1.5, 1.75 for base 2)
        return calc_step_size(self.base - 1, self.minor_count, (5, 2.5, 2, 1))
    
    
    def _on_log_ticker_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        # base changed
        if evt is None or evt.name == 'base':
            self.formatter.base = self.base
