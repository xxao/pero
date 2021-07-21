#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. properties import *


class Scale(PropertySet):
    """
    Abstract base class for various types of scales, which are used to convert
    values between two dimensions. Typically they are used in plotting for
    conversion between real data values into device screen units, conversion
    of values into categories or levels etc.
    
    If possible, derived classes should implement conversion methods for both
    directions: the 'scale' method, which converts values from the input range
    to output range and the 'invert' method, which converts from the output
    range to input range.
    
    To convert more data conveniently and/or efficiently, the scales can convert
    not only a single value but whole sequence such as list or numpy.array at
    once. For custom scales be sure this functionality is kept.
    
    Properties:
        
        in_range: (any,), None or UNDEF
            Specifies the input values or range.
        
        out_range: (any,), None or UNDEF
            Specifies the output values or range.
    """
    
    in_range = TupleProperty((), dynamic=False, nullable=True)
    out_range = TupleProperty((), dynamic=False, nullable=True)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "%s -> %s" % (self.in_range, self.out_range)
    
    
    def __repr__(self):
        """Gets debug string representation."""
        
        return "%s(%s)" % (self.__class__.__name__, self.__str__())
    
    
    def scale(self, value, *args, **kwargs):
        """
        Returns corresponding output-range value for given input-range value.
        
        This method should be overridden in derived classes to provide specific
        mechanism to convert from input to output range.
        """
        
        raise NotImplementedError("The 'scale' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def invert(self, value, *args, **kwargs):
        """
        Returns corresponding input-range value for given output-range value.
        
        This method should be overridden in derived classes to provide specific
        mechanism to convert from output to input range.
        """
        
        raise NotImplementedError("The 'invert' method is not implemented for '%s'." % self.__class__.__name__)
