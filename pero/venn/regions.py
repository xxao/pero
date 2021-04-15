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
        
        return Path()
    
    
    def label(self):
        """
        Gets the label position.
        
        Returns:
            (float, float)
                Label coordinates.
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
        
        Returns:
            (pero.venn.Region, pero.venn.Region),)
                Venn regions for remaining and overlapping parts.
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
        
        Returns:
            (pero.venn.Region, pero.venn.Region),)
                Venn regions for remaining and overlapping parts.
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
        
        self._center = tuple(center)
        self._radius = float(radius)
    
    
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
    
    
    def label(self):
        """
        Gets the label position.
        
        Returns:
            (float, float)
                Label coordinates.
        """
        
        return self._center
    
    
    def overlay(self, center, radius):
        """
        Calculates remaining and overlapping region with given circle.
        
        Args:
            center: (float, float)
                Center coordinates of the overlapping circle.
            
            radius: float
                Radius of the overlapping circle.
        
        Returns:
            (pero.venn.Region, pero.venn.Region),)
                Venn regions for remaining and overlapping parts.
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
        remains = (
            Arch.from_points(center, points[0], points[1], radius, False),
            Arch.from_points(self._center, points[1], points[0], self._radius, True))
        
        overlap = (
            Arch.from_points(self._center, points[0], points[1], self._radius, True),
            Arch.from_points(center, points[1], points[0], radius, True))
        
        # make regions
        return ArcsRegion(remains), ArcsRegion(overlap)


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
    
    
    def label(self):
        """
        Gets the label position.
        
        Returns:
            (float, float)
                Label coordinates.
        """
        
        # calc angle of centers
        angle = utils.inclination(self._in_center, self._out_center)
        
        # calc points at circles
        p1 = utils.ray(self._in_center, angle, self._in_radius)
        p2 = utils.ray(self._out_center, angle, self._out_radius)
        
        # calc average point
        return tuple(numpy.mean((p1, p2), 0))
    
    
    def overlay(self, center, radius):
        """
        Calculates remaining and overlapping region with given circle.
        
        Args:
            center: (float, float)
                Center coordinates of the overlapping circle.
            
            radius: float
                Radius of the overlapping circle.
        
        Returns:
            (pero.venn.Region, pero.venn.Region),)
                Venn regions for remaining and overlapping parts.
        """
        
        # calc distance
        dist = utils.distance(self._out_center, center)
        
        # non intersecting
        if dist >= self._out_radius + radius:
            return self, EmptyRegion()
        
        # calc intersections
        points_out = utils.intersect_circles(self._out_center, self._out_radius, center, radius)
        points_in = utils.intersect_circles(self._in_center, self._in_radius, center, radius)
        
        # full overlap or outside
        if len(points_out) == 0 and len(points_in) == 0:
            return self._no_intersections(center, radius)
        
        # both circles are cut through
        if len(points_out) == 2 and len(points_in) == 2:
            return self._two_intersections_for_both(center, radius, points_out, points_in)
        
        # outer circle cut through
        if len(points_out) == 2:
            return self._two_intersections_for_outer(center, radius, points_out)
        
        # inner circle cut through
        if len(points_in) == 2:
            return self._two_intersections_for_inner(center, radius, points_in)
        
        raise ValueError("Unknown overlap scenario!")
    
    
    def _no_intersections(self, center, radius):
        """Handles the case where the circle is not outside but has no intersections."""
        
        # get inside flags
        inside_out = utils.is_circle_in_circle(center, radius, self._out_center, self._out_radius)
        inside_in = utils.is_circle_in_circle(center, radius, self._in_center, self._in_radius)
        
        # circle overlaps whole ring
        if not inside_out:
            return EmptyRegion(), self
        
        # circle is inside the hole
        if inside_in:
            return self, EmptyRegion()
        
        # circle is inside the ring
        remains = (
            Arch(self._out_center[0], self._out_center[1], self._out_radius, 0, 2*numpy.pi, True),
            None,
            Arch(self._in_center[0], self._in_center[1], self._in_radius, 0, 2*numpy.pi, True),
            None,
            Arch(center[0], center[1], radius, 0, 2 * numpy.pi, True))
        
        return ArcsRegion(remains), CircleRegion(center, radius)
    
    
    def _two_intersections_for_both(self, center, radius, points_out, points_in):
        """Handles the case where each of the two circles has two intersections."""
        
        # assemble remaining part
        remains = (
            Arch.from_points(center, points_out[0], points_in[0], radius, False),
            Arch.from_points(self._in_center, points_in[0], points_in[1], self._in_radius, False),
            Arch.from_points(center, points_in[1], points_out[1], radius, False),
            Arch.from_points(self._out_center, points_out[1], points_out[0], self._out_radius, True))
        
        # assemble overlapping part
        overlap = (
            Arch.from_points(self._out_center, points_out[0], points_out[1], self._out_radius, True),
            Arch.from_points(center, points_out[1], points_in[1], radius, True),
            Arch.from_points(self._in_center, points_in[1], points_in[0], self._in_radius, False),
            Arch.from_points(center, points_in[0], points_out[0], radius, True))
        
        # make regions
        return ArcsRegion(remains), ArcsRegion(overlap)
    
    
    def _two_intersections_for_outer(self, center, radius, points):
        """Handles the case where outer circles has two intersections."""
        
        # assemble remaining part
        remains = (
            Arch.from_points(center, points[0], points[1], radius, False),
            Arch.from_points(self._out_center, points[1], points[0], self._out_radius, True),
            None,
            Arch(self._in_center[0], self._in_center[1], self._in_radius, 0, 2*numpy.pi, True))
        
        # assemble overlapping part
        overlap = (
            Arch.from_points(self._out_center, points[0], points[1], self._out_radius, True),
            Arch.from_points(center, points[1], points[0], radius, True))
        
        # make regions
        return ArcsRegion(remains), ArcsRegion(overlap)
    
    
    def _two_intersections_for_inner(self, center, radius, points):
        """Handles the case where inner circles has two intersections."""
        
        # assemble remaining part
        remains = (
            Arch(self._out_center[0], self._out_center[1], self._out_radius, 0, 2*numpy.pi, True),
            None,
            Arch.from_points(center, points[0], points[1], radius, True),
            Arch.from_points(self._in_center, points[1], points[0], self._in_radius, True))
        
        # assemble overlapping part
        overlap = (
            Arch.from_points(center, points[0], points[1], radius, True),
            Arch.from_points(self._in_center, points[1], points[0], self._in_radius, False))
        
        # make regions
        return ArcsRegion(remains), ArcsRegion(overlap)


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
            
            # add circle
            if arc.angle() % (2*numpy.pi) == 0:
                path.circle(arc.center[0], arc.center[1], arc.radius)
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
    
    
    def label(self):
        """
        Gets the label position.
        
        Returns:
            (float, float)
                Label coordinates.
        """
        
        # get segments
        segments = [[]]
        for arc in self._arcs:
            if arc is None:
                segments.append([])
            else:
                segments[-1].append(arc)
        
        # single segment
        if len(segments) == 1:
            
            # get arcs
            arcs = segments[0]
            if len(arcs) > 3:
                arcs = sorted(arcs, key=lambda a: abs(a.angle()), reverse=True)[:2]
            
            # calc arcs centroid
            points = (a.middle for a in arcs)
            return utils.polygon_centroid(*points)
        
        # multiple non-circle segments
        if all(len(s) > 1 for s in segments):
            
            # get biggest segment
            length = 0
            for segment in segments:
                ln = sum(abs(a.length()) for a in segment)
                if ln > length:
                    arcs = segment
                    length = ln
            
            # calc arcs centroid
            points = (a.middle for a in arcs)
            return utils.polygon_centroid(*points)
        
        # circle inside arcs
        if len(segments) == 2:
            return None
        
        # circles inside circle
        if len(segments) == 3:
            return None
        
        raise NotImplementedError("Unknown label scenario!")
    
    
    def overlay(self, center, radius):
        """
        Calculates remaining and overlapping region with given circle.
        
        Args:
            center: (float, float)
                Center coordinates of the overlapping circle.
            
            radius: float
                Radius of the overlapping circle.
        
        Returns:
            (pero.venn.Region, pero.venn.Region),)
                Venn regions for remaining and overlapping parts.
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
            return self._single_intersection_for_both(center, radius, points_1, points_2)
        
        # cut through
        elif len(points_1) == 2 and len(points_2) == 2:
            return self._two_intersections_for_both(center, radius, points_1, points_2)
        
        # one cut twice
        elif len(points_1) == 2 or len(points_2) == 2:
            return self._two_intersections_for_one(center, radius, points_1, points_2)
        
        raise ValueError("Unknown overlap scenario!")
    
    
    def _no_intersections(self, center, radius):
        """Handles the case where there is either complete or no overlap at all."""
        
        # circle overlaps all arcs
        if utils.is_point_in_circle(self._arcs[0].start, center, radius):
            return EmptyRegion(), self
        
        # get arcs
        arc_1, arc_2 = self._arcs
        
        # check if circle is inside the arcs
        inside_1 = utils.is_circle_in_circle(center, radius, arc_1.center, arc_1.radius)
        inside_2 = utils.is_circle_in_circle(center, radius, arc_2.center, arc_2.radius)
        
        # no overlap possible if outside both arcs
        if not inside_1 and not inside_2:
            return self, EmptyRegion()
        
        # for convex shape it must be inside both to overlap
        if arc_1.clockwise == arc_2.clockwise:
            if not inside_1 or not inside_2:
                return self, EmptyRegion()
        
        # for concave shape it cannot be inside the smaller arc to overlap
        else:
            inside_smaller = inside_1 if arc_1.length() < arc_2.length() else inside_2
            if inside_smaller:
                return self, EmptyRegion()
        
        # assemble remaining part
        remains = (
            self._arcs[0],
            self._arcs[1],
            None,
            Arch(center[0], center[1], radius, 0, 2*numpy.pi, True))
        
        # make regions
        return ArcsRegion(remains), CircleRegion(center, radius)
    
    
    def _single_intersection_for_both(self, center, radius, points_1, points_2):
        """Handles the case where each of the two arcs has single intersection."""
        
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
        
        # check for start cut
        start_cut = utils.is_point_in_circle(arc_1.start, center, radius)
        
        # assemble remaining part
        remains = (
            seg_2,
            seg_3,
            Arch.from_points(center, point_2, point_1, radius, not start_cut))
        
        # assemble overlapping part
        overlap = (
            seg_1,
            Arch.from_points(center, point_1, point_2, radius, start_cut),
            seg_4)
        
        # flip parts if end cut
        if not start_cut:
            remains, overlap = overlap, remains
        
        # make regions
        return ArcsRegion(remains), ArcsRegion(overlap)
    
    
    def _two_intersections_for_both(self, center, radius, points_1, points_2):
        """Handles the case where each of the two arcs has two intersections."""
        
        # get arcs
        arc_1, arc_2 = self._arcs
        
        # split arcs
        seg_1 = Arch.from_points(arc_1.center, arc_1.start, points_1[0], arc_1.radius, arc_1.clockwise)
        seg_2 = Arch.from_points(arc_1.center, points_1[0], points_1[1], arc_1.radius, arc_1.clockwise)
        seg_3 = Arch.from_points(arc_1.center, points_1[1], arc_1.end, arc_1.radius, arc_1.clockwise)
        
        seg_4 = Arch.from_points(arc_2.center, arc_2.start, points_2[0], arc_2.radius, arc_2.clockwise)
        seg_5 = Arch.from_points(arc_2.center, points_2[0], points_2[1], arc_2.radius, arc_2.clockwise)
        seg_6 = Arch.from_points(arc_2.center, points_2[1], arc_2.end, arc_2.radius, arc_2.clockwise)
        
        # check for inner cut
        inside_cut = not utils.is_point_in_circle(arc_1.start, center, radius)
        
        # assemble remaining part
        remains = (
            seg_1,
            Arch.from_points(center, points_1[0], points_2[1], radius, not inside_cut),
            seg_6,
            None,
            seg_3,
            seg_4,
            Arch.from_points(center, points_2[0], points_1[1], radius, not inside_cut))
        
        # assemble overlapping part
        overlap = (
            seg_2,
            Arch.from_points(center, points_1[1], points_2[0], radius, inside_cut),
            seg_5,
            Arch.from_points(center, points_2[1], points_1[0], radius, inside_cut))
        
        # flip parts if corner cut
        if not inside_cut:
            remains, overlap = overlap, remains
        
        # make regions
        return ArcsRegion(remains), ArcsRegion(overlap)
    
    
    def _two_intersections_for_one(self, center, radius, points_1, points_2):
        """Handles the case where one arc has two intersections, the other none."""
        
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
        
        # check for inner cut
        inside_cut = not utils.is_point_in_circle(arc_1.start, center, radius)
        
        # assemble remaining part
        remains = (
            seg_1,
            Arch.from_points(center, point_1, point_2, radius, not inside_cut),
            seg_3,
            arc_2)
        
        # assemble overlapping part
        overlap = (
            seg_2,
            Arch.from_points(center, point_2, point_1, radius, inside_cut))
        
        # flip parts if corner cut
        if not inside_cut:
            remains, overlap = overlap, remains
        
        # make regions
        return ArcsRegion(remains), ArcsRegion(overlap)
