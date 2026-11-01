#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy


class Matrix(object):
    """
    Represents 2D transformation matrix used to apply requested transformations
    to given coordinates, mostly to transform a path.
    
    Most of the methods returns self so that they can be chained.
    """
    
    
    def __init__(self, a=1, b=0, c=0, d=1, tx=0, ty=0):
        """
        Initializes a new instance of Matrix from affine coefficients.
        Default values create an identity matrix. Points are transformed as
        x' = a*x + c*y + tx and y' = b*x + d*y + ty.
        
        Args:
            a: int or float
                X contribution to the transformed x-coordinate.
            
            b: int or float
                X contribution to the transformed y-coordinate.
            
            c: int or float
                Y contribution to the transformed x-coordinate.
            
            d: int or float
                Y contribution to the transformed y-coordinate.
            
            tx: int or float
                Horizontal translation.
            
            ty: int or float
                Vertical translation.
        """
        
        self._matrix = numpy.array((
            [a, c, tx],
            [b, d, ty],
            [0.0, 0.0, 1.0]), dtype=float)
    
    
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
    
    
    def merge(self, matrix):
        """
        Merges given matrix into current one.
        
        Args:
            matrix: pero.Matrix
                Matrix to merge.
        
        Returns:
            pero.Matrix
                Returns self so that the commands can be chained.
        """
        
        self._matrix = numpy.dot(matrix._matrix, self._matrix)
        
        return self
    
    
    def invert(self):
        """
        Inverts current matrix in place. If the matrix is singular, it remains
        unchanged and an exception is raised.
        
        Returns:
            pero.Matrix
                Returns self so that the commands can be chained.
        
        Raises:
            numpy.linalg.LinAlgError
                If the matrix is singular and cannot be inverted.
        """
        
        self._matrix = numpy.linalg.inv(self._matrix)
        
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
        Transforms scalar or broadcast-compatible array coordinates by current
        matrix.
        
        Args:
            x: int, float or array-like
                X-coordinate(s) to be transformed.
            
            y: int, float or array-like
                Y-coordinate(s) to be transfromed.
        
        Returns:
            numpy.ndarray
                Transformed coordinates with shape (2,) for scalar inputs or
                (2, *broadcast_shape) for array inputs. The first axis contains
                the transformed x and y coordinates.
        """
        
        x = numpy.asarray(x)
        y = numpy.asarray(y)
        matrix = self._matrix
        
        tx = matrix[0, 0]*x + matrix[0, 1]*y + matrix[0, 2]
        ty = matrix[1, 0]*x + matrix[1, 1]*y + matrix[1, 2]
        
        return numpy.array((tx, ty))
    
    
    def clone(self):
        """
        Creates a clone of current matrix.
        
        Returns:
            pero.Matrix
                Returns cloned matrix.
        """
        
        matrix = Matrix()
        matrix.merge(self)
        
        return matrix
