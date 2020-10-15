#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from ..drawing import Arch, Path
from ..drawing import utils


class Region(object):
    """Defines a base class for all types of Venn diagram regions."""
    
    
    def points(self):
        """
        Gets all the intersection points.
        
        Returns:
            ((float, float),)
                All intersection points.
        """
        
        return ()
    
    
    def path(self):
        """
        Gets the path of the region.
        
        This method must be implemented for each derived class.
        
        Returns:
            pero.Path
                Region path.
        """
        
        return None
    
    
    def overlay(self, center, radius):
        """
        Calculates remaining and overlapping region with given circle.
        
        This method must be implemented for each derived class.
        
        Args:
            center: (float, float)
                Center coordinates of the overlapping circle.
            
            radius: float
                Radius of the overlapping circle.
        """
        
        raise NotImplementedError()


class EmptyRegion(Region):
    """Defines an empty region."""
    
    
    def overlay(self, center, radius):
        """
        Calculates remaining and overlapping region with given circle.
        
        Args:
            center: (float, float)
                Center coordinates of the overlapping circle.
            
            radius: float
                Radius of the overlapping circle.
        """
        
        return self, self


class CircleRegion(Region):
    """Defines a complete circle region."""
    
    
    def __init__(self, center, radius):
        """
        Initializes a new instance of the circle region.
        
        Args:
            center: (float, float)
                Center coordinates of the circle.
            
            radius: float
                Radius of the circle.
        """
        
        self._center = center
        self._radius = radius
    
    
    def path(self):
        """
        Gets the path of the region.
        
        Returns:
            pero.Path
                Region path.
        """
        
        path = Path()
        path.circle(self._center[0], self._center[1], self._radius)
        
        return path
    
    
    def overlay(self, center, radius):
        """
        Calculates remaining and overlapping region with given circle.
        
        Args:
            center: (float, float)
                Center coordinates of the overlapping circle.
            
            radius: float
                Radius of the overlapping circle.
        """
        
        # calc distance
        dist = utils.distance(self._center, center)
        
        # non intersecting
        if dist >= self._radius + radius:
            return self, EmptyRegion()
        
        # same circles
        if dist == 0 and self._radius == radius:
            return EmptyRegion(), self
        
        # full overlap
        if dist <= abs(self._radius - radius):
            if self._radius > radius:
                return RingRegion(self._center, self._radius, center, radius), CircleRegion(center, radius)
            return EmptyRegion(), CircleRegion(self._center, self._radius)
        
        # calc intersections
        points = utils.intersect_circles(self._center, self._radius, center, radius)
        
        # make arcs
        residue = (
            Arch.from_points(center, points[0], points[1], radius, False),
            Arch.from_points(self._center, points[1], points[0], self._radius, True))
        
        overlap = (
            Arch.from_points(self._center, points[0], points[1], self._radius, True),
            Arch.from_points(center, points[1], points[0], radius, True))
        
        # make regions
        return ArcsRegion(residue), ArcsRegion(overlap)


class RingRegion(Region):
    """Defines a circle region with circular hole inside."""
    
    
    def __init__(self, out_center, out_radius, in_center, in_radius):
        """
        Initializes a new instance of the ring region.
        
        Args:
            out_center: (float, float)
                Center coordinates of the outer circle.
            
            out_radius: float
                Radius of the outer circle.
            
            in_center: (float, float)
                Center coordinates of the inner circle.
            
            in_radius: float
                Radius of the inner circle.
        """
        
        self._out_center = out_center
        self._out_radius = out_radius
        self._in_center = in_center
        self._in_radius = in_radius
    
    
    def path(self):
        """
        Gets the path of the region.
        
        Returns:
            pero.Path
                Region path.
        """
        
        path = Path()
        path.circle(self._out_center[0], self._out_center[1], self._out_radius)
        path.circle(self._in_center[0], self._in_center[1], self._in_radius)
        
        return path
    
    
    def overlay(self, center, radius):
        """
        Calculates remaining and overlapping region with given circle.
        
        Args:
            center: (float, float)
                Center coordinates of the overlapping circle.
            
            radius: float
                Radius of the overlapping circle.
        """
        
        # calc distance
        dist = utils.distance(self._out_center, center)
        
        # non intersecting
        if dist >= self._out_radius + radius:
            return self, EmptyRegion()
        
        # calc intersections
        out_points = utils.intersect_circles(self._out_center, self._out_radius, center, radius)
        int_points = utils.intersect_circles(self._in_center, self._in_radius, center, radius)
        
        # TODO
        
        return EmptyRegion(), EmptyRegion()


