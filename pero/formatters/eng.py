#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from .. enums import *
from .. properties import *
from . formatter import Formatter


class EngFormatter(Formatter):
    """
    This formatter tool uses engineering prefixes to represent powers of 1000
    with optional 'units' attached. E.g. 1000 with 'Hz' units will be formatted
    into 1 kHz label.
    
    The number of visible decimal places is determined automatically by current
    'precision' and 'domain' but it can also be specified directly using the
    'places' property.
    
    Sometimes it might be handy to just format the number and remove the whole
    suffix (the multiplier symbol and units) from all the labels. This can be
    achieved by setting the 'hide_suffix' property to True and then the actual
    suffix can be retrieved using the 'suffix' method.
    
    Properties:
        
        units: str, None or UNDEF
            Specifies the optional units to be added right after a formatted
            label.
        
        places: int or UNDEF
            Specifies the requested number of decimal placed to show. If not
            specified, the formatting is automatically set by current
            'precision' and 'domain'.
        
        hide_suffix: bool
            Specifies whether the whole suffix (the multiplier symbol and units)
            should be removed from the formatted values (True). The actual
            suffix can then be retrieved using the 'suffix' method.
    """
    
    units = StringProperty(UNDEF, dynamic=False, nullable=True)
    places = IntProperty(UNDEF, dynamic=False)
    hide_suffix = BoolProperty(False, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of EngFormatter."""
        
        super().__init__(**overrides)
        
        # init buffers
        self._power = 0
        self._suffix = ""
        self._template = None
        
        self._prefixes = None
        self._is_dirty = True
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_eng_formatter_property_changed)
    
    
    def format(self, value, *args, **kwargs):
        """
        Formats a given value using engineering formatting.
        
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
        
        # get template
        template = self._template
        if not template:
            template = self._make_template(value)
        
        # apply power
        if self._power:
            value = value / (10.**self._power)
        
        # apply template
        return template.format(value)
    
    
    def suffix(self, *args, **kwargs):
        """
        Gets current (or the latest) suffix (e.g. kHz).
        
        Returns:
            str
                Labels suffix.
        """
        
        # init formatting
        if self._is_dirty:
            self._init_formatting()
        
        # return suffix
        return self._suffix
    
    
    def _init_formatting(self):
        """Initializes formatting based on current settings."""
        
        # reset
        self._power = 0
        self._suffix = ""
        self._template = None
        self._is_dirty = False
        
        # init prefixes
        self._prefixes = {v: k for k, v in ENG_PREFIXES.items()}
        
        # check domain
        if not self.domain:
            return
        
        # make template
        self._template = self._make_template(abs(self.domain))
    
    
    def _make_template(self, domain):
        """Creates template to cover expected range."""
        
        # get power
        self._power = int(math.floor(math.log10(abs(domain)) / 3) * 3) if domain else 0
        self._power = min(self._power, max(self._prefixes.keys()))
        self._power = max(self._power, min(self._prefixes.keys()))
        
        # get suffix
        suffix = self._prefixes[self._power]
        
        # add units
        if self.units:
            suffix += self.units
        
        # hide suffix
        if self.hide_suffix:
            self._suffix = suffix
            suffix = ""
        
        # add spacer
        if suffix:
            suffix = " " + suffix
        
        # get places
        places = 0
        
        if self.places is not UNDEF:
            places = int(self.places)
        
        elif self.precision and self.precision < domain:
            last_digit = int(math.floor(math.log10(abs(self.precision))))
            places = self._power - last_digit
        
        # make template
        return "{:.%df}%s" % (max(0, places), suffix)
    
    
    def _on_eng_formatter_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        self._is_dirty = True
