#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. properties import *


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
        self._left = x
        self._top = y
        self._right = x + width
        self._bottom = y + height
        self._width = width
        self._height = height
        
        self._reversed = False
        
        # check values
        if self._left > self._right:
            self._left, self._right = self._right, self._left
            self._width *= -1
            self._reversed = True
        
        if self._top > self._bottom:
            self._top, self._bottom = self._bottom, self._top
            self._height *= -1
            self._reversed = True
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "%f, %f, %f, %f" % (self._left, self._top, self._width, self._height)
    
    
    @property
    def x(self):
        """Gets x-coordinate of the left corner."""
        
        return self._left
    
    
    @property
    def y(self):
        """Gets y-coordinate of the top corner."""
        
        return self._top
    
    
    @property
    def width(self):
        """Gets full width."""
        
        return self._width
    
    
    @property
    def height(self):
        """Gets full height."""
        
        return self._height
    
    
    @property
    def left(self):
        """Gets x-coordinate of the left."""
        
        return self._left
    
    
    @property
    def right(self):
        """Gets x-coordinate of the right."""
        
        return self._right
    
    
    @property
    def top(self):
        """Gets y-coordinate of the top."""
        
        return self._top
    
    
    @property
    def bottom(self):
        """Gets y-coordinate of the bottom."""
        
        return self._bottom
    
    
    @property
    def center(self):
        """Gets coordinates of the center."""
        
        return (
            0.5 * (self._left + self._right),
            0.5 * (self._top + self._bottom))
    
    
    @property
    def x1(self):
        """Gets x-coordinate of the top left corner."""
        
        return self._left
    
    
    @property
    def y1(self):
        """Gets y-coordinate of the top left corner."""
        
        return self._top
    
    
    @property
    def x2(self):
        """Gets x-coordinate of the top right corner."""
        
        return self._right
    
    
    @property
    def y2(self):
        """Gets y-coordinate of the bottom right corner."""
        
        return self._bottom
    
    
    @property
    def cx(self):
        """Gets x-coordinate of the center."""
        
        return 0.5 * (self._left + self._right)
    
    
    @property
    def cy(self):
        """Gets y-coordinate of the center."""
        
        return 0.5 * (self._top + self._bottom)
    
    
    @property
    def tl(self):
        """Gets coordinates of the top-left corner."""
        
        return self._left, self._top
    
    
    @property
    def tr(self):
        """Gets coordinates of the top-right corner."""
        
        return self._right, self._top
    
    
    @property
    def bl(self):
        """Gets coordinates of the bottom-left corner."""
        
        return self._left, self._bottom
    
    
    @property
    def br(self):
        """Gets coordinates of the bottom-right corner."""
        
        return self._right, self._bottom
    
    
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
        
        return self._left, self._top, self._width, self._height
    
    
    @property
    def points(self):
        """Gets rectangle as p1, p2, p3, p3 points starting from top left."""
        
        p1 = (self._left, self._top)
        p2 = (self._right, self._top)
        p3 = (self._right, self._bottom)
        p4 = (self._left, self._bottom)
        
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
        
        frame = Frame(self._left, self._top, self._width, self._height)
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
            self._left += x
            self._right += x
        
        if y:
            self._top += y
            self._bottom += y
    
    
    def shrink(self, top=0, right=0, bottom=0, left=0):
        """
        Shrinks current frame on each specified side.
        
        Args:
            top: int, float or None
                Top padding.
            
            right: int, float or None
                Right padding.
            
            bottom: int, float or None
                Bottom padding.
            
            left: int, float or None
                Left padding.
        """
        
        self._left += left
        self._right -= right
        self._top += top
        self._bottom -= bottom
        
        self._width = self._right - self._left
        self._height = self._bottom - self._top
    
    
    def expand(self, top=0, right=0, bottom=0, left=0):
        """
        Expands current frame on each specified side.
        
        Args:
            top: int, float or None
                Top padding.
            
            right: int, float or None
                Right padding.
            
            bottom: int, float or None
                Bottom padding.
            
            left: int, float or None
                Left padding.
        """
        
        self._left -= left
        self._right += right
        self._top -= top
        self._bottom += bottom
        
        self._width = self._right - self._left
        self._height = self._bottom - self._top
    
    
    def extend(self, x=None, y=None, width=0, height=0):
        """
        Extends current frame to include given coordinate, single point or 
        additional frame.
        
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
            
            left = min(self._left, self._right, x, x+width)
            right = max(self._left, self._right, x, x+width)
            
            self._left = left
            self._right = right
            self._width = right - left
        
        if y is not None:
            
            top = min(self._top, self._bottom, y, y+height)
            bottom = max(self._top, self._bottom, y, y+height)
            
            self._top = top
            self._bottom = bottom
            self._height = bottom - top
    
    
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
        left = min(self._left, other._left)
        right = max(self._right, other._right)
        width = right - left
        
        # get y and height
        top = min(self._top, other._top)
        bottom = max(self._bottom, other._bottom)
        height = bottom - top
        
        return Frame(left, top, width, height)
    
    
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
        left = max(self._left, other._left)
        right = min(self._right, other._right)
        width = right - left
        
        if width <= 0:
            return None
        
        # get y and height
        top = max(self._top, other._top)
        bottom = min(self._bottom, other._bottom)
        height = bottom - top
        
        if height <= 0:
            return None
        
        return Frame(left, top, width, height)
    
    
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
        
        return self._left <= x <= self._right and self._top <= y <= self._bottom
    
    
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
        
        if not ((self._left <= other._left <= self._right)
            or (self._left <= other._right <= self._right)
            or (other._left <= self._left and other._right >= self._right)):
            return False
        
        if not ((self._top <= other._top <= self._bottom)
            or (self._top <= other._bottom <= self._bottom)
            or (other._top <= self._top and other._bottom >= self._bottom)):
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
        super().__init__(**kwargs)
    
    
    def parse(self, value):
        """Validates and converts given value."""
        
        # check type
        if isinstance(value, Frame):
            return value
        
        # parse main
        value = super().parse(value)
        
        # allow UNDEF and None
        if value is UNDEF or value is None:
            return value
        
        # check func
        if callable(value):
            return value
        
        # convert to frame
        return Frame(*value)
