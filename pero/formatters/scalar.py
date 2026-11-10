#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from .. enums import *
from .. properties import *
from . formatter import Formatter
from . utils import *


class ScalarFormatter(Formatter):
    """
    This formatter tool uses an automatic formatting of given number according
    to current 'domain', 'precision' and additional settings. It is typically
    used to format labels for standard numeric axes.
    
    A scientific notation style (e.g. 2e6) can be used to format numbers
    exceeding specific threshold, which can be specified by the 'sci_threshold'
    property as a power of 'base'. (E.g. if set to 3, all the values grater
    than 1000 or smaller than -1000 wil be formatted with scientific notation.)
    
    The scientific notation suffix can be removed from labels by setting the
    'hide_suffix' property to True and it becomes available using the 'suffix'
    method. Specific formatting of the suffix can also be defined by the
    'suffix_template' property expecting the power as input (e.g. 'e{:.0f}').
    
    Properties:
        
        base: int or float
            Specifies an exponent base used for scientific notation.
        
        sci_notation: bool
            Specifies whether the scientific notation (e.g. 2e6) is enabled
            (True) or disabled (False).
        
        sci_threshold: int
            Specifies the threshold for 'domain' from which the scientific
            notation should be used as a power of 'base'.
        
        trim_zeros: bool
            Specifies whether redundant fractional zeros are removed from labels.
        
        hide_suffix: bool
            Specifies whether the scientific notation suffix should be removed
            from the formatted value (True). The actual suffix can be retrieved
            by the 'suffix' method.
        
        suffix_template: str, None or UNDEF
            Specifies the format()-style template to be used for suffix
            formatting expecting the power as input (e.g. 'e{:.0f}'). Named
            'base' and 'power' fields are also available. If set to UNDEF,
            the default suffix is used based on current 'base'.
    """
    
    base = NumProperty(10, dynamic=False)
    sci_notation = BoolProperty(True, dynamic=False)
    sci_threshold = IntProperty(5, dynamic=False)
    trim_zeros = BoolProperty(True, dynamic=False)
    
    hide_suffix = BoolProperty(False, dynamic=False)
    suffix_template = StringProperty(UNDEF, dynamic=False, nullable=True)
    
    
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
        
        # check value
        if not value:
            return "0"
        
        # use scientific notation
        if self.sci_notation and self._has_suffix and not self.hide_suffix:
            if self.base == 10:
                return self._format_sci_10(value)
            return self._format_sci_base(value)
        
        # use fixed notation (scaled if suffix is hidden)
        power = self._power if self.hide_suffix and self._has_suffix else 0
        digits = max(0, -self._get_digits(power))
        label = "{:.{}f}".format(value / self.base**power, digits)
        label = self._trim_zeros(label)
        
        # avoid '-0'
        return label.lstrip('-') if float(label) == 0 else label
    
    
    def suffix(self, *args, **kwargs):
        """
        Gets current labels suffix (e.g. e2).
        
        Returns:
            str
                Labels suffix.
        """
        
        # init formatting
        if self._is_dirty:
            self._init_formatting()
        
        # check suffix
        if not self.hide_suffix or not self._has_suffix:
            return ""
        
        # get template
        template = self.suffix_template
        if template is UNDEF:
            template = " (e{power})" if self.base == 10 else " (×{base}^{power})"
        
        # check template
        if not template:
            return ""
        
        # apply template
        base = "{:.15g}".format(self.base)
        return template.format(self._power, base=base, power=self._power)
    
    
    def _init_formatting(self):
        """Initializes formatting based on current range."""
        
        # get range and precision
        domain = self.domain or 1.
        precision = self.precision or 1.
        
        # calc power and digits
        self._power = calc_power(abs(domain), self.base)
        self._has_suffix = abs(self._power) >= abs(self.sci_threshold)
        self._last_digit = int(math.floor(math.log10(abs(precision))))
        
        # reset flag
        self._is_dirty = False
    
    
    def _get_digits(self, power):
        """Gets last significant decimal digit relative to base^power."""
        
        return math.floor(math.log10(abs(self.precision or 1.)) - power * math.log10(self.base))
    
    
    def _format_sci_10(self, value):
        """Formats given value as 1.2e+03."""
        
        # get sign and power
        sign = "-" if value < 0 else ""
        value = abs(value)
        power = calc_power(value, self.base)
        
        # use standard notation
        digits = max(0, -self._get_digits(power))
        
        # avoid digits beyond the float's shortest representation
        if self.trim_zeros:
            sig = repr(float(value)).partition('e')[0].replace('.', '').strip('0')
            digits = min(digits, max(0, len(sig) - 1))
        
        # prepare label
        mantissa, _, exponent = "{:.{}e}".format(value, digits).partition('e')
        mantissa = self._trim_zeros(mantissa)
        
        return "%s%se%s" % (sign, mantissa, exponent)
    
    
    def _format_sci_base(self, value):
        """Formats given value as number×base^power."""
        
        # get sign and power
        sign = "-" if value < 0 else ""
        value = abs(value)
        power = calc_power(value, self.base)
        
        # get mantissa (fix rounding overflow)
        for power in (power, power + 1):
            digits = max(0, -self._get_digits(power))
            mantissa = "{:.{}f}".format(value / self.base**power, digits)
            if float(mantissa) < self.base:
                break
        
        # prepare label
        mantissa = self._trim_zeros(mantissa)
        coeff = "" if mantissa == "1" else mantissa + "×"
        base = "{:.15g}".format(self.base)
        
        return "%s%s%s^%d" % (sign, coeff, base, power)
    
    
    def _trim_zeros(self, label):
        """Removes redundant fractional zeros if enabled."""
        
        if self.trim_zeros and '.' in label:
            return label.rstrip('0').rstrip('.')
        
        return label
    
    
    def _on_scalar_formatter_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        self._is_dirty = True
