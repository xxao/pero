#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from .. enums import *
from .. properties import *
from .. formatters import ScalarFormatter
from . ticker import Ticker
from . linear import LinTicker
from . logarithmic import LogTicker
from . utils import calc_precision


class SymlogTicker(Ticker):
    """
    This type of ticker generates ticks and labels for symmetric logarithmic
    scales. Ticks within [-threshold, threshold] are linear. Logarithmic ticks
    outside this region are anchored at threshold on both sides of zero.
    Ranges entirely within the linear region use LinTicker.
    
    Properties:
        
        threshold: int or float
            Positive, finite threshold for linear region. Defaults to 1.
            This value should match the threshold of the corresponding scale.
        
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
    
    threshold = RangeProperty(1, types=(float,), minimum=0, minimum_incl=False, dynamic=False)
    base = NumProperty(10, dynamic=False)
    major_count = IntProperty(7, dynamic=False)
    minor_count = IntProperty(4, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of SymlogTicker."""
        
        # init formatter
        if 'formatter' not in overrides:
            overrides['formatter'] = ScalarFormatter()
        
        # init base
        super().__init__(**overrides)
        
        # init linear ticker
        self._lin_ticker = LinTicker(
            major_count = self.major_count,
            minor_count = self.minor_count)
        
        # init log ticker
        self._log_ticker = LogTicker(
            base = self.base,
            major_count = self.major_count,
            minor_count = self.minor_count)
        
        # bind event
        self.bind(EVT_PROPERTY_CHANGED, self._on_symlog_ticker_property_changed)
    
    
    def make_ticks(self):
        """
        Generates ticks according to current settings.
        
        Returns:
            (float,), (float,)
                Generated major and minor ticks.
        """
        
        # normalize range
        start, end = sorted((self.start, self.end))
        
        # constant range
        if start == end:
            self.formatter.precision = calc_precision((start,))
            return (start,), ()
        
        # use linear range
        if -self.threshold <= start <= end <= self.threshold:
            major_ticks, minor_ticks = self._make_linear_ticks(start, end)
        
        # use log range
        else:
            major_ticks, minor_ticks = self._make_log_ticks(start, end)
        
        # update formatter
        self.formatter.precision = calc_precision(major_ticks)
        
        # restore direction
        if self.start > self.end:
            major_ticks = major_ticks[::-1]
            minor_ticks = minor_ticks[::-1]
        
        return major_ticks, minor_ticks
    
    
    def beautify(self, start, end):
        """
        Calculates visually nice range to cover given range.
        
        Args:
            start: int or float
                Start value of the range.
            
            end: int or float
                End value of the range.
        
        Returns:
            (float, float)
                New extended range.
        """
        
        # constant range
        if start == end:
            return start, end
        
        # normalize range
        lo, hi = sorted((start, end))
        
        # get threshold
        threshold = self.threshold
        
        # use linear range
        if -threshold <= lo <= hi <= threshold:
            self._lin_ticker.major_step = UNDEF
            lo, hi = self._lin_ticker.beautify(lo, hi)
        
        # use log range
        else:
            
            # update lin ticker
            self._lin_ticker.major_step = threshold
            
            # beautify lo
            if lo < -threshold:
                lo = self._log_ticker.beautify(1, -lo / threshold)[1] * -threshold
            elif lo > threshold:
                lo = self._log_ticker.beautify(lo / threshold, lo / threshold)[0] * threshold
            else:
                lo = self._lin_ticker.beautify(lo, threshold)[0]
            
            # beautify hi
            if hi > threshold:
                hi = self._log_ticker.beautify(1, hi / threshold)[1] * threshold
            elif hi < -threshold:
                hi = self._log_ticker.beautify(-hi / threshold, -hi / threshold)[0] * -threshold
            else:
                hi = self._lin_ticker.beautify(-threshold, hi)[1]
        
        return (hi, lo) if start > end else (lo, hi)
    
    
    def _make_linear_ticks(self, start, end):
        """Makes ticks for linear range."""
        
        self._lin_ticker(start=start, end=end, major_step=UNDEF)
        major_ticks = self._lin_ticker.major_ticks()
        minor_ticks = self._lin_ticker.minor_ticks()
        
        return major_ticks, minor_ticks
    
    
    def _make_log_ticks(self, start, end):
        """Makes ticks for logarithmic range."""
        
        # init ticks
        major_ticks = []
        minor_ticks = []
        
        # get threshold
        threshold = self.threshold
        
        # get linear range in threshold units
        linear_start = max(start, -threshold)
        linear_end = min(end, threshold)
        linear_span = max(0, linear_end - linear_start) / threshold
        
        # get log range
        log_ranges = ((-1, max(threshold, -end), -start), (1, max(threshold, start), end))
        log_ranges = [(sign, lo, hi) for sign, lo, hi in log_ranges if lo <= hi]
        log_spans = [math.log(hi / lo, self.base) for sign, lo, hi in log_ranges]
        
        # get total range
        total_span = linear_span + sum(log_spans)
        
        # allocate logarithmic ticks by region span and restore their signs
        for (sign, lo, hi), span in zip(log_ranges, log_spans):
            count = max(1, round(self.major_count * span / total_span))
            self._log_ticker(start=lo / threshold, end=hi / threshold, major_count=count)
            major_ticks.extend(sign * threshold * t for t in self._log_ticker.major_ticks())
            minor_ticks.extend(sign * threshold * t for t in self._log_ticker.minor_ticks())
        
        # add central ticks, zero and thresholds
        if linear_start <= linear_end:
            self._lin_ticker(start=linear_start, end=linear_end, major_step=threshold)
            major_ticks.extend(self._lin_ticker.major_ticks())
            minor_ticks.extend(self._lin_ticker.minor_ticks())
        
        # merge regions
        major_ticks = tuple(sorted(set(t for t in major_ticks if start <= t <= end)))
        minor_ticks = tuple(sorted(set(t for t in minor_ticks if start <= t <= end)))
        
        return major_ticks, minor_ticks
    
    
    def _on_symlog_ticker_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        if evt is None or evt.name == 'base':
            self._log_ticker.base = self.base
        
        if evt is None or evt.name == 'major_count':
            self._lin_ticker.major_count = self.major_count
            self._log_ticker.major_count = self.major_count
        
        if evt is None or evt.name == 'minor_count':
            self._lin_ticker.minor_count = self.minor_count
            self._log_ticker.minor_count = self.minor_count