class ArcsRegion(Region):
    """Defines a region consisting of multiple arcs."""
    
    
    def __init__(self, arcs):
        """
        Initializes a new instance of the ring region.
        
        Args:
            arcs: (pero.Arch,)
                Sequence of arcs.
        """
        
        self._arcs = tuple(arcs)
    
    
    def points(self):
        """
        Gets all the intersection points.
        
        Returns:
            ((float, float),)
                All intersection points.
        """
        
        return tuple(a.start for a in self._arcs if a is not None)
    
    
    def path(self):
        """
        Gets the path of the region.
        
        Returns:
            pero.Path
                Region path.
        """
        
        # init path
        path = Path()
        
        # add arcs
        init = True
        for arc in self._arcs:
            
            # break current sub-path
            if arc is None:
                path.close()
                init = True
                continue
            
            # init new subpath
            if init:
                path.move_to(*arc.start)
                init = False
            
            # add arc
            path.arc_around(arc.center[0], arc.center[1], arc.end_angle, arc.clockwise)
        
        # close path
        path.close()
        
        return path
    
    
    def overlay(self, center, radius):
        """
        Calculates remaining and overlapping region with given circle.
        
        Args:
            center: (float, float)
                Center coordinates of the overlapping circle.
            
            radius: float
                Radius of the overlapping circle.
        """
        
        # check number of arcs
        if len(self._arcs) > 2:
            raise ValueError("More than two arcs are not supported for overlay.")
        
        # calc intersections
        points_1 = self._arcs[0].intersect_circle(center[0], center[1], radius, inside=True)
        points_2 = self._arcs[1].intersect_circle(center[0], center[1], radius, inside=True)
        
        # full overlap or outside
        if len(points_1) == 0 and len(points_2) == 0:
            return self._no_intersections(center, radius)
        
        # corner overlap
        if len(points_1) == 1 and len(points_2) == 1:
            return self._single_intersection_for_each(center, radius, points_1, points_2)
        
        # cut through
        elif len(points_1) == 2 and len(points_2) == 2:
            return self._two_intersections_for_each(center, radius, points_1, points_2)
        
        # one cut twice
        elif len(points_1) == 2 or len(points_2) == 2:
            return self._two_intersections_for_one(center, radius, points_1, points_2)
        
        raise ValueError("Unknown overlap scenario!")
    
    
    def _no_intersections(self, center, radius):
        """Handles the case where there is either complete or no overlap at all."""
        
        # circle overlaps all arcs
        if utils.is_inside_circle(self._arcs[0].start, center, radius):
            return EmptyRegion(), self
        
        # get arcs
        arc_1, arc_2 = self._arcs
        
        # check if circle is inside the arcs
        inside_1 = utils.distance(arc_1.center, center) <= abs(arc_1.radius - radius)
        inside_2 = utils.distance(arc_2.center, center) <= abs(arc_2.radius - radius)
        
        # no overlap possible if not inside both arcs
        if not (inside_1 or inside_2):
            return self, EmptyRegion()
        
        # if sum of insides and directions is odd the circle is fully outside
        if sum((inside_1, inside_2, arc_1.clockwise, arc_2.clockwise)) % 2:
            return self, EmptyRegion()
        
        # assemble remaining part
        remain = list(self._arcs[:])
        remain.append(None)
        remain.append(Arch(center[0], center[1], radius, 0, 2*numpy.pi, True))
        
        # make regions
        return ArcsRegion(remain), CircleRegion(center, radius)
    
    
    def _single_intersection_for_each(self, center, radius, points_1, points_2):
        """Handles the case where each of the two arcs has single intersection."""
        
        # init parts
        remains = []
        overlap = []
        
        # get arcs
        arc_1, arc_2 = self._arcs
        
        # get intersections
        point_1 = points_1[0]
        point_2 = points_2[0]
        
        # split arcs
        seg_1 = Arch.from_points(arc_1.center, arc_1.start, point_1, arc_1.radius, arc_1.clockwise)
        seg_2 = Arch.from_points(arc_1.center, point_1, arc_1.end, arc_1.radius, arc_1.clockwise)
        
        seg_3 = Arch.from_points(arc_2.center, arc_2.start, point_2, arc_2.radius, arc_2.clockwise)
        seg_4 = Arch.from_points(arc_2.center, point_2, arc_2.end, arc_2.radius, arc_2.clockwise)
        
        # cut is at the beginning
        if utils.is_inside_circle(arc_1.start, center, radius):
            
            # assemble remaining part
            remains.append(seg_2)
            remains.append(seg_3)
            remains.append(Arch.from_points(center, point_2, point_1, radius, False))
            
            # assemble overlapping part
            overlap.append(seg_1)
            overlap.append(Arch.from_points(center, point_1, point_2, radius, True))
            overlap.append(seg_4)
        
        # cut is at the end
        else:
            
            # assemble remaining part
            remains.append(seg_1)
            remains.append(Arch.from_points(center, point_1, point_2, radius, False))
            remains.append(seg_4)
            
            # assemble overlapping part
            overlap.append(seg_2)
            overlap.append(seg_3)
            overlap.append(Arch.from_points(center, point_2, point_1, radius, True))
        
        # make regions
        return ArcsRegion(remains), ArcsRegion(overlap)
    
    
    def _two_intersections_for_each(self, center, radius, points_1, points_2):
        """Handles the case where each of the two arcs has two intersections."""
        
        # init parts
        remain = []
        overlap = []
        
        # get arcs
        arc_1, arc_2 = self._arcs
        
        # split arcs
        seg_1 = Arch.from_points(arc_1.center, arc_1.start, points_1[0], arc_1.radius, arc_1.clockwise)
        seg_2 = Arch.from_points(arc_1.center, points_1[0], points_1[1], arc_1.radius, arc_1.clockwise)
        seg_3 = Arch.from_points(arc_1.center, points_1[1], arc_1.end, arc_1.radius, arc_1.clockwise)
        
        seg_4 = Arch.from_points(arc_2.center, arc_2.start, points_2[0], arc_2.radius, arc_2.clockwise)
        seg_5 = Arch.from_points(arc_2.center, points_2[0], points_2[1], arc_2.radius, arc_2.clockwise)
        seg_6 = Arch.from_points(arc_2.center, points_2[1], arc_2.end, arc_2.radius, arc_2.clockwise)
        
        # assemble remaining part
        remain.append(seg_1)
        remain.append(Arch.from_points(center, points_1[0], points_2[1], radius, False))
        remain.append(seg_6)
        remain.append(None)
        remain.append(seg_3)
        remain.append(seg_4)
        remain.append(Arch.from_points(center, points_2[0], points_1[1], radius, False))
        
        # assemble overlapping part
        overlap.append(seg_2)
        overlap.append(Arch.from_points(center, points_1[1], points_2[0], radius, True))
        overlap.append(seg_5)
        overlap.append(Arch.from_points(center, points_2[1], points_1[0], radius, True))
        
        # make regions
        return ArcsRegion(remain), ArcsRegion(overlap)
    
    
    def _two_intersections_for_one(self, center, radius, points_1, points_2):
        """Handles the case where one arc has two intersections, the other none."""
        
        # init parts
        remain = []
        overlap = []
        
        # get arcs
        if points_1:
            arc_1, arc_2 = self._arcs
            point_1, point_2 = points_1
        else:
            arc_2, arc_1 = self._arcs
            point_1, point_2 = points_2
        
        # split arc
        seg_1 = Arch.from_points(arc_1.center, arc_1.start, point_1, arc_1.radius, arc_1.clockwise)
        seg_2 = Arch.from_points(arc_1.center, point_1, point_2, arc_1.radius, arc_1.clockwise)
        seg_3 = Arch.from_points(arc_1.center, point_2, arc_1.end, arc_1.radius, arc_1.clockwise)
        
        # cut is on edges
        if utils.is_inside_circle(arc_1.start, center, radius):
            
            # assemble remaining part
            remain.append(seg_2)
            remain.append(Arch.from_points(center, point_2, point_1, radius, False))
            
            # assemble overlapping part
            overlap.append(seg_1)
            overlap.append(Arch.from_points(center, point_1, point_2, radius, True))
            overlap.append(seg_3)
            overlap.append(arc_2)
        
        # cut is in middle
        else:
            
            # assemble remaining part
            remain.append(seg_1)
            remain.append(Arch.from_points(center, point_1, point_2, radius, False))
            remain.append(seg_3)
            remain.append(arc_2)
            
            # assemble overlapping part
            overlap.append(seg_2)
            overlap.append(Arch.from_points(center, point_2, point_1, radius, True))
        
        # make regions
        return ArcsRegion(remain), ArcsRegion(overlap)
