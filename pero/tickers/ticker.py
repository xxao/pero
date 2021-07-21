#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. enums import *
from .. properties import *
from .. formatters import Formatter


class Ticker(PropertySet):
    """
    Abstract base class for various types of ticks and labels generators, which
    are typically used to generate nice looking ticks, labels and grids for
    charts.
    
    All derived classes have to implement the 'make_ticks' method, which is
    then automatically used to calculate major and minor ticks.
    
    Labels are automatically created from major ticks using specified
    'formatter'. The formatter 'domain' is automatically updated by current
    range. Its 'precision', however, must be updated manually in derived classes
    as needed.
    
    For some cases it is useful to hide either the first or the last tick and
    label, such as for radial axes. This can be achieved by setting the
    'hide_first' or 'hide_last' properties.
    
    Properties:
        
        start: int or float
            Specifies the start value of the range in data units.
        
        end: int or float
            Specifies the end value of the range in data units.
        
        formatter: pero.Formatter
            Specifies the formatter to be used to format labels.
        
        hide_first: bool
            Specifies whether the first tick and label should be removed.
        
        hide_last: bool
            Specifies whether the last tick and label should be removed.
    """
    
    start = NumProperty(UNDEF, dynamic=False)
    end = NumProperty(UNDEF, dynamic=False)
    
    formatter = Property(UNDEF, types=(Formatter,), dynamic=False)
    hide_first = BoolProperty(False, dynamic=False)
    hide_last = BoolProperty(False, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Ticker."""
        
        super().__init__(**overrides)
        
        # init buffers
        self._major_ticks = ()
        self._minor_ticks = ()
        self._labels = ()
        self._is_dirty = True
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_ticker_property_changed)
    
    
    def initialize(self):
        """Recalculates internal values to current settings if necessary."""
        
        # skip if not necessary
        if not self._is_dirty:
            return
        
        # reset buffers
        self._major_ticks = ()
        self._minor_ticks = ()
        self._labels = ()
        
        # update formatter
        self.formatter.domain = max(abs(self.start), abs(self.end))
        
        # make ticks
        major_ticks, minor_ticks = self.make_ticks()
        self._major_ticks = tuple(major_ticks)
        self._minor_ticks = tuple(minor_ticks)
        
        # reset flag
        self._is_dirty = False
    
    
    def make_ticks(self):
        """
        Generates ticks according to current settings. This method must be
        overridden in derived classes to provide specific mechanism to calculate
        major and minor ticks.
        
        Returns:
            (float,), (float,)
                Generated major and minor ticks.
        """
        
        raise NotImplementedError("The 'make_ticks' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def major_ticks(self):
        """
        Gets calculated major ticks.
        
        Returns:
            (float,)
                Major ticks values.
        """
        
        # recalculate values
        if self._is_dirty:
            self.initialize()
        
        # get ticks
        ticks = self._major_ticks
        
        if self.hide_first and len(ticks) > 0:
            ticks = ticks[1:]
        
        if self.hide_last and len(ticks) > 0:
            ticks = ticks[:-1]
        
        return ticks
    
    
    def minor_ticks(self):
        """
        Gets calculated minor ticks.
        
        Returns:
            (float,)
                Minor ticks values in data units.
        """
        
        # recalculate values
        if self._is_dirty:
            self.initialize()
        
        # get ticks
        ticks = self._minor_ticks
        
        if self.hide_first and len(ticks) > 0:
            ticks = ticks[1:]
        
        if self.hide_last and len(ticks) > 0:
            ticks = ticks[:-1]
        
        return ticks
    
    
    def labels(self):
        """
        Gets formatted labels for major ticks.
        
        Returns:
            (str,)
                Formatted major ticks labels.
        """
        
        # recalculate values
        if self._is_dirty:
            self.initialize()
        
        # format labels
        if not self._labels:
            self._labels = tuple(map(self.format, self._major_ticks))
        
        # get labels
        labels = self._labels
        
        if self.hide_first and len(labels) > 0:
            labels = labels[1:]
        
        if self.hide_last and len(labels) > 0:
            labels = labels[:-1]
        
        return labels
    
    
    def suffix(self):
        """
        Gets current suffix to be added to axis title (e.g. 10^5).
        
        Returns:
            str
                Labels suffix.
        """
        
        # recalculate values
        if self._is_dirty:
            self.initialize()
        
        # get current suffix
        return self.formatter.suffix()
    
    
    def format(self, value):
        """
        Formats given label value using current formatter.
        
        Args:
            value: any
                A value in data units to be formatted for label.
        
        Return:
            str
                Formatted label value.
        """
        
        # recalculate values
        if self._is_dirty:
            self.initialize()
        
        # apply formatting
        return self.formatter.format(value)
    
    
    def beautify(self, start, end):
        """
        Calculates visually nice range to cover given range.
        
        This method should be overridden in derived classes to provide specific
        mechanism to beautify given range.
        
        Args:
            start: int or float
                Minimum value of the range.
            
            end: int or float
                Maximum value of the range.
        
        Returns:
            (float, float)
                New extended range.
        """
        
        return start, end
    
    
    def _on_ticker_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        # mark as dirty
        self._is_dirty = True
        
        # reset buffers
        self._major_ticks = ()
        self._minor_ticks = ()
        self._labels = ()
