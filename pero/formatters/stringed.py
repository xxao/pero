#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. properties import *
from . formatter import Formatter


class EmptyFormatter(Formatter):
    """This formatter tool returns an empty string for any given value."""
    
    
    def format(self, value, *args, **kwargs):
        """
        Returns an empty string for any given value.
        
        Args:
            value: any
                Value to be formatted.
        
        Returns:
            str
                Empty string.
        """
        
        return ""


class StrFormatter(Formatter):
    """
    This formatter tool uses the newer format()-style templates to format
    given values.
    
    Properties:
        
        template: str
            Specifies the format()-style template to be used for custom
            formatting.
        
        trim: bool
            Specifies whether to automatically remove leading and trailing
            whitespace.
    """
    
    template = StringProperty("{0}", dynamic=False)
    trim = BoolProperty(True, dynamic=False, nullable=True)
    
    
    def format(self, value, *args, **kwargs):
        """
        Formats given value using custom formatting template.
        
        Args:
            value: ?
                Value to be formatted.
        
        Returns:
            str
                Formatted label.
        """
        
        # format and trim
        if self.trim:
            return self.template.format(value).strip()
        
        # format only
        return self.template.format(value)


class PrintfFormatter(Formatter):
    """
    This formatter tool uses the old %-style templates to format given values.
    
    Properties:
        
        template: str
            Specifies the %-style template to be used for custom formatting.
        
        trim: bool
            Specifies whether to automatically remove leading and trailing
            whitespace.
    """
    
    template = StringProperty('%s', dynamic=False)
    trim = BoolProperty(True, dynamic=False, nullable=True)
    
    
    def format(self, value, *args, **kwargs):
        """
        Formats given value using custom formatting template.
        
        Args:
            value: any
                Value to be formatted.
        
        Returns:
            str
                Formatted label.
        """

        # format and trim
        if self.trim:
            return (self.template % value).strip()
        
        # format only
        return self.template % value
