#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from ..enums import *
from ..properties import *
from .formatter import Formatter


class SplitFormatter(Formatter):
    """
    This formatter tool uses defined splits to denote scale and attach
    optional 'units'. E.g. 1000 with 'Hz' units will be formatted into '1 kHz'
    label.
    
    The number of visible decimal places is determined automatically by current
    'precision' and 'domain' but it can also be specified directly using the
    'places' property.
    
    Sometimes it might be handy to just format the number and remove the whole
    suffix (the split symbol and units) from all the labels. This can be
    achieved by setting the 'hide_suffix' property to True and then the actual
    suffix can be retrieved using the 'suffix' method.
    
    Properties:
        
        prefixes: {str: int}
            Prefixes definition.
        
        units: str, None or UNDEF
            Specifies the optional units to be added right after a formatted
            label.
        
        places: int or UNDEF
            Specifies the requested number of decimal placed to show. If not
            specified, the formatting is automatically set by current
            'precision' and 'domain'.
        
        hide_suffix: bool
            Specifies whether the whole suffix (the split symbol and units)
            should be removed from the formatted values (True). The actual
            suffix can then be retrieved using the 'suffix' method.
        
        suffix_template: str, None or UNDEF
            Specifies the format()-style template to be used for suffix
            formatting.
    """
    
    splits = DictProperty(SPLITS_ENG, dynamic=False)
    units = StringProperty(UNDEF, dynamic=False, nullable=True)
    places = IntProperty(UNDEF, dynamic=False)
    
    hide_suffix = BoolProperty(False, dynamic=False)
    suffix_template = StringProperty(" ({0})", dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of SplitFormatter."""
        
        super().__init__(**overrides)
        
        # init buffers
        self._power = 0
        self._suffix = ""
        self._template = None
        
        self._splits = None
        self._is_dirty = True
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_split_formatter_property_changed)
    
    
    def format(self, value, *args, **kwargs):
        """
        Formats given value using current formatting.

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
            value /= self._power
        
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
        if self.hide_suffix and self._suffix and self.suffix_template:
            return self.suffix_template.format(self._suffix)
        
        # return suffix
        return ""
    
    
    def _init_formatting(self):
        """Initializes formatting based on current settings."""
        
        # reset
        self._power = 0
        self._suffix = ""
        self._template = None
        self._is_dirty = False
        
        # init splits
        self._splits = {v: k for k, v in self.splits.items()}
        
        # check domain
        if not self.domain:
            return
        
        # make template
        self._template = self._make_template(abs(self.domain))
    
    
    def _make_template(self, domain):
        """Creates template to cover expected range."""
        
        # get power
        splits = tuple(sorted(self._splits.keys(), reverse=True))
        for split in splits:
            if domain / split >= 1.:
                self._power = split
                break
        
        self._power = min(self._power, max(splits))
        self._power = max(self._power, min(splits))
        
        # get suffix
        self._suffix = self._splits.get(self._power, "")
        
        # add units
        if self.units:
            self._suffix += self.units
        
        # init direct suffix
        suffix = "" if self.hide_suffix else self._suffix
        if suffix:
            suffix = " " + suffix
        
        # get places
        places = 0
        if self.places is not UNDEF:
            places = int(self.places)
        
        elif self.precision and self.precision < domain:
            last_digit = int(math.floor(math.log10(abs(self.precision))))
            power = int(math.floor(math.log10(self._power)))
            places = power - last_digit
        
        # make template
        return "{:.%df}%s" % (max(0, places), suffix)
    
    
    def _on_split_formatter_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        self._is_dirty = True


class EngFormatter(SplitFormatter):
    """Special type of pero.SplitFormatter predefined for engineering notation."""
    
    splits = DictProperty(SPLITS_ENG, dynamic=False)


class BytesFormatter(SplitFormatter):
    """Special type of pero.SplitFormatter predefined for bytes scale."""
    
    splits = DictProperty(SPLITS_BYTES, dynamic=False)
    units = StringProperty("B", dynamic=False, nullable=True)


class SecondsFormatter(SplitFormatter):
    """Special type of pero.SplitFormatter predefined for time scale."""
    
    splits = DictProperty(SPLITS_TIME, dynamic=False)
