#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ..properties import *


class Frame(object):
    """
    Represents a rectangular frame defined by its top-left coordinates, width
    and height.
    """
    
    
    def __init__(self, x, y, width=0, height=0):
        """
        Initializes a new instance of Frame.
        
        Args:
            x: int or float
                X-coordinate of the top left corner.
            
            y: int or float
                Y-coordinate of the top left corner.
            
            width: int or float
                Full width.
            
            height: int or float
                Full height.
        """
        
        # set values
        self._left_x = x
        self._top_y = y
        self._right_x = x + width
        self._bottom_y = y + height
        self._width = width
        self._height = height
        self._reversed = False
        
        # check values
        if self._left_x > self._right_x:
            self._left_x, self._right_x = self._right_x, self._left_x
            self._width *= -1
            self._reversed = True
        
        if self._top_y > self._bottom_y:
            self._top_y, self._bottom_y = self._bottom_y, self._top_y
            self._height *= -1
            self._reversed = True
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "%f, %f, %f, %f" % (self._left_x, self._top_y, self._width, self._height)
    
    
    @property
    def x(self):
        """Gets x-coordinate of the left corner."""
        
        return self._left_x
    
    
    @property
    def y(self):
        """Gets y-coordinate of the top corner."""
        
        return self._top_y
    
    
    @property
    def width(self):
        """Gets full width."""
        
        return self._width
    
    
    @property
    def height(self):
        """Gets full height."""
        
        return self._height
    
    
    @property
    def center(self):
        """Gets coordinates of the center."""
        
        return (
            0.5 * (self._left_x + self._right_x),
            0.5 * (self._top_y + self._bottom_y))
    
    
    @property
    def x1(self):
        """Gets x-coordinate of the top left corner."""
        
        return self._left_x
    
    
    @property
    def y1(self):
        """Gets y-coordinate of the top left corner."""
        
        return self._top_y
    
    
    @property
    def x2(self):
        """Gets x-coordinate of the top right corner."""
        
        return self._right_x
    
    
    @property
    def y2(self):
        """Gets y-coordinate of the bottom right corner."""
        
        return self._bottom_y
    
    
    @property
    def cx(self):
        """Gets x-coordinate of the center."""
        
        return 0.5 * (self._left_x + self._right_x)
    
    
    @property
    def cy(self):
        """Gets y-coordinate of the center."""
        
        return 0.5 * (self._top_y + self._bottom_y)
    
    
    @property
    def tl(self):
        """Gets coordinates of the top-left corner."""
        
        return self._left_x, self._top_y
    
    
    @property
    def tr(self):
        """Gets coordinates of the top-right corner."""
        
        return self._right_x, self._top_y
    
    
    @property
    def bl(self):
        """Gets coordinates of the bottom-left corner."""
        
        return self._left_x, self._bottom_y
    
    
    @property
    def br(self):
        """Gets coordinates of the bottom-right corner."""
        
        return self._right_x, self._bottom_y
    
    
    @property
    def c(self):
        """Gets coordinates of the center."""
        
        return self.center
    
    
    @property
    def w(self):
        """Gets full width."""
        
        return self._width
    
    
    @property
    def h(self):
        """Gets full height."""
        
        return self._height
    
    
    @property
    def wh(self):
        """Gets width and height."""
        
        return self._width, self._height
    
    
    @property
    def rect(self):
        """Gets rectangle as x, y, width, height."""
        
        return self._left_x, self._top_y, self._width, self._height
    
    
    @property
    def points(self):
        """Gets rectangle as p1, p2, p3, p3 points starting from top left."""
        
        p1 = (self._left_x, self._top_y)
        p2 = (self._right_x, self._top_y)
        p3 = (self._right_x, self._bottom_y)
        p4 = (self._left_x, self._bottom_y)
        
        return p1, p2, p3, p4
    
    
    @property
    def reversed(self):
        """Returns True if the frame had originally negative width or height."""
        
        return self._reversed
    
    
    def clone(self):
        """
        Creates exact clone of current frame.
        
        Returns:
            pero.Frame
                Cloned frame.
        """
        
        frame = Frame(self._left_x, self._top_y, self._width, self._height)
        frame._reversed = self._reversed
        
        return frame
    
    
    def offset(self, x=0, y=0):
        """
        Shifts current frame by specified value in x and y directions.
        
        Args:
            x: int, float or None
                X-coordinate offset.
        
            y: int, float or None
                Y-coordinate offset.
        """
        
        if x:
            self._left_x += x
            self._right_x += x
        
        if y:
            self._top_y += y
            self._bottom_y += y
    
    
    def extend(self, x=None, y=None, width=0, height=0):
        """
        Extends current frame to include given coordinate, single point or 
        a whole frame.
        
        Args:
            x: int, float, pero.Frame or None
                X-coordinate or frame to include.
            
            y: int, float or None
                Y-coordinate to include.
            
            width: int or float
                Width of the frame to include.
            
            height: int or float
                Height of the frame to include.
        """
        
        if isinstance(x, Frame):
            x, y, width, height = x.rect
        
        if x is not None:
            
            left_x = min(self._left_x, self._right_x, x, x+width)
            right_x = max(self._left_x, self._right_x, x, x+width)
            
            self._left_x = left_x
            self._right_x = right_x
            self._width = right_x - left_x
        
        if y is not None:
            
            top_y = min(self._top_y, self._bottom_y, y, y+height)
            bottom_y = max(self._top_y, self._bottom_y, y, y+height)
            
            self._top_y = top_y
            self._bottom_y = bottom_y
            self._height = bottom_y - top_y
    
    
    def union(self, other):
        """
        Creates a new frame containing union area of current frame
        and given frame.
        
        Args:
            other: pero.Frame
                Frame to union with.
        
        Returns:
            pero.Frame or None
                Union frame.
        """
        
        # get x and width
        left_x = min(self._left_x, other._left_x)
        right_x = max(self._right_x, other._right_x)
        width = right_x - left_x
        
        # get y and height
        top_y = min(self._top_y, other._top_y)
        bottom_y = max(self._bottom_y, other._bottom_y)
        height = bottom_y - top_y
        
        return Frame(left_x, top_y, width, height)
    
    
    def intersection(self, other):
        """
        Creates a new frame containing intersection area between current frame
        and given frame or None if no such area.
        
        Args:
            other: pero.Frame
                Frame to intersect with.
        
        Returns:
            pero.Frame or None
                Intersection frame or None of no overlap.
        """
        
        # get x and width
        left_x = max(self._left_x, other._left_x)
        right_x = min(self._right_x, other._right_x)
        width = right_x - left_x
        
        if width <= 0:
            return None
        
        # get y and height
        top_y = max(self._top_y, other._top_y)
        bottom_y = min(self._bottom_y, other._bottom_y)
        height = bottom_y - top_y
        
        if height <= 0:
            return None
        
        return Frame(left_x, top_y, width, height)
    
    
    def contains(self, x, y):
        """
        Checks if given point is inside current frame.
        
        Args:
            x: int, float
                X-coordinate to check.
            
            y: int, float
                Y-coordinate to check.
        
        Returns:
            bool
                Returns True if given point is inside, False otherwise.
        """
        
        return self._left_x <= x <= self._right_x and self._top_y <= y <= self._bottom_y
    
    
    def overlaps(self, other):
        """
        Checks if there is any overlap between current frame and given frame.
        
        Args:
            other: pero.Frame
                Frame to check.
        
        Returns:
            bool
                Returns True if any overlap exists, False otherwise.
        """
        
        if not ((self._left_x <= other._left_x <= self._right_x)
            or (self._left_x <= other._right_x <= self._right_x)
            or (other._left_x <= self._left_x and other._right_x >= self._right_x)):
            return False
        
        if not ((self._top_y <= other._top_y <= self._bottom_y)
            or (self._top_y <= other._bottom_y <= self._bottom_y)
            or (other._top_y <= self._top_y and other._bottom_y >= self._bottom_y)):
            return False
        
        return True


class FrameProperty(Property):
    """
    Defines a frame property. The value must be provided as a pero.Frame or
    as a tuple or list of four values for left x, top y, width and height.
    """
    
    
    def __init__(self, default=UNDEF, **kwargs):
        """Initializes a new instance of MarkerProperty."""
        
        kwargs['default'] = default
        kwargs['types'] = (Frame, tuple, list)
        super(FrameProperty, self).__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # check type
        if isinstance(value, Frame):
            return value
        
        # parse main
        value = super(FrameProperty, self).parse(value)
        
        # allow UNDEF and None
        if value is UNDEF or value is None:
            return value
        
        # check func
        if callable(value):
            return value
        
        # convert to frame
        return Frame(*value)
