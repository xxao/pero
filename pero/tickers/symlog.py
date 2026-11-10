#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from .. enums import *
from .. properties import *
from .. formatters import ScalarFormatter
from . ticker import Ticker
from . linear import LinTicker
from . logarithmic import LogTicker
from . utils import calc_precision, extend_range, extend_log_range


class SymlogTicker(Ticker):
    """
    This type of ticker generates ticks and labels for symmetric logarithmic
    scales. Ticks are logarithmic outside the [-threshold, threshold] interval
    and linear inside.
    
    Properties:
        
        base: int or float
            Specifies the logarithm base.
        
        threshold: int or float
            Positive, finite threshold for linear region.
        
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
    threshold = NumProperty(1, dynamic=False)
    major_count = IntProperty(7, dynamic=False)
    minor_count = IntProperty(4, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of SymlogTicker."""
        
        # init formatter
        if 'formatter' not in overrides:
            overrides['formatter'] = ScalarFormatter()
        
        # init base
        super().__init__(**overrides)
        
        # lock formatter
        self.lock_property('formatter')
        
        # set base
        self.formatter.base = self.base
        
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
        
        # get threshold
        thr = self.threshold
        
        # constant log range
        if start == end and abs(start) > thr:
            lo, hi = self._log_ticker.beautify(abs(start), abs(start))
            lo = max(thr, lo)
            return (-hi, -lo) if start < 0 else (lo, hi)
        
        # normalize range
        lo, hi = sorted((start, end))
        
        # use linear range
        if -thr <= lo <= hi <= thr:
            lo, hi = self._lin_ticker.beautify(lo, hi)
        
        # use log range
        else:
            
            # beautify lo
            if lo < -thr:
                lo = -extend_log_range(-lo, -lo, self.base)[1]
            elif lo > thr:
                lo = max(thr, extend_log_range(lo, lo, self.base)[0])
            else:
                lo = extend_range(lo, thr, thr)[0]
            
            # beautify hi
            if hi > thr:
                hi = extend_log_range(hi, hi, self.base)[1]
            elif hi < -thr:
                hi = -max(thr, extend_log_range(-hi, -hi, self.base)[0])
            else:
                hi = extend_range(-thr, hi, thr)[1]
        
        return (hi, lo) if start > end else (lo, hi)
    
    
    def _make_linear_ticks(self, start, end):
        """Makes ticks for linear-only range."""
        
        self._lin_ticker(
            start = start,
            end = end,
            major_step = UNDEF,
            major_count = self.major_count,
            minor_count = self.minor_count)
        
        major_ticks = self._lin_ticker.major_ticks()
        minor_ticks = self._lin_ticker.minor_ticks()
        
        return major_ticks, minor_ticks
    
    
    def _make_log_ticks(self, start, end):
        """Makes ticks for logarithmic range."""
        
        # init ticks
        major_ticks = []
        minor_ticks = []
        
        # get threshold
        thr = self.threshold
        
        # get linear range
        lin_start = max(start, -thr)
        lin_end = min(end, thr)
        
        # get log ranges
        log_ranges = ((-1, max(thr, -end), -start), (1, max(thr, start), end))
        log_ranges = [(sign, lo, hi) for sign, lo, hi in log_ranges if lo <= hi]
        
        # get absolute and relative spans
        lin_span = max(0, lin_end - lin_start)
        log_spans = [thr * (math.log(hi) - math.log(lo)) for _, lo, hi in log_ranges]
        total_span = lin_span + sum(log_spans)
        lin_share = lin_span / total_span if total_span else 0.0
        log_share = max(log_spans, default=0.0) / total_span if total_span else 0.0
        
        # get counts
        lin_major_count, lin_minor_count = self._distribute_ticks(lin_share)
        log_major_count, log_minor_count = self._distribute_ticks(log_share)
        
        # use longer side range to keep symmetry
        if len(log_ranges) == 2:
            hi = max(-start, end)
            log_ranges = [(-1, thr, hi), (1, thr, hi)]
        
        # add log range ticks
        for sign, lo, hi in log_ranges:
            
            self._log_ticker(
                start = lo,
                end = hi,
                major_count = log_major_count,
                minor_count = log_minor_count)
            
            major_ticks.extend(sign * t for t in self._log_ticker.major_ticks())
            if log_minor_count:
                minor_ticks.extend(sign * t for t in self._log_ticker.minor_ticks())
        
        # add linear range ticks
        if lin_start <= lin_end:
            
            self._lin_ticker(
                start = lin_start,
                end = lin_end,
                major_step = UNDEF,
                major_count = lin_major_count,
                minor_count = lin_minor_count)
            
            major_ticks.extend(t for t in self._lin_ticker.major_ticks() if t not in (-thr, thr))
            if lin_major_count >= 2:
                major_ticks.extend(t for t in (-thr, thr) if start <= t <= end)
            
            if lin_minor_count and max(-start, end) <= thr * self.base:
                minor_ticks.extend(self._lin_ticker.minor_ticks())
        
        # remove duplicates
        major_ticks = tuple(sorted(set(t for t in major_ticks if start <= t <= end)))
        minor_ticks = tuple(sorted(set(t for t in minor_ticks if start <= t <= end)))
        
        return major_ticks, minor_ticks
    
    
    def _distribute_ticks(self, span_share):
        """Calculates tick counts from its share of the total span."""
        
        if span_share <= 0:
            return 0, 0
        
        major_count = max(1, round(self.major_count * span_share))
        minor_budget = self.major_count * self.minor_count * span_share
        
        minor_count = (
            max(1, round(minor_budget / major_count))
            if minor_budget >= 0.5 else 0)
        
        return major_count, minor_count
    
    
    def _on_symlog_ticker_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        # base changed
        if evt is None or evt.name == 'base':
            self._log_ticker.base = self.base
            self.formatter.base = self.base
        
        # major count changed
        if evt is None or evt.name == 'major_count':
            self._lin_ticker.major_count = self.major_count
            self._log_ticker.major_count = self.major_count
        
        # minor count changed
        if evt is None or evt.name == 'minor_count':
            self._lin_ticker.minor_count = self.minor_count
            self._log_ticker.minor_count = self.minor_count
