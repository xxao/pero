#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from .. enums import *
from .. properties import *
from . formatter import Formatter


class ScalarFormatter(Formatter):
    """
    This formatter tool uses an automatic formatting of given number according
    to current 'domain', 'precision' and additional settings. It is typically
    used to format labels for standard numeric axes.
    
    A scientific notation style (e.g. 2e6) can be used to format numbers
    exceeding specific threshold, which can be specified by the 'sci_threshold'
    property as a power of 10. (E.g. if set to 3, all the values grater than
    1000 or smaller than -1000 wil be formatted with scientific notation.)
    
    The scientific notation suffix can be removed from labels by setting the
    'hide_suffix' property to True and it becomes available using the 'suffix'
    method. Specific formatting of the suffix can also be defined by the
    'suffix_template' property expecting the power as input (e.g. 'e{:.0f}').
    
    Properties:
        
        sci_notation: bool
            Specifies whether the scientific notation (e.g. 2e6) is enabled
            (True) or disabled (False).
        
        sci_threshold: int
            Specifies the threshold for 'domain' from which the scientific
            notation should be used as a power of 10.
        
        hide_suffix: bool
            Specifies whether the scientific notation suffix should be removed
            from the formatted value (True). The actual suffix can be retrieved
            by the 'suffix' method.
        
        suffix_template: str, None or UNDEF
            Specifies the format()-style template to be used for suffix
            formatting expecting the power as input (e.g. 'e{:.0f}').
    """
    
    sci_notation = BoolProperty(True, dynamic=False)
    sci_threshold = IntProperty(5, dynamic=False)
    hide_suffix = BoolProperty(False, dynamic=False)
    suffix_template = StringProperty(" (e{:.0f})", dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of ScalarFormatter."""
        
        super().__init__(**overrides)
        
        # init buffers
        self._power = 0
        self._last_digit = 0
        self._has_suffix = False
        self._is_dirty = True
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_scalar_formatter_property_changed)
    
    
    def format(self, value, *args, **kwargs):
        """
        Formats a given value using scalar formatting.
        
        Args:
            value: float
                Value to be formatted.
        
        Returns:
            str
                Formatted label.
        """
        
        # init formatting
        if self._is_dirty:
            self._init_formatting()
        
        # use suffix
        if self.hide_suffix and self._has_suffix:
            value = value / (10.**self._power)
            template = "{:1.%df}" % abs(self._last_digit - self._power)
        
        # use scientific notation
        elif self.sci_notation and self._has_suffix:
            
            last_digit = 0
            if value:
                value_power = int(math.floor(math.log10(abs(value))))
                if value_power > self._last_digit:
                    last_digit = self._last_digit - value_power
            
            template = "{:1.%de}" % abs(last_digit)
        
        # use current precision
        elif self._last_digit < 0:
            template = "{:0.%df}" % abs(self._last_digit)
        
        # make integer
        else:
            template = "{:0.0f}"
        
        # apply format
        label = template.format(value)
        
        # avoid '-0'
        if label[0] == '-' and float(label) == 0:
            label = label[1:]
        
        return label
    
    
    def suffix(self, *args, **kwargs):
        """
        Gets current labels suffix (e.g. e-2).
        
        Returns:
            str
                Labels suffix.
        """
        
        # init formatting
        if self._is_dirty:
            self._init_formatting()
        
        # return suffix
        if self.hide_suffix and self._has_suffix and self.suffix_template:
            return self.suffix_template.format(self._power)
        
        # not defined
        return ""
    
    
    def _init_formatting(self):
        """Initializes formatting based on current range."""
        
        # get range and precision
        domain = self.domain or 1.
        precision = self.precision or 1.
        
        # calc power and digits
        self._power = int(math.floor(math.log10(abs(domain))))
        self._has_suffix = abs(self._power) >= abs(self.sci_threshold)
        self._last_digit = int(math.floor(math.log10(abs(precision))))
        
        # reset flag
        self._is_dirty = False
    
    
    def _on_scalar_formatter_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        self._is_dirty = True
