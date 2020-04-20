#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy


class Matrix(object):
    """
    Represents 2D transformation matrix used to apply requested transformations
    to given coordinates, mostly to transform a path.
    
    Most of the methods returns self so that they can be chained.
    """
    
    
    def __init__(self):
        """Initializes a new instance of Matrix."""
        
        self._matrix = numpy.identity(3)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return str(self._matrix)
    
    
    def clear(self):
        """
        Clears all applied transformations and resets current matrix to identity
        matrix.
        
        Returns:
            pero.Matrix
                Returns self so that the commands can be chained.
        """
        
        self._matrix = numpy.identity(3)
        
        return self
    
    
    def translate(self, x_shift=None, y_shift=None):
        """
        Applies horizontal and vertical shift to current matrix.
        
        Args:
            x_shift: int or float
                Horizontal shift.
            
            y_shift: int or float
                Vertical shift.
        
        Returns:
            pero.Matrix
                Returns self so that the commands can be chained.
        """
        
        if not x_shift and not y_shift:
            return self
        
        elif y_shift is None:
            y_shift = 0
        
        elif x_shift is None:
            x_shift = 0
        
        trans = numpy.array((
            [1.0, 0.0, x_shift],
            [0.0, 1.0, y_shift],
            [0.0, 0.0, 1.0]))
        
        self._matrix = numpy.dot(trans, self._matrix)
        
        return self
    
    
    def rotate(self, angle, x=0, y=0, clockwise=True):
        """
        Applies rotation around specified origin to current matrix.
        
        Args:
            angle: float
                Angle to be applied in radians.
            
            x: int float
                X-coordinate of the rotation origin.
            
            y: int float
                Y-coordinate of the rotation origin.
            
            clockwise: bool
                Specifies the direction of rotation. If set to True, the rotation
                will be applied in the clockwise direction.
        
        Returns:
            pero.Matrix
                Returns self so that the commands can be chained.
        """
        
        clockwise = 1 if clockwise else -1
        
        a = numpy.cos(angle) * clockwise
        b = numpy.sin(angle) * clockwise
        
        trans = numpy.array((
            [a, -b, 0.0],
            [b, a, 0.0],
            [0.0, 0.0, 1.0]))
        
        if x != 0 or y != 0:
            self.translate(-x, -y)
        
        self._matrix = numpy.dot(trans, self._matrix)
        
        if x != 0 or y != 0:
            self.translate(x, y)
        
        return self
    
    
    def scale(self, x_scale, y_scale, x=0, y=0):
        """
        Applies horizontal and vertical scaling from specified origin to current
        matrix.
        
        Args:
            x_scale: int or float
                Horizontal axis scale.
            
            y_scale: int or float
                Vertical axis scale.
            
            x: int float
                X-coordinate of the scaling origin.
            
            y: int float
                Y-coordinate of the scaling origin.
        
        Returns:
            pero.Matrix
                Returns self so that the commands can be chained.
        """
        
        trans = numpy.array((
            [x_scale, 0.0, 0.0],
            [0.0, y_scale, 0.0],
            [0.0, 0.0, 1.0]))
        
        if x != 0 or y != 0:
            self.translate(-x, -y)
        
        self._matrix = numpy.dot(trans, self._matrix)
        
        if x != 0 or y != 0:
            self.translate(x, y)
        
        return self
    
    
    def skew(self, x_shear, y_shear, x=0, y=0, clockwise=True):
        """
        Applies skewing and shearing around specified origin to current matrix.
        
        Args:
            x_shear: float
                Angle to be applied along horizontal axis in radians.
            
            y_shear: float
                Angle to be applied along vertical axis in radians.
            
            x: int float
                X-coordinate of the rotation origin.
            
            y: int float
                Y-coordinate of the rotation origin.
            
            clockwise: bool
                Specifies the direction of skew. If set to True, the skew
                will be applied in the clockwise direction.
        
        Returns:
            pero.Matrix
                Returns self so that the commands can be chained.
        """
        
        clockwise = 1 if clockwise else -1
        
        a = numpy.tan(x_shear) * clockwise
        b = numpy.tan(y_shear) * clockwise
        
        trans = numpy.array((
            [1.0, a, 0.0],
            [b, 1.0, 0.0],
            [0.0, 0.0, 1.0]))
        
        if x != 0 or y != 0:
            self.translate(-x, -y)
        
        self._matrix = numpy.dot(trans, self._matrix)
        
        if x != 0 or y != 0:
            self.translate(x, y)
        
        return self
    
    
    def ray(self, length, angle):
        """
        Applies shift along the direction of given angle to current matrix.
        
        Args:
            length: float
                Shift along the angle.
            
            angle: float
                Angle of the shift in radians.
        
        Returns:
            pero.Matrix
                Returns self so that the commands can be chained.
        """
        
        self.rotate(-angle)
        self.translate(length)
        self.rotate(angle)
        
        return self
    
    
    def hflip(self, x=0):
        """
        Applies horizontal flipping along specified x-coordinate to current
        matrix.
        
        Args:
            x: int or float
                Flipping x-coordinate.
        
        Returns:
            pero.Matrix
                Returns self so that the commands can be chained.
        """
        
        self.scale(-1, 1, x, 0)
        
        return self
    
    
    def vflip(self, y=0):
        """
        Applies vertical flipping along specified y-coordinate to current
        matrix.
        
        Args:
            y: int or float
                Flipping y-coordinate.
        
        Returns:
            pero.Matrix
                Returns self so that the commands can be chained.
        """
        
        self.scale(1, -1, 0, y)
        
        return self
    
    
    def transform(self, x, y):
        """
        Transforms given point by current matrix.
        
        Args:
            x: int or float
                X-coordinate of the point to be transformed.
            
            y: int or float
                Y-coordinate of the point to be transformed.
        
        Returns:
            (int, int) or (float, float)
                Transformed point.
        """
        
        return numpy.array((x, y, 1)).dot(self._matrix.T)[0:2]
