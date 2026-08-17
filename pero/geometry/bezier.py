#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
import math
import numpy
from . import helpers
from . import intersects
from . frame import Frame

# define constants
REDUCE_DEPTH = 32
REDUCE_LIMIT = 4096


class Bezier(object):
    """
    Represents a cubic Bezier curve. This is just an experimental object to be
    able to calculate various attributes of a cubic Bezier curve.
    """
    
    
    def __init__(self, x1, y1, cx1, cy1, cx2, cy2, x2, y2):
        """
        Initialize a new instance of cubic Bezier curve.
        
        Args:
            x1: int or float
                X-coordinate of the start point.
            
            y1: int or float
                Y-coordinate of the start point.
            
            cx1: int or float
                X-coordinate of the start control point.
            
            cy1: int or float
                Y-coordinate of the start control point.
            
            cx2: int or float
                X-coordinate of the end control point.
            
            cy2: int or float
                Y-coordinate of the end control point.
            
            x2: int or float
                X-coordinate of the end point.
            
            y2: int or float
                Y-coordinate of the end point.
        """
        
        self._x1 = float(x1)
        self._y1 = float(y1)
        self._p1 = (self._x1, self._y1)
        
        self._cx1 = float(cx1)
        self._cy1 = float(cy1)
        self._c1 = (self._cx1, self._cy1)
        
        self._cx2 = float(cx2)
        self._cy2 = float(cy2)
        self._c2 = (self._cx2, self._cy2)
        
        self._x2 = float(x2)
        self._y2 = float(y2)
        self._p2 = (self._x2, self._y2)
        
        self._t1 = 0.
        self._t2 = 1.
        
        self._is_simple = None
        self._is_line = None
        self._is_linear = None
        
        self._bbox = None
        self._extremes = None
        self._inflections = None
        self._reduced = None
        
        self._derivs = helpers.derivatives(*self.points)
    
    
    def __str__(self):
        """Gets standard string representation."""
        
        return "C(%d,%d %d,%d %d,%d %d,%d)" % (
            self._x1, self._y1,
            self._cx1, self._cy1,
            self._cx2, self._cy2,
            self._x2, self._y2)
    
    
    def __repr__(self):
        """Gets debug string representation."""
        
        return "%s(%s)" % (self.__class__.__name__, self.__str__())
    
    
    @property
    def coords(self):
        """
        Gets curve coordinates as x1, y1, cx1, cy1, cx2, cy2, x2, y2.
        
        Returns:
            (float, float, float, float, float, float, float, float)
                Curve coordinates.
        """
        
        return (
            self._x1, self._y1,
            self._cx1, self._cy1,
            self._cx2, self._cy2,
            self._x2, self._y2)
    
    
    @property
    def points(self):
        """
        Gets curve coordinates as p1, c1, c2, p2.
        
        Returns:
            ((float, float), (float, float), (float, float), (float, float))
                Curve coordinates.
        """
        
        return self._p1, self._c1, self._c2, self._p2
    
    
    @property
    def start(self):
        """
        Gets curve start point as x1, y1.
        
        Returns:
            (float, float)
                Curve start point.
        """
        
        return self._p1
    
    
    @property
    def end(self):
        """
        Gets curve end point as x2, y2.
        
        Returns:
            (float, float)
                Curve end point.
        """
        
        return self._p2
    
    
    @property
    def c1(self):
        """
        Gets curve first control point as cx1, cy1.
        
        Returns:
            (float, float)
                Curve first control point.
        """
        
        return self._c1
    
    
    @property
    def c2(self):
        """
        Gets curve second control point as cx2, cy2.
        
        Returns:
            (float, float)
                Curve second control point.
        """
        
        return self._c2
    
    
    def is_line(self):
        """
        Gets a value indicating if current curve is a straight line, where a line
        is defined as having all control points on the baseline and the control
        points are between the end points.
        
        Returns:
            bool
                Returns True if straight line, False otherwise.
        """
        
        if self._is_line is None:
            
            c1, c2, p2 = helpers.align(self._p1, self._p2, self._c1, self._c2, self._p2)
            _, tolerance = helpers.tolerances(self.points)
            
            self._is_line = (
                abs(c1[1]) <= tolerance and
                abs(c2[1]) <= tolerance and
                -tolerance <= c1[0] <= c2[0] <= p2[0]+tolerance)
        
        return self._is_line
    
    
    def is_linear(self):
        """
        Gets a value indicating if current curve is a straight line with linear
        parameterization.
        
        Returns:
            bool
                Returns True if linearly parameterized, False otherwise.
        """
        
        if self._is_linear is None:
            
            if not self.is_line():
                self._is_linear = False
                return self._is_linear
            
            c1 = helpers.relative(self._p1, self._p2, 1./3.)
            c2 = helpers.relative(self._p1, self._p2, 2./3.)
            _, tolerance = helpers.tolerances(self.points)
            
            self._is_linear = (
                helpers.distance(self._c1, c1) <= tolerance and
                helpers.distance(self._c2, c2) <= tolerance)
        
        return self._is_linear
    
    
    def is_simple(self):
        """
        Gets a value indicating if current curve is simple, where a simpleness
        is defined as having all control points on the same side of the
        baseline, the control-to-end-point lines may not cross and the angle
        between the end point normals is no greater than 60 degrees.
        
        Returns:
            bool
                Returns True if simple, False otherwise.
        """
        
        if self._is_simple is None:
            
            if self.is_line():
                self._is_simple = True
                return self._is_simple
            
            a1 = helpers.angle(self._p2, self._p1, self._c1)
            a2 = helpers.angle(self._p2, self._p1, self._c2)
            
            if (a1 > 0 > a2) or (a1 < 0 < a2):
                self._is_simple = False
            
            else:
                nx1, ny1 = self.normal(0)
                nx2, ny2 = self.normal(1)
                
                if None in (nx1, ny1, nx2, ny2):
                    self._is_simple = True
                
                else:
                    s = nx1*nx2 + ny1*ny2
                    self._is_simple = s >= .5
        
        return self._is_simple
    
    
    def bbox(self):
        """
        Calculates current curve bounding box based on anchors and extremes.
        
        Returns:
            pero.Frame
                Curve bounding box.
        """
        
        if self._bbox is None:
            
            self._bbox = Frame(self._x1, self._y1, self._x2-self._x1, self._y2-self._y1)
            
            if self.is_line():
                return self._bbox.clone()
            
            extremes = self.extremes()
            extremes = set(extremes[0]+extremes[1])
            
            for t in extremes:
                x, y = self.point(t)
                self._bbox.extend(x, y)
        
        return self._bbox.clone()
    
    
    def extremes(self):
        """
        Calculates all extremes of current curve. For each dimension it provides
        all the t-values at which the extremes occur.
        
        Returns:
            ((float,), (float,))
                Extremes t-values for each dimension.
        """
        
        if self._extremes is None:
            
            if self.is_line():
                self._extremes = ((), ())
                return self._extremes
            
            ex = []
            
            for dim in (0, 1):
                s = lambda v: v[dim]
                
                p = list(map(s, self._derivs[0]))
                roots = []
                
                for root in helpers.droots(p):
                    root = helpers.snap_t(root, helpers.ROOT_EPSILON)
                    if helpers.in_unit(root, helpers.ROOT_EPSILON):
                        roots.append(min(1., max(0., root)))
                
                ex.append(tuple(helpers.unique(roots, helpers.ROOT_EPSILON)))
            
            self._extremes = tuple(ex)
        
        return self._extremes
    
    
    def inflections(self):
        """
        Calculates all the inflection points of current curve as their t-values.
        
        Returns:
            (float,)
                Inflections t-values.
        """
        
        if self._inflections is None:
            
            if self.is_line():
                self._inflections = ()
                return self._inflections
            
            p = helpers.align(self._p1, self._p2, *self.points)
            
            a = float(p[2][0] * p[1][1])
            b = float(p[3][0] * p[1][1])
            c = float(p[1][0] * p[2][1])
            d = float(p[3][0] * p[2][1])
            
            coeffs = numpy.array((
                18 * (-3*a + 2*b + 3*c - d),
                18 * (3*a - b - 3*c),
                18 * (c - a)), dtype=float)
            
            scale = max(abs(x) for x in coeffs)
            if scale == 0:
                self._inflections = ()
                return self._inflections
            
            coeffs /= scale
            while len(coeffs) > 1 and abs(coeffs[0]) <= helpers.COEFF_EPSILON:
                coeffs = coeffs[1:]
            
            result = []
            if len(coeffs) > 1:
                for root in numpy.roots(coeffs):
                    
                    if abs(root.imag) > helpers.ROOT_EPSILON:
                        continue
                    
                    t = helpers.snap_t(float(root.real), helpers.ROOT_EPSILON)
                    if helpers.in_unit(t, helpers.ROOT_EPSILON):
                        result.append(t)
            
            self._inflections = tuple(helpers.unique(result, helpers.ROOT_EPSILON))
        
        return self._inflections
    
    
    def reduced(self):
        """
        Splits current curve into multiple simple segments, where the simpleness
        is defined as having all control points on the same side of the
        baseline, the control-to-end-point lines may not cross and the angle
        between the end point normals is no greater than 60 degrees.
        
        Returns:
            (pero.Bezier,)
                Collection of simple segments.
        """
        
        if self._reduced is None:
            
            curve = self
            if self._t1 != 0. or self._t2 != 1.:
                curve = self.clone()
                curve._t1 = 0.
                curve._t2 = 1.
            
            if curve.is_simple():
                self._reduced = tuple((curve,))
                return self._reduced
            
            pass1 = []
            pass2 = []
            
            extremes = curve.extremes()
            extremes = helpers.unique(
                (0., 1.) + extremes[0] + extremes[1],
                helpers.ROOT_EPSILON)
            
            t1 = extremes[0]
            for i in range(1, len(extremes)):
                t2 = extremes[i]
                segment = curve.slice(t1, t2)
                pass1.append(segment)
                t1 = t2
            
            stack = [(segment, 0.) for segment in reversed(pass1)]
            count = 0
            while stack:
                
                segment, depth = stack.pop()
                count += 1
                
                if count > REDUCE_LIMIT:
                    raise RuntimeError("Bezier reduction limit exceeded.")
                
                if segment.is_simple():
                    pass2.append(segment)
                    continue
                
                if depth >= REDUCE_DEPTH:
                    raise RuntimeError("Bezier reduction depth exceeded.")
                
                left, right = segment.split(0.5)
                stack.append((right, depth + 1))
                stack.append((left, depth + 1))
            
            self._reduced = tuple(pass2)
        
        return self._reduced
    
    
    def point(self, t):
        """
        Calculates x and y coordinates of the curve point at specified t-value.
        Note that the t-values are not distributed linearly along the curve but
        are influenced by the control points.
        
        Args:
            t: float
                The t-value position in range of 0-1.
        
        Returns:
            (float, float)
                Coordinates of the curve point.
        """
        
        if t == 0:
            return self._p1
        if t == 1:
            return self._p2
        
        mt = 1 - t
        a = mt*mt*mt
        b = mt*mt*t*3
        c = mt*t*t*3
        d = t*t*t
        
        x = a*self._x1 + b*self._cx1 + c*self._cx2 + d*self._x2
        y = a*self._y1 + b*self._cy1 + c*self._cy2 + d*self._y2
        
        return x, y
    
    
    def derivative(self, t):
        """
        Calculates the curve tangent at the specified t-value as a
        not-normalized vector.
        
        Args:
            t: float
                The t-value position in range of 0-1.
        
        Returns:
            (float, float)
                Derivatives vector.
        """
        
        mt = 1 - t
        a = mt*mt
        b = mt*t*2
        c = t*t
        
        p = self._derivs[0]
        
        dx = a*p[0][0] + b*p[1][0] + c*p[2][0]
        dy = a*p[0][1] + b*p[1][1] + c*p[2][1]
        
        return dx, dy
    
    
    def tangent(self, t):
        """
        Calculates the curve tangent at the specified t-value as a normalized
        vector.
        
        Args:
            t: float
                The t-value position in range of 0-1.
        
        Returns:
            (float, float)
                Normalized tangent vector.
        """
        
        dx, dy = self.derivative(t)
        scale = max(abs(dx), abs(dy))
        
        if scale == 0:
            return None, None
        
        dx /= scale
        dy /= scale
        q = math.hypot(dx, dy)
        
        return dx/q, dy/q
    
    
    def normal(self, t):
        """
        Calculates the curve normal at the specified t-value as a normalized
        vector.
        
        Args:
            t: float
                The t-value position in range of 0-1.
        
        Returns:
            (float, float)
                Normalized normal vector.
        """
        
        dx, dy = self.derivative(t)
        scale = max(abs(dx), abs(dy))
        
        if scale == 0:
            return None, None
        
        dx /= scale
        dy /= scale
        q = math.hypot(dx, dy)
        
        return -dy/q, dx/q
    
    
    def hull(self, t):
        """
        Calculates the hull points for all iterations at specified t-value.
        This generates in total 10 points grouped by iterations. The first
        iteration contains 4 points, the second iteration contains 3 points, the
        third iteration contains 2 points and finally the fourth iteration
        contains just a single point, which is the point of the curve.
        
        Args:
            t: float
                The t-value position in range of 0-1.
        
        Returns:
            (((float, float),),)
                Coordinates of the hull points.
        """
        
        p = self.points
        h = [list(p)]
        
        while len(p) > 1:
            
            buff = []
            for i in range(len(p)-1):
                buff.append(helpers.relative(p[i], p[i+1], t))
            
            h.append(buff)
            p = buff
        
        return tuple(h)
    
    
    def split(self, t):
        """
        Splits current curve at specified t-value position. For the edge values
        of t-value the edge segment is set to None and a clone of current curve
        is returned for the other segment.
        
        Args:
            t: float
                The t-value position in range of 0-1.
        
        Returns:
            (pero.Bezier, pero.Bezier)
                Two new curves as a result of splitting.
        """
        
        if t == 0:
            return None, self.clone()
        if t == 1:
            return self.clone(), None
        
        h = self.hull(t)
        
        x1, y1 = h[0][0]
        cx1, cy1 = h[1][0]
        cx2, cy2 = h[2][0]
        x2, y2 = h[3][0]
        left = Bezier(x1, y1, cx1, cy1, cx2, cy2, x2, y2)
        
        x1, y1 = h[3][0]
        cx1, cy1 = h[2][1]
        cx2, cy2 = h[1][2]
        x2, y2 = h[0][3]
        right = Bezier(x1, y1, cx1, cy1, cx2, cy2, x2, y2)
        
        left._t1 = helpers.scale_t(0, 0, 1, self._t1, self._t2)
        left._t2 = helpers.scale_t(t, 0, 1, self._t1, self._t2)
        right._t1 = helpers.scale_t(t, 0, 1, self._t1, self._t2)
        right._t2 = helpers.scale_t(1, 0, 1, self._t1, self._t2)
        
        return left, right
    
    
    def slice(self, t1, t2):
        """
        Makes a slice of current curve at specified t-value positions.
        
        Args:
            t1: float
                The starting t-value position in range of 0-1.
            
            t2: float
                The end t-value position in range of 0-1.
        
        Returns:
            pero.Bezier
                Slice of current curve.
        """
        
        if t1 == t2:
            return None
        
        if t1 > t2:
            t1, t2 = t2, t1
        
        left, right = self.split(t1)
        
        t2 = (t2 - t1) / (1. - t1)
        
        left, right = right.split(t2)
        
        return left
    
    
    def equals(self, curve, threshold=0):
        """
        Checks if there is a complete overlap between current curve
        and given curve.
        
        Args:
            curve: pero.Bezier
                Curve to check.
            
            threshold: int or float
                Coordinate comparison tolerance.
        
        Returns:
            bool
                Returns True if the curves are completely overlapping, False
                otherwise.
        """
        
        pairs = zip(self.points, curve.points)
        return all(helpers.distance(a, b) <= threshold for a, b in pairs)
    
    
    def overlaps(self, curve, threshold=0):
        """
        Checks if there is any overlap between bounding boxes of current curve
        and given curve.
        
        Args:
            curve: pero.Bezier
                Curve to check.
            
            threshold: int or float
                Coordinate comparison tolerance.
        
        Returns:
            bool
                Returns True if any overlap of bounding boxes exists, False
                otherwise.
        """
        
        return self.bbox().overlaps(curve.bbox(), threshold=threshold)
    
    
    def cuts(self, x1, y1, x2, y2):
        """
        Finds the intersections between current curve and specified infinite
        line. Intersections are returned as t-values of current curve.
        
        Args:
            x1: int or float
                X-coordinate of the line start point.
            
            y1: int or float
                Y-coordinate of the line start point.
            
            x2: int or float
                X-coordinate of the line end point.
            
            y2: int or float
                Y-coordinate of the line end point.
        
        Returns:
            (float,)
                Intersections as t-values for current curve.
        """
        
        if x1 == x2 and y1 == y2:
            return tuple()
        
        return tuple(helpers.roots((x1, y1), (x2, y2), *self.points))
    
    
    def xcuts(self, x):
        """
        Finds the intersections between current curve and an infinite line going
        through given x-coordinate. Intersections are returned as t-values of
        current curve.
        
        Args:
            x: int, float
                X-coordinate of the cut.
        
        Returns:
            (float,)
                Intersections as t-values for current curve.
        """
        
        return self.cuts(x, -1, x, 1)
    
    
    def ycuts(self, y):
        """
        Finds the intersections between current curve and an infinite line going
        through given y-coordinate. Intersections are returned as t-values of
        current curve.
        
        Args:
            y: int, float
                Y-coordinate of the cut.
        
        Returns:
            (float,)
                Intersections as t-values for current curve.
        """
        
        return self.cuts(-1, y, 1, y)
    
    
    def intersects(self, curve=None, tolerance=None):
        """
        Finds the intersections between current curve and another. Intersections
        are returned as pairs of t-values, where the first corresponds to this
        curve and the second corresponds to the other curve.
        
        If the curve is not specified, self intersections of current curve are
        returned.
        
        Args:
            curve: pero.Bezier or None
                Curve to intersect with current curve.
            
            tolerance: float or None
                Coordinate tolerance used for intersection matching. A
                scale-aware tolerance is calculated if omitted.
        
        Returns:
            ((float,float),)
                Intersections as t-values for current and given curves.
        """
        
        return intersects.intersects(self, curve, tolerance)
    
    
    def reversed(self):
        """
        Creates a copy with reversed parameter direction.
        
        Returns:
            pero.Bezier
                Cloned curve.
        """
        
        return Bezier(
            self._x2, self._y2,
            self._cx2, self._cy2,
            self._cx1, self._cy1,
            self._x1, self._y1)
    
    
    def clone(self):
        """
        Creates exact clone of current curve.
        
        Returns:
            pero.Bezier
                Cloned curve.
        """
        
        curve = Bezier(
            self._x1, self._y1,
            self._cx1, self._cy1,
            self._cx2, self._cy2,
            self._x2, self._y2)
        
        curve._t1 = self._t1
        curve._t2 = self._t2
        
        return curve
    
    
    @staticmethod
    def from_line(x1, y1, x2, y2):
        """
        Creates a Bezier curve from a straight line.
        
        Args:
            x1: int, float
                X-coordinate of the start point.
            
            y1: int, float
                Y-coordinate of the start point.
            
            x2: int, float
                X-coordinate of the end point.
            
            y2: int, float
                Y-coordinate of the end point.
        
        Returns:
            pero.Bezier
                Bezier curve representing the line.
        """
        
        dx = (x2 - x1) / 3.
        dy = (y2 - y1) / 3.
        
        return Bezier(
            x1, y1,
            x1 + dx, y1 + dy,
            x2 - dx, y2 - dy,
            x2, y2)
