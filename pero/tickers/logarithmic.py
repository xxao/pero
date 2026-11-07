"""Proposed replacement for pero/tickers/logarithmic.py; not installed."""

import math
from ..properties import IntProperty, NumProperty
from ..formatters import ScalarFormatter
from .ticker import Ticker
from .utils import *


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
            overrides['formatter'] = ScalarFormatter(trim_zeros=True)
        
        # init base
        super().__init__(**overrides)
    
    
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
        
        # constant range
        if start == end:
            major_ticks, minor_ticks = (start,), ()
            precision = start
        
        # linear range
        elif snap(hi - lo) < 1:
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
        
        lo, hi = sorted((start, end))
        lo = math.pow(self.base, math.floor(snap(math.log(lo, self.base))))
        hi = math.pow(self.base, math.ceil(snap(math.log(hi, self.base))))
        
        return (hi, lo) if start > end else (lo, hi)
    
    
    def _make_linear_ticks(self, start, end):
        """Makes ticks for linear range."""
        
        # make major ticks
        count = max(1, self.major_count)
        major_step = calc_step_size(end - start, count, (1, 2, 5))
        major_ticks = make_lin_ticks(start, end, major_step)
        
        # retry with finer spacing
        if not major_ticks:
            major_step = calc_step_size(end - start, count+1, (1, 2, 5))
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
        major_ticks = self._make_power_ticks(start, end, lo, hi, major_step)
        
        # generate subdivisions or consecutive powers
        if self.base == int(self.base):
            dense = make_log_ticks(start, end, self.base)
        else:
            dense = self._make_power_ticks(start, end, lo, hi, 1)
        
        # prefer dense ticks when their count is closer
        if abs(len(dense) - count) < abs(len(major_ticks) - count):
            major_ticks, major_step = dense, 1
        
        # ensure ticks available
        if not major_ticks:
            return self._make_linear_ticks(start, end)
        
        # use dense ticks at unit exponent steps
        if major_step == 1:
            minor_ticks = dense
        
        # use finer ticks for sparse grids
        else:
            minor_step = calc_step_size(major_step, self.minor_count, splits, step_base, exact=True)
            minor_step = max(1, minor_step)
            minor_ticks = self._make_power_ticks(start, end, lo, hi, minor_step)
        
        # calc precision
        precision = calc_precision(major_ticks)
        
        return major_ticks, minor_ticks, precision
    
    
    def _make_power_ticks(self, start, end, lo, hi, step):
        """Make ticks by step."""
        
        ticks = (math.pow(self.base, t) for t in make_lin_ticks(lo, hi, step))
        return tuple(x for x in ticks if start <= x <= end)
