#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from . import utils
from .frame import Frame


class Arch(object):
    """Represents a simple arch."""
    
    
    def __init__(self, x, y, radius, start_angle, end_angle, clockwise):
        """
        Initializes new instance of arch by its center coordinates, radius,
        start and end angle.
        
        Args:
            x: int or float
                X-coordinate of the center.
            
            y: int or float
                Y-coordinate of the center.
            
            radius: int or float
                Radius of the arch.
            
            start_angle: float
                Start angle in radians.
            
            end_angle: float
                End angle in radians.
            
            clockwise: bool
                Specifies the direction of drawing. If set to True, the arch
                will be drawn in the clockwise direction.
        """
        
        self._x = float(x)
        self._y = float(y)
        self._radius = float(radius)
        self._start_angle = utils.normal_angle(start_angle)
        self._end_angle = utils.normal_angle(end_angle)
        self._clockwise = bool(clockwise)
        
        self._bbox = None
        self._angle = None
        self._start_point = None
        self._end_point = None
        self._mid_point = None
    
    
    @property
    def x(self):
        """
        Gets x-coordinate of the arch center.
        
        Returns:
            float
                Center x-coordinates.
        """
        
        return self._x
    
    
    @property
    def y(self):
        """
        Gets y-coordinate of the arch center.
        
        Returns:
            float
                Center y-coordinates.
        """
        
        return self._y
    
    
    @property
    def radius(self):
        """
        Gets the arch radius.
        
        Returns:
            float
                Radius.
        """
        
        return self._radius
    
    
    @property
    def start_angle(self):
        """
        Gets the start angle in radians.
        
        Returns:
            float
                Start angle in radians.
        """
        
        return self._start_angle
    
    
    @property
    def end_angle(self):
        """
        Gets the end angle in radians.
        
        Returns:
            float
                Start end in radians.
        """
        
        return self._end_angle
    
    
    @property
    def clockwise(self):
        """
        Gets the arch direction indicator.
        
        Returns:
            float
                True if clockwise, False otherwise.
        """
        
        return self._clockwise
    
    
    def bbox(self):
        """
        Calculates arch bounding box.
        
        Returns:
            pero.Frame or None
                Arch bounding box.
        """
        
        if self._bbox is None:
            
            # get end points
            p1 = self.start_point()
            p2 = self.end_point()
            
            # init frame
            self._bbox = Frame(p1[0], p1[1])
            self._bbox.extend(p2[0], p2[1])
            
            # add extremes if existing
            if self.contains_angle(0):
                self._bbox.extend(self._x + self._radius, self._y)
            
            if self.contains_angle(0.5*numpy.pi):
                self._bbox.extend(self._x, self._y + self._radius)
            
            if self.contains_angle(numpy.pi):
                self._bbox.extend(self._x - self._radius, self._y)
            
            if self.contains_angle(1.5*numpy.pi):
                self._bbox.extend(self._x, self._y - self._radius)
        
        return self._bbox
    
    
    def length(self):
        """Returns actual length of the arch."""
        
        return self._radius * self.angle()
    
    
    def angle(self):
        """
        Gets the angle between start and end.
        
        Returns:
            float
                Arch angle in radians.
        """
        
        if self._angle is None:
            self._angle = utils.angle_difference(self._start_angle, self._end_angle, self._clockwise)
        
        return self._angle
    
    
    def start_point(self):
        """
        Gets the starting point of the arch.
        
        Returns:
            (float, float)
                Arch start coordinates.
        """
        
        if self._start_point is None:
            self._start_point = self.angle_as_point(self._start_angle)
        
        return self._start_point
    
    
    def end_point(self):
        """
        Gets the end point of the arch.
        
        Returns:
            (float, float)
                Arch end coordinates.
        """
        
        if self._end_point is None:
            self._end_point = self.angle_as_point(self._end_angle)
        
        return self._end_point
    
    
    def mid_point(self):
        """
        Gets the middle angle point of the arch.
        
        Returns:
            (float, float)
                Arch middle angle coordinates.
        """
        
        if self._mid_point is None:
            angle = abs(self.angle() / 2)
            angle += self._start_angle if self._clockwise else self._end_angle
            self._mid_point = self.angle_as_point(angle)
        
        return self._mid_point
    
    
    def segment_area(self):
        """
        Calculates area of the arch segment, which is the area of the arch
        without the triangle, which goes to the center.
        
        Returns:
            float
                Sector area.
        """
        
        theta = abs(self.angle())
        return self._radius * self._radius / 2 * (theta - numpy.sin(theta))
    
    
    def sector_area(self):
        """
        Calculates area of the arch sector, which is the area of the arch plus
        the triangle, which goes to the center.
        
        Returns:
            float
                Sector area.
        """
        
        return self._radius * self._radius / 2 * abs(self.angle())
    
    
    def angle_as_point(self, angle):
        """
        Calculates coordinates of the point with given angle using current arch
        center and radius.
        
        Args:
            angle: float
                Angle in radians.
        
        Returns:
            (float, float)
                Coordinates of the point.
        """
        
        x = self._x + self._radius * numpy.cos(angle)
        y = self._y + self._radius * numpy.sin(angle)
        
        return x, y
    
    
    def point_as_angle(self, x, y):
        """
        Calculates angle between given point.
        
        Args:
            x: float
                X-coordinate of the point.
            
            y: float
                Y-coordinate of the point.
        
        Returns:
            float
                Angle in radians.
        """
        
        angle = utils.inclination((self._x, self._y), (x, y))
        return utils.normal_angle(angle)
    
    
    def contains_point(self, x, y):
        """Returns True if given point lays on the arch."""
        
        angle = self.point_as_angle(x, y)
        return self.contains_angle(angle)
    
    
    def contains_angle(self, angle):
        """Returns True if given angle lays between start and end angle of the arch."""
        
        angle = utils.normal_angle(angle)
        diff = utils.angle_difference(self._start_angle, angle, self._clockwise)
        
        return abs(diff) <= abs(self.angle())
    
    
    def intersect_circle(self, x, y, radius):
        """
        Calculates all intersection points between current arch and given
        circle.
        
        Args:
            x: float
                X-coordinate of the circle center.
            
            y: float
                Y-coordinate of the circle center.
            
            radius: float
                Radius of the circle.
        
        Returns:
            ((float, float),)
                Coordinates of all intersection points.
        """
        
        # calc circles intersection
        points = utils.intersect_circles((self._x, self._y), self._radius, (x, y), radius)
        if points is None:
            return ()
        
        # get points inside current arch
        points = [p for p in points if self.contains_point(p[0], p[1])]
        
        # sort by angle
        points.sort(key=lambda p: self.point_as_angle(p[0], p[1]))
        
        return points
    
    
    def intersect_arch(self, arch):
        """
        Calculates all intersection points between current arch and given arch.
        
        Args:
            arch: pero.Arch
                Arch to intersect.
        
        Returns:
            ((float, float),)
                Coordinates of all intersection points.
        """
        
        # calc circle intersection
        points = self.intersect_circle(arch.x, arch.y, arch.radius)
        
        # get points inside given arch
        points = [p for p in points if arch.contains_point(p[0], p[1])]
        
        return points
    
    
    @staticmethod
    def from_points(center, start_point, end_point, radius, clockwise):
        """
        Initializes new instance of arch by its center coordinates, start and
        end point coordinates, radius and direction.
        
        Args:
            center: (float, float)
                Coordinates of the center.
            
            start_point: (float, float)
                Coordinates of the starting point.
            
            end_point: (float, float)
                Coordinates of the end point.
            
            radius: int or float
                Radius of the arch.
            
            clockwise: bool
                Specifies the direction of drawing. If set to True, the arch
                will be drawn in the clockwise direction.
        """
        
        start_angle = utils.inclination(center, start_point)
        end_angle = utils.inclination(center, end_point)
        
        return Arch(center[0], center[1], radius, start_angle, end_angle, clockwise)
