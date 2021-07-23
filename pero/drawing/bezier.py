#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# Adapted from the original code by Pomax
# https://pomax.github.io/bezierinfo/

# import modules
import numpy
from . import helpers
from . frame import Frame

# define constants
PROJECTION_STEP = 0.1
REDUCE_STEP = 0.1
LUT_STEPS = 100
INTERSECT_THRESHOLD = 0.1


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
        self._lut = []
        
        self._simple = None
        self._bbox = None
        self._extremes = None
        self._inflections = None
        self._length = None
        
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
    
    
    def simple(self):
        """
        Gets a value indicating if current curve is simple, where a simpleness
        is defined as having all control points on the same side of the
        baseline, the control-to-end-point lines may not cross and the angle
        between the end point normals is no greater than 60 degrees.
        
        Returns:
            bool
                Returns True if simple, False otherwise.
        """
        
        if self._simple is None:
            
            a1 = helpers.angle(self._p2, self._p1, self._c1)
            a2 = helpers.angle(self._p2, self._p1, self._c1)
            
            if (a1 > 0 > a2) or (a1 < 0 < a2):
                self._simple = False
            
            else:
                nx1, ny1 = self.normal(0)
                nx2, ny2 = self.normal(1)
                
                if None in (nx1, ny1, nx2, ny2):
                    self._simple = True
                
                else:
                    s = nx1*nx2 + ny1*ny2
                    a = abs(numpy.arccos(s))
                    self._simple = a < numpy.pi/3
        
        return self._simple
    
    
    def bbox(self):
        """
        Calculates current curve bounding box based on anchors and extremes.
        
        Returns:
            pero.Frame
                Curve bounding box.
        """
        
        if self._bbox is None:
            
            self._bbox = Frame(self._x1, self._y1, self._x2-self._x1, self._y2-self._y1)
            
            extremes = self.extremes()
            extremes = set(extremes[0]+extremes[1])
            
            for t in extremes:
                x, y = self.point(t)
                self._bbox.extend(x, y)
        
        return self._bbox.clone()
    
    
    def length(self):
        """
        Calculates the length of current curve using numerical approximation.
        
        Returns:
            float
                Current curve length.
        """
        
        if self._length is None:
            self._length = 0
            
            for i in range(len(helpers.T_VALUES)):
                t = 0.5 * helpers.T_VALUES[i] + 0.5
                dx, dy = self.derivative(t)
                self._length += helpers.C_VALUES[i] * numpy.sqrt(dx*dx + dy*dy)
        
            self._length *= .5
        
        return self._length
    
    
    def extremes(self):
        """
        Calculates all extremes of current curve. For each dimension it provides
        all the t-values at which the extremes occur.
        
        Returns:
            ((float,), (float,))
                Extremes t-values for each dimension.
        """
        
        if self._extremes is None:
            
            ex = [[], []]
            
            for dim in (0, 1):
                s = lambda v: v[dim]
                
                p = list(map(s, self._derivs[0]))
                ex[dim] = helpers.droots(p)
                
                p = list(map(s, self._derivs[1]))
                ex[dim] += helpers.droots(p)
                
                f = lambda v: (0 <= v <= 1)
                ex[dim] = list(filter(f, ex[dim]))
            
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
            
            p = helpers.align(self._p1, self._p2, *self.points)
            
            a = float(p[2][0] * p[1][1])
            b = float(p[3][0] * p[1][1])
            c = float(p[1][0] * p[2][1])
            d = float(p[3][0] * p[2][1])
            
            v1 = 18 * (-3*a + 2*b + 3*c - d)
            v2 = 18 * (3*a - b - 3*c)
            v3 = 18 * (c - a)
            
            if helpers.equals(v1, 0, 1e-3):
                
                if not helpers.equals(v2, 0, 1e-3):
                    t = -v3 / v2
                    if 0 <= t <= 1:
                        return [t]
                return []
            
            d = 2*v1
            if helpers.equals(d, 0, 1e-3):
                return []
            
            trm = v2*v2 - 4*v1*v3
            if trm < 0:
                return []
            
            sq = numpy.sqrt(v2*v2 - 4*v1*v3)
            buff = []
            
            t1 = (sq-v2)/d
            if 0 <= t1 <= 1:
                buff.append(t1)
            
            t2 = -(v2+sq)/d
            if 0 <= t2 <= 1:
                buff.append(t2)
            
            self._inflections = tuple(buff)
        
        return self._inflections
    
    
    def lut(self, steps=LUT_STEPS):
        """
        Generates a look-up table of coordinates on current curve, spaced at
        parametrically equidistant intervals of 1/steps.
        
        Args:
            steps: int
                Number of steps to generate.
        
        Returns:
            ((float, float),)
                Positions look-up table.
        """
        
        if len(self._lut) == steps+1:
            return self._lut
        
        self._lut = []
        for t in range(steps+1):
            self._lut.append(self.point(float(t)/steps))
        
        self._lut = tuple(self._lut)
        
        return self._lut
    
    
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
        Calculates the curve tangent at the specified t-value as a not-
        normalized vector.
        
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
        q = numpy.sqrt(dx*dx + dy*dy)
        
        if dx == 0 and dy == 0:
            return None, None
        
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
        
        if dx == 0 and dy == 0:
            print("Bad curve:", self)
            return None, None
        
        q = numpy.sqrt(dx*dx + dy*dy)
        
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
        
        left._t1 = self._scale_t(0, 0, 1, self._t1, self._t2)
        left._t2 = self._scale_t(t, 0, 1, self._t1, self._t2)
        right._t1 = self._scale_t(t, 0, 1, self._t1, self._t2)
        right._t2 = self._scale_t(1, 0, 1, self._t1, self._t2)
        
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
    
    
    def reduce(self):
        """
        Splits current curve into multiple simple segments, where the simpleness
        is defined as having all control points on the same side of the
        baseline, the control-to-end-point lines may not cross and the angle
        between the end point normals is no greater than 60 degrees.
        
        Returns:
            (pero.Bezier,)
                Collection of simple segments.
        """
        
        if self.simple():
            return tuple((self, ))
        
        pass1 = []
        pass2 = []
        step = REDUCE_STEP
        
        extremes = self.extremes()
        extremes = list(set([0] + extremes[0] + extremes[1] + [1]))
        extremes.sort()
        
        t1 = extremes[0]
        for i in range(1, len(extremes)):
            t2 = extremes[i]
            
            segment = self.slice(t1, t2)
            segment._t1 = t1
            segment._t2 = t2
            
            pass1.append(segment)
            t1 = t2
        
        for p1 in pass1:
            
            if p1.simple():
                pass2.append(p1)
                continue
            
            t1 = 0
            t2 = 0
            while t2 <= 1:
                
                t2 = t1 + step
                while t2 <= 1+step:
                    
                    # not sure about this :)
                    if abs(t1 - t2) < step:
                        t1 = t2
                        break
                    
                    segment = p1.slice(t1, t2)
                    
                    if not segment.simple():
                        t2 -= step
                        
                        if abs(t1 - t2) < step:
                            t1 = t2
                            break
                        
                        segment = p1.slice(t1, t2)
                        segment._t1 = self._scale_t(t1, 0, 1, p1._t1, p1._t2)
                        segment._t2 = self._scale_t(t2, 0, 1, p1._t1, p1._t2)
                        
                        pass2.append(segment)
                        t1 = t2
                        break
                    
                    t2 += step
            
            if t1 < 1:
                
                tmp, segment = p1.split(t1)
                segment._t1 = self._scale_t(t1, 0, 1, p1._t1, p1._t2)
                segment._t2 = p1._t2
                
                pass2.append(segment)
        
        return tuple(pass2)
    
    
    def project(self, x, y):
        """
        Finds the point on current curve, nearest to specified coordinates. This
        gives back the on-curve coordinates, t-value and distance.
        
        Args:
            x: int or float
                X-coordinate of the point.
            
            y: int or float
                Y-coordinate of the point.
        
        Returns:
            (float, float, float, float)
                Results as x,y coordinates, t-value and distance.
        """
        
        lut = self.lut()
        nearest = self._get_nearest_lut(lut, x, y)
        idx = nearest[0]
        dist = nearest[1]
        ln = len(lut)-1.
        
        if idx == 0 or idx == ln:
            t = idx / ln
            p = self.point(t)
            
            return p[0], p[1], t, dist
        
        t1 = (idx - 1.) / ln
        t2 = (idx + 1.) / ln
        t = t1
        ft = t
        step = PROJECTION_STEP/ln
        dist += 1
        
        while t < t2+step:
            
            p = self.point(t)
            dx = x - p[0]
            dy = y - p[1]
            d = numpy.sqrt(dx*dx + dy*dy)
            
            if d < dist:
                dist = d
                ft = t
            
            t += step
        
        p = self.point(ft)
        
        return p[0], p[1], t, dist
    
    
    def overlaps(self, curve):
        """
        Checks if there is any overlap between bounding boxes of current curve
        and given curve.
        
        Args:
            curve: pero.Bezier
                Curve to check.
        
        Returns:
            bool
                Returns True if any overlap of bounding boxes exists, False
                otherwise.
        """
        
        return self.bbox().overlaps(curve.bbox())
    
    
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
    
    
    def intersects(self, curve=None, threshold=INTERSECT_THRESHOLD):
        """
        Finds the intersections between current curve and another. Intersections
        are returned as pairs of t-values, where the first corresponds to this
        curve and the second corresponds to the other curve.
        
        If the curve is not specified, self intersections of current curve are
        returned.
        
        Args:
            curve: pero.Bezier or None
                Curve to intersect with current curve.
            
            threshold: float
                Resolution threshold as a maximum size of a segment.
        
        Returns:
            ((float,float),)
                Intersections as t-values for current and given curves.
        """
        
        if curve is None:
            inters = self._intersects_self(threshold)
        else:
            inters = self._intersects_curve(curve, threshold)
        
        if not inters:
            return tuple()
        
        inters.sort()
        buff = [inters[0]]
        t1 = buff[-1]
        
        for t2 in inters[1:]:
            
            if not helpers.equals(t1[0], t2[0], 1e-3):
                buff.append(t2)
                t1 = t2
            
            elif not helpers.equals(t1[1], t2[1], 1e-3):
                buff.append(t2)
                t1 = t2
        
        return tuple(buff)
    
    
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
    
    
    def _scale_t(self, t, ds, de, ts, te):
        """Scales given t-value into new range."""
    
        return ts + (te-ts)*(t-ds)/(de-ds)
    
    
    def _get_nearest_lut(self, lut, x, y):
        """Gets closest item and distance from look-up table."""
        
        dist = numpy.power(2., 63)
        idx = 0
        
        for i, p in enumerate(lut):
            
            dx = x - p[0]
            dy = y - p[1]
            d = numpy.sqrt(dx*dx + dy*dy)
            
            if d < dist:
                dist = d
                idx = i
        
        return idx, dist
    
    
    def _intersects_self(self, threshold):
        """Calculates all intersection points with self."""
        
        reduced = self.reduce()
        
        buff = []
        for i in range(len(reduced)-2):
            
            seg1 = reduced[i:i+1]
            seg2 = reduced[i+2:]
            
            pairs = []
            for s1 in seg1:
                for s2 in seg2:
                    if s1.overlaps(s2):
                        pairs.append((s1, s2))
            
            for pair in pairs:
                buff += self._intersect_simple(pair[0], pair[1], threshold)
        
        return buff
    
    
    def _intersects_curve(self, curve, threshold):
        """Calculates all intersection points with given curve."""
        
        seg1 = self.reduce()
        seg2 = curve.reduce()
        
        pairs = []
        for s1 in seg1:
            for s2 in seg2:
                if s1.overlaps(s2):
                    pairs.append((s1, s2))
        
        buff = []
        for pair in pairs:
            buff += self._intersect_simple(pair[0], pair[1], threshold)
        
        return buff
    
    
    def _intersect_simple(self, c1, c2, threshold):
        """Calculates all intersection points between two simple segments."""
        
        c1b = c1.bbox()
        c2b = c2.bbox()
        
        if c1b.w + c1b.h < threshold and c2b.w + c2b.h < threshold:
            t1 = 0.5 * (c1._t1 + c1._t2)
            t2 = 0.5 * (c2._t1 + c2._t2)
            return tuple(((t1, t2),))
        
        seg1 = (c1,)
        if c1b.w + c1b.h >= threshold:
            seg1 = c1.split(0.5)
        
        seg2 = (c2,)
        if c2b.w + c2b.h >= threshold:
            seg2 = c2.split(0.5)
        
        pairs = []
        for s1 in seg1:
            for s2 in seg2:
                if s1.overlaps(s2):
                    pairs.append((s1,s2))
        
        buff = []
        for pair in pairs:
            buff += self._intersect_simple(pair[0], pair[1], threshold)
        
        return buff
