#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from .. enums import *
from .. properties import *


class Interpol(PropertySet):
    """
    Abstract base class for various types of interpolators. The interpolators
    are used within continuous scales to convert values between two dimensions.
    Such conversion is always done in two steps: normalizing given value within
    input range and de-normalizing the normalized value within output range. For
    such functionality each interpolator should implement specific methods for
    'normalize' and 'denormalize' values within provided ranges.
    
    In some cases like conversion of whole data series the input value is
    represented as a sequence of values rather than a single value. The
    interpolator therefore should be designed to accept such data type as well.
    """
    
    
    def normalize(self, x, start, end):
        """
        Calculates normalized value within specified range.
        
        Args:
            x: float or (float,)
                Value(s) to be normalized.
            
            start: float
                Start of the range to normalize into.
            
            end: float
                End of the range to normalize into.
        
        Returns:
            float or (float,)
                Normalized value(s).
        """
        
        raise NotImplementedError("The 'normalize' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def denormalize(self, x, start, end):
        """
        Calculates de-normalized value within specified range.
        
        Args:
            x: float or (float,)
                Normalized value(s) to be converted.
            
            start: float
                Start of the range to de-normalize from.
            
            end: float
                End of the range to de-normalize from.
        
        Returns:
            float or (float,)
                De-normalized value(s).
        """
        
        raise NotImplementedError("The 'normalize' method is not implemented for '%s'." % self.__class__.__name__)


class LinInterpol(Interpol):
    """
    This type of interpolator applies linear interpolation within specified
    ranges.
    """
    
    
    def normalize(self, x, start, end):
        """
        Calculates normalized value within specified range.
        
        Args:
            x: float or numpy.ndarray
                Value(s) to be normalized.
            
            start: float
                Start of the range to normalize into.
            
            end: float
                End of the range to normalize into.
        
        Returns:
            float or numpy.ndarray
                Normalized value(s).
        """
        
        return (x - start) / float(end - start)
    
    
    def denormalize(self, x, start, end):
        """
        Calculates de-normalized value within specified range.
        
        Args:
            x: float or numpy.ndarray
                Normalized value(s) to be converted.
            
            start: float
                Start of the range to de-normalize from.
            
            end: float
                End of the range to de-normalize from.
        
        Returns:
            float or numpy.ndarray
                De-normalized value(s).
        """
        
        return start + x * (end - start)
    

class LogInterpol(Interpol):
    """
    This type of interpolator applies logarithmic interpolation within specified
    ranges.
    """
    
    
    def normalize(self, x, start, end):
        """
        Calculates normalized value within specified range.
        
        Args:
            x: float or numpy.ndarray
                Value(s) to be normalized.
            
            start: float
                Start of the range to normalize into.
            
            end: float
                End of the range to normalize into.
        
        Returns:
            float, numpy.ndarray
                Normalized value(s).
        """
        
        return numpy.log(x / float(start)) / numpy.log(end / float(start))
    
    
    def denormalize(self, x, start, end):
        """
        Calculates de-normalized value within specified range.
        
        Args:
            x: float or numpy.ndarray
                Normalized value(s) to be converted.
            
            start: float
                Start of the range to de-normalize from.
            
            end: float
                End of the range to de-normalize from.
        
        Returns:
            value: float or numpy.ndarray
                De-normalized value(s).
        """
        
        return numpy.power(end, x) * numpy.power(start, 1-x)
    

class PowInterpol(Interpol):
    """
    This type of interpolator applies exponential interpolation within specified
    ranges.
    
    Properties:
        
        power: int or float
            Specifies the exponent to be used.
    """
    
    power = FloatProperty(1, dynamic=False)
    
    
    def normalize(self, x, start, end):
        """
        Calculates normalized value within specified range.
        
        Args:
            x: float or numpy.ndarray
                Value(s) to be normalized.
            
            start: float
                Start of the range to normalize into.
            
            end: float
                End of the range to normalize into.
        
        Returns:
            float or numpy.ndarray
                Normalized value(s).
        """
        
        power = self.power
        a = numpy.power(start, power)
        b = numpy.power(end, power) - a
        
        return (numpy.power(x, power) - a) / float(b)
    
    
    def denormalize(self, x, start, end):
        """
        Calculates de-normalized value within specified range.
        
        Args:
            x: float or numpy.ndarray
                Normalized value(s) to be converted.
            
            start: float
                Start of the range to de-normalize from.
            
            end: float
                End of the range to de-normalize from.
        
        Returns:
            float or numpy.ndarray
                De-normalized value(s).
        """
        
        power = self.power
        a = numpy.power(start, power)
        b = numpy.power(end, power) - a
        c = 1./power
        
        return numpy.power(a + x * b, c)
