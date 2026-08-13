#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
import numpy

from ..enums import *
from . import helpers
from .bezier import Bezier


_PARAM_EPSILON = 1e-9


class _Segment(object):
    """Represents a single path segment with topology and geometry information."""
    
    
    def __init__(self, kind, start, end, c1=None, c2=None,
        operand=0, contour=0, source=None, t1=0., t2=1.):
        """Initializes a new instance of the _Segment class."""
        
        self.kind = kind
        self.curve = None
        
        self.source = self if source is None else source.source
        self.operand = operand
        self.contour = contour
        self.params = [0., 1.]
        self.t1 = float(t1)
        self.t2 = float(t2)
        
        self._init_curve(start, c1, c2, end)
    
    
    @classmethod
    def create(cls, kind, curve, operand, contour, tolerance):
        """Creates a topology segment from given Bezier curve with tolerance check."""
        
        start, c1, c2, end = curve.points
        
        if kind == PATH_LINE:
            if helpers.distance(start, end) <= tolerance:
                return None
            
            return _Segment(kind, start, end, c1, c2,
                operand = operand,
                contour = contour)
        
        points = (start, c1, c2, end)
        if max(helpers.distance(start, x) for x in points[1:]) <= tolerance:
            return None
        
        baseline = helpers.subtract(end, start)
        length = helpers.length(baseline)
        if length > tolerance:
            
            d1 = abs(helpers.cross(helpers.subtract(c1, start), baseline)) / length
            d2 = abs(helpers.cross(helpers.subtract(c2, start), baseline)) / length
            if d1 <= tolerance and d2 <= tolerance:
                
                u1 = helpers.dot(helpers.subtract(c1, start), baseline) / (length * length)
                u2 = helpers.dot(helpers.subtract(c2, start), baseline) / (length * length)
                if -_PARAM_EPSILON <= u1 <= u2 <= 1. + _PARAM_EPSILON:
                    
                    return _Segment(PATH_LINE, start, end,
                        operand = operand,
                        contour = contour)
        
        return _Segment(kind, start, end, c1, c2,
            operand = operand,
            contour = contour)
    
    
    @property
    def start(self):
        """Gets the start point of the segment."""
        
        return self.curve.start
    
    
    @start.setter
    def start(self, value):
        """Sets the start point of the segment."""
        
        self._init_curve(value, self.curve.c1, self.curve.c2, self.curve.end)
    
    
    @property
    def end(self):
        """Gets the end point of the segment."""
        
        return self.curve.end
    
    
    @end.setter
    def end(self, value):
        """Sets the end point of the segment."""
        
        self._init_curve(self.curve.start, self.curve.c1, self.curve.c2, value)
    
    
    @property
    def c1(self):
        """Gets the first control point of the segment."""
        
        return self.curve.c1
    
    
    @property
    def c2(self):
        """Gets the second control point of the segment."""
        
        return self.curve.c2
    
    
    @property
    def points(self):
        """Gets the points of the segment as (start, c1, c2, end)."""
        
        return self.curve.points
    
    
    def command(self):
        """Gets the path command representing this segment."""
        
        if self.kind == PATH_LINE:
            return (PATH_LINE,) + self.end
        
        return (PATH_CURVE,) + self.c1 + self.c2 + self.end
    
    
    def bbox(self):
        """Gets bounding box of the segment as (min_x, min_y, max_x, max_y)."""
        
        bbox = self.curve.bbox()
        return bbox.left, bbox.top, bbox.right, bbox.bottom
    
    
    def point(self, t):
        """Gets a point on the segment at parameter t."""
        
        return self.curve.point(t)
    
    
    def derivative(self, t):
        """Gets a tangent vector on the segment at parameter t."""
        
        return self.curve.derivative(t)
    
    
    def crossings(self, point, tolerance):
        """Gets horizontal line crossing and winding contributions."""
        
        x, y = point
        crossings = 0
        winding = 0
        
        if self.kind == PATH_LINE:
            
            y1 = self.start[1]
            y2 = self.end[1]
            
            if not ((y1 <= y < y2) or (y2 <= y < y1)):
                return crossings, winding
            
            cross_x = self.start[0] + (y-y1)*(self.end[0]-self.start[0])/(y2-y1)
            if cross_x > x+tolerance:
                return 1, 1 if y2 > y1 else -1
            
            return crossings, winding
        
        for t in self.curve.ycuts(y):
            
            if t < -_PARAM_EPSILON or t >= 1.-_PARAM_EPSILON:
                continue
            
            t = max(0., t)
            if self.point(t)[0] <= x+tolerance:
                continue
            
            before = self.point(max(0., t-1e-6))[1]-y
            after = self.point(min(1., t+1e-6))[1]-y
            if before*after > 0:
                continue
            
            dy = self.derivative(t)[1]
            if abs(dy) <= tolerance:
                dy = after-before
            if abs(dy) <= tolerance:
                continue
            
            crossings += 1
            winding += 1 if dy > 0 else -1
        
        return crossings, winding
    
    
    def overlaps(self, other, tolerance):
        """Checks if the segment overlaps with another segment."""
        
        return self.curve.overlaps(other.curve, tolerance)
    
    
    def split(self, t):
        """Adds a split parameter."""
        
        value = min(1., max(0., float(t)))
        if not any(abs(value - x) <= _PARAM_EPSILON for x in self.params):
            self.params.append(value)
    
    
    def slice(self, t1, t2):
        """Gets a new segment representing the slice between parameters t1 and t2."""
        
        if t2 < t1:
            return self.slice(t2, t1).reversed()
        
        curve = self.curve.slice(t1, t2)
        t1 = self.t1+(self.t2-self.t1)*t1
        t2 = self.t1+(self.t2-self.t1)*t2
        
        return _Segment(self.kind, curve.start, curve.end, curve.c1, curve.c2,
            operand = self.operand,
            contour = self.contour,
            source = self,
            t1 = t1,
            t2 = t2)
    
    
    def fragments(self, tolerance):
        """Gets a list of segments representing the split fragments of the segment."""
        
        result = []
        
        params = sorted(self.params)
        for t1, t2 in zip(params[:-1], params[1:]):
            
            if t2-t1 <= _PARAM_EPSILON:
                continue
            
            piece = self.slice(t1, t2)
            
            if helpers.distance(piece.start, piece.end) <= tolerance:
                if piece.kind == PATH_LINE:
                    continue
                if max(helpers.distance(piece.start, x) for x in piece.points[1:]) <= tolerance:
                    continue
            
            result.append(piece)
        
        return result
    
    
    def boundary(self, contours_a, rule_a, contours_b, rule_b, operation, tolerance, scale):
        """Returns the correctly directed segment if it bounds the result."""
        
        point = self.point(.5)
        tangent = self.derivative(.5)
        
        if helpers.length(tangent) <= tolerance:
            for t in (.37, .63, .2, .8):
                point = self.point(t)
                tangent = self.derivative(t)
                if helpers.length(tangent) > tolerance:
                    break
        
        length = helpers.length(tangent)
        if length <= tolerance:
            return None
        
        normal = (-tangent[1]/length, tangent[0]/length)
        offset = max(tolerance*16., scale*1e-8)
        
        for multiplier in (1., .25, .0625, 4.):
            
            delta = offset*multiplier
            left = (point[0]+normal[0]*delta, point[1]+normal[1]*delta)
            right = (point[0]-normal[0]*delta, point[1]-normal[1]*delta)
            
            left_value = self._boolean(
                self._inside(left, contours_a, rule_a, tolerance),
                self._inside(left, contours_b, rule_b, tolerance), operation)
            
            right_value = self._boolean(
                self._inside(right, contours_a, rule_a, tolerance),
                self._inside(right, contours_b, rule_b, tolerance), operation)
            
            if left_value != right_value:
                return self if left_value else self.reversed()
        
        return None
    
    
    def reversed(self):
        """Gets a new segment representing the reversed segment."""
        
        return _Segment(self.kind, self.end, self.start, self.c2, self.c1,
            operand = self.operand,
            contour = self.contour,
            source = self,
            t1 = self.t2,
            t2 = self.t1)
    
    
    def merge(self, other, tolerance):
        """Merges adjacent compatible segments, if possible."""
        
        if helpers.distance(self.end, other.start) > tolerance*8.:
            return None
        
        if self.source is other.source and abs(self.t2-other.t1) <= _PARAM_EPSILON:
            return self.source.slice(self.t1, other.t2)
        
        if self.kind != PATH_LINE or other.kind != PATH_LINE:
            return None
        
        a = helpers.subtract(self.end, self.start)
        b = helpers.subtract(other.end, other.start)
        limit = tolerance*max(helpers.length(a), helpers.length(b), 1.)
        
        if abs(helpers.cross(a, b)) > limit or helpers.dot(a, b) < 0:
            return None
        
        return _Segment(PATH_LINE, self.start, other.end,
            operand = self.operand,
            contour = self.contour)
    
    
    def intersects(self, other, tolerance, scale):
        """Gets intersection parameter pairs with self or given segment."""
        
        if other is None:
            return self._intersect_self(tolerance, scale)
        
        if self.kind == PATH_LINE and other.kind == PATH_LINE:
            return self._intersect_line_line(other, tolerance)
        
        if self.kind == PATH_LINE:
            return self._intersect_line_curve(other, tolerance)
        
        if other.kind == PATH_LINE:
            return self._intersect_curve_line(other, tolerance)
        
        if self.curve.equals(other.curve, tolerance * 8.):
            return [(0., 0.), (1., 1.)]
        
        if self.curve.equals(other.reversed().curve, tolerance * 8.):
            return [(0., 1.), (1., 0.)]
        
        overlaps = self._intersect_overlaps(other, tolerance)
        if overlaps:
            return overlaps
        
        box1 = self.bbox()
        box2 = other.bbox()
        overlap_w = min(box1[2], box2[2]) - max(box1[0], box2[0])
        overlap_h = min(box1[3], box2[3]) - max(box1[1], box2[1])
        
        endpoints = self._intersect_endpoints(other, tolerance)
        if endpoints and (overlap_w <= tolerance * 2. or overlap_h <= tolerance * 2.):
            return endpoints
        
        threshold = max(tolerance * 4., scale * 1e-9)
        result = list(endpoints)
        result.extend(self.curve.intersects(other.curve, threshold))
        result = [(helpers.snap(x[0], 1e-7), helpers.snap(x[1], 1e-7)) for x in result]
        
        return helpers.unique_pairs(result, 1e-7)
    
    
    def _init_curve(self, start, c1, c2, end):
        """Initializes the Bezier curve for the segment."""
        
        if self.kind == PATH_LINE or c1 is None:
            c1 = helpers.relative(start, end, 1. / 3.)
        
        if self.kind == PATH_LINE or c2 is None:
            c2 = helpers.relative(start, end, 2. / 3.)
        
        self.curve = Bezier(*start, *c1, *c2, *end)
    
    
    def _inside(self, point, contours, fill_rule, tolerance):
        """Checks if a point is inside given contours according to the fill rule."""
        
        winding = 0
        crossings = 0
        
        for contour in contours:
            count, direction = contour.crossings(point, tolerance)
            crossings += count
            winding += direction
        
        return bool(crossings % 2) if fill_rule == EVENODD else winding != 0
    
    
    def _boolean(self, a, b, operation):
        """Returns the boolean value of two inside checks according to the operation."""
        
        if operation == BOOL_UNION:
            return a or b
        
        if operation == BOOL_INTERSECT:
            return a and b
        
        return a and not b
    
    
    def _intersect_self(self, tolerance, scale):
        """Gets self-intersection parameter pairs."""
        
        if self.kind == PATH_LINE:
            return []
        
        threshold = max(tolerance*4., scale*1e-9)
        result = [x for x in self.curve.intersects(None, threshold) if abs(x[0]-x[1]) > 1e-5]
        
        return helpers.unique_pairs(result, 1e-6)
    
    
    def _intersect_line_line(self, other, tolerance):
        """Gets line intersection parameter pairs with another line segment."""
        
        p = self.start
        r = helpers.subtract(self.end, self.start)
        q = other.start
        s = helpers.subtract(other.end, other.start)
        rxs = helpers.cross(r, s)
        qmp = helpers.subtract(q, p)
        limit = tolerance * max(helpers.length(r), helpers.length(s), 1.)
        
        if abs(rxs) > limit:
            t1 = helpers.cross(qmp, s) / rxs
            t2 = helpers.cross(qmp, r) / rxs
            if helpers.in_unit(t1, _PARAM_EPSILON) and helpers.in_unit(t2, _PARAM_EPSILON):
                return [(t1, t2)]
            return []
        
        if abs(helpers.cross(qmp, r)) > limit:
            return []
        
        rr = helpers.dot(r, r)
        ss = helpers.dot(s, s)
        if rr == 0 or ss == 0:
            return []
        
        t0 = helpers.dot(qmp, r) / rr
        t1 = t0 + helpers.dot(s, r) / rr
        low = max(0., min(t0, t1))
        high = min(1., max(t0, t1))
        if high < low - _PARAM_EPSILON:
            return []
        
        result = []
        for t1 in (low, high):
            point = self.point(t1)
            t2 = helpers.dot(helpers.subtract(point, q), s) / ss
            if helpers.in_unit(t2, _PARAM_EPSILON):
                result.append((t1, t2))
        
        return helpers.unique_pairs(result, _PARAM_EPSILON)
    
    
    def _intersect_line_curve(self, other, tolerance):
        """Gets line intersection parameter pairs with another curve segment."""
        
        return [(b, a) for a, b in other._intersect_curve_line(self, tolerance)]
    
    
    def _intersect_curve_line(self, other, tolerance):
        """Gets curve intersection parameter pairs with another line segment."""
        
        direction = helpers.subtract(other.end, other.start)
        length = helpers.dot(direction, direction)
        if length == 0:
            return []
        
        result = []
        
        for t1 in self.curve.cuts(*other.start, *other.end):
            
            if not helpers.in_unit(t1, _PARAM_EPSILON):
                continue
            
            p = self.point(t1)
            t2 = helpers.dot(helpers.subtract(p, other.start), direction) / length
            distance = helpers.line_distance(other.start, other.end, p)
            
            if helpers.in_unit(t2, _PARAM_EPSILON) and distance <= tolerance * 4.:
                result.append((t1, t2))
        
        return helpers.unique_pairs(result, _PARAM_EPSILON)
    
    
    def _intersect_candidates(self, point, tolerance):
        
        dx = max(x[0] for x in self.points) - min(x[0] for x in self.points)
        dy = max(x[1] for x in self.points) - min(x[1] for x in self.points)
        roots = self.curve.xcuts(point[0]) if dx >= dy else self.curve.ycuts(point[1])
        
        result = []
        for t in roots:
            if (helpers.in_unit(t, _PARAM_EPSILON) and
                    helpers.distance(self.point(t), point) <= tolerance * 8.):
                result.append(min(1., max(0., t)))
        
        return result
    
    
    def _intersect_overlaps(self, other, tolerance):
        """pass"""
        
        candidates = []
        
        for t1, p in ((0., self.start), (1., self.end)):
            for t2 in other._intersect_candidates(p, tolerance):
                candidates.append((t1, t2))
        
        for t2, p in ((0., other.start), (1., other.end)):
            for t1 in self._intersect_candidates(p, tolerance):
                candidates.append((t1, t2))
        
        candidates = helpers.unique_pairs(candidates, _PARAM_EPSILON)
        if len(candidates) < 2:
            return []
        
        result = []
        for i, left in enumerate(candidates[:-1]):
            for right in candidates[i + 1:]:
                
                if abs(left[0] - right[0]) <= _PARAM_EPSILON:
                    continue
                if abs(left[1] - right[1]) <= _PARAM_EPSILON:
                    continue
                
                a = self.slice(left[0], right[0])
                b = other.slice(left[1], right[1])
                if a.curve.equals(b.curve, tolerance * 8.):
                    result.extend((left, right))
        
        return result
    
    
    def _intersect_endpoints(self, other, tolerance):
        """pass"""
        
        result = []
        for t1, p1 in ((0., self.start), (1., self.end)):
            for t2, p2 in ((0., other.start), (1., other.end)):
                if helpers.distance(p1, p2) <= tolerance*8.:
                    result.append((t1, t2))
        
        return result


class _Contour(object):
    """Represents an ordered closed collection of path segments."""
    
    
    def __init__(self, segments=None):
        """Initializes a new instance of the _Contour class."""
        
        self.segments = list(segments or ())
    
    
    def __bool__(self):
        """Returns True if the contour has any segments."""
        
        return bool(self.segments)
    
    
    def __len__(self):
        """Gets number of segments in the contour."""
        
        return len(self.segments)
    
    
    def __iter__(self):
        """Gets an iterator over the contour segments."""
        
        return iter(self.segments)
    
    
    def __getitem__(self, index):
        """Gets the segment at given index."""
        
        return self.segments[index]
    
    
    def append(self, segment):
        """Appends given segment to the contour."""
        
        self.segments.append(segment)
    
    
    def commands(self, tolerance):
        """Serializes the contour into closed path commands."""
        
        commands = [(PATH_MOVE,) + self.segments[0].start]
        
        for i, seg in enumerate(self.segments):
            
            if (i == len(self.segments) - 1 and
                    seg.kind == PATH_LINE and
                    helpers.distance(seg.end, self.segments[0].start) <= tolerance * 8.):
                continue
            
            commands.append(seg.command())
        
        commands.append((PATH_CLOSE,))
        return commands
    
    
    def bbox(self):
        """Gets bounding box of the contour as (min_x, min_y, max_x, max_y)."""
        
        boxes = [x.bbox() for x in self.segments]
        
        return (
            min(x[0] for x in boxes),
            min(x[1] for x in boxes),
            max(x[2] for x in boxes),
            max(x[3] for x in boxes))
    
    
    def area(self):
        """Gets signed contour area."""
        
        area = 0.
        
        values, weights = numpy.polynomial.legendre.leggauss(5)
        samples = list(zip(values, weights))
        
        for seg in self.segments:
            
            if seg.kind == PATH_LINE:
                area += .5*(seg.start[0]*seg.end[1] - seg.end[0]*seg.start[1])
                continue
            
            total = 0.
            for value, weight in samples:
                t = .5*(value+1.)
                point = seg.point(t)
                tangent = seg.derivative(t)
                total += weight*(point[0]*tangent[1]-point[1]*tangent[0])
            area += .25*total
        
        return area
    
    
    def crossings(self, point, tolerance):
        """Gets horizontal line crossing and winding contributions."""
        
        crossings = 0
        winding = 0
        
        for seg in self.segments:
            count, direction = seg.crossings(point, tolerance)
            crossings += count
            winding += direction
        
        return crossings, winding
    
    
    def normalize(self, tolerance):
        """Reorders segments to start with the top-left anchor."""
        
        index = min(range(len(self.segments)),
            key = lambda i: (
                round(self.segments[i].start[0]/tolerance),
                round(self.segments[i].start[1]/tolerance)))
        
        self.segments = self.segments[index:]+self.segments[:index]
    
    
    def simplify(self, tolerance):
        """Removes unnecessary split anchors and collinear line anchors."""
        
        changed = True
        while changed and len(self.segments) > 1:
            changed = False
            
            for i in range(len(self.segments)):
                j = (i+1) % len(self.segments)
                
                merged = self.segments[i].merge(self.segments[j], tolerance)
                if merged is None:
                    continue
                
                if j == 0:
                    self.segments = [merged]+self.segments[1:i]
                else:
                    self.segments = (self.segments[:i]+[merged]+self.segments[j+1:])
                
                changed = True
                break


class _Nodes(object):
    """Represents a spatial index for path segment endpoints."""
    
    
    def __init__(self, tolerance):
        """Initializes a new instance of the _Nodes class."""
        
        self.tolerance = tolerance * 8.
        self.grid = {}
        self.points = []
    
    
    def add(self, point):
        """Adds a point and returns its index."""
        
        key = self.key(point)
        
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                k = (key[0] + dx, key[1] + dy)
                for index in self.grid.get(k, ()):
                    if helpers.distance(point, self.points[index]) <= self.tolerance:
                        return index
        
        index = len(self.points)
        self.points.append(point)
        self.grid.setdefault(key, []).append(index)
        
        return index
    
    
    def key(self, point):
        """Gets a grid key for given point."""
        
        return (int(math.floor(point[0] / self.tolerance)),
                int(math.floor(point[1] / self.tolerance)))


def operate(first, second, operation):
    """Returns commands representing a boolean operation on two paths."""
    
    points = [p for c in first.beziers() for p in c.points]
    points += [p for c in second.beziers() for p in c.points]
    scale, tolerance = helpers.tolerances(points)
    
    contours_a, segments_a = _parse_path(first, 0, tolerance)
    contours_b, segments_b = _parse_path(second, 1, tolerance)
    segments = segments_a + segments_b
    
    if not segments:
        return ()
    
    _find_intersections(segments, tolerance, scale)
    
    boundary = []
    for seg in segments:
        for frag in seg.fragments(tolerance):
            
            frag = frag.boundary(
                contours_a, first.fill_rule,
                contours_b, second.fill_rule,
                operation, tolerance, scale)
            
            if frag and not any(frag.curve.equals(x.curve, tolerance) for x in boundary):
                boundary.append(frag)
    
    contours = []
    for contour in _stitch_segments(boundary, tolerance):
        contour.simplify(tolerance)
        contour.normalize(tolerance)
        if contour and abs(contour.area()) > tolerance * tolerance:
            contours.append(contour)
    
    commands = []
    for contour in sorted(contours, key=lambda c: (-abs(c.area()), c[0].start)):
        commands += contour.commands(tolerance)
    
    return tuple(commands)


def _parse_path(path, operand_id, tolerance):
    """Parses path into topology segments and contours."""
    
    contours = []
    segments = []
    
    for contour_id, subpath in enumerate(path.split()):
        
        if subpath.is_empty():
            continue
        
        if not subpath.is_closed():
            raise ValueError("Path operation requires closed subpaths.")
        
        contour = _Contour()
        for curve in subpath.beziers():
            kind = PATH_LINE if curve.is_line() else PATH_CURVE
            segment = _Segment.create(kind, curve, operand_id, contour_id, tolerance)
            if segment is not None:
                contour.append(segment)
        
        if contour:
            bbox = contour.bbox()
            if bbox[2]-bbox[0] > tolerance and bbox[3]-bbox[1] > tolerance:
                contours.append(contour)
                segments.extend(contour)
    
    return contours, segments


def _find_intersections(segments, tolerance, scale):
    """Finds and marks splits at any segments intersections."""
    
    for i, first in enumerate(segments):
        
        for t1, t2 in first.intersects(None, tolerance, scale):
            first.split(t1)
            first.split(t2)
        
        for second in segments[i+1:]:
            
            if not first.overlaps(second, tolerance):
                continue
            
            for t1, t2 in first.intersects(second, tolerance, scale):
                
                if first.operand == second.operand \
                    and first.contour == second.contour \
                    and (t1 <= _PARAM_EPSILON and t2 >= 1.-_PARAM_EPSILON) \
                        or (t2 <= _PARAM_EPSILON and t1 >= 1.-_PARAM_EPSILON):
                    continue
                
                first.split(t1)
                second.split(t2)


def _stitch_segments(segments, tolerance):
    """Combines segments into discrete contours."""
    
    if not segments:
        return []
    
    contours = []
    
    nodes = _Nodes(tolerance)
    starts = []
    ends = []
    outgoing = {}
    
    for idx, segment in enumerate(segments):
        start = nodes.add(segment.start)
        end = nodes.add(segment.end)
        starts.append(start)
        ends.append(end)
        outgoing.setdefault(start, []).append(idx)
    
    used = set()
    
    for seed in range(len(segments)):
        
        if seed in used:
            continue
        
        contour = _Contour()
        current = seed
        start_node = starts[seed]
        safety = 0
        
        while current not in used and safety <= len(segments)+1:
            safety += 1
            
            used.add(current)
            segment = segments[current]
            segment.start = nodes.points[starts[current]]
            segment.end = nodes.points[ends[current]]
            contour.append(segment)
            
            end_node = ends[current]
            if end_node == start_node:
                break
            
            candidates = [x for x in outgoing.get(end_node, ()) if x not in used]
            if not candidates:
                contour = _Contour()
                break
            
            current = _choose_next_segment(segment, candidates, segments)
        
        if contour and ends[current] == start_node:
            contours.append(contour)
    
    return contours


def _choose_next_segment(incoming, candidates, segments):
    """Chooses the next segment to continue the contour based on turning angle."""
    
    tangent = incoming.derivative(1.)
    angle = math.atan2(tangent[1], tangent[0])
    
    return max(candidates, key=lambda x: _calc_segment_score(segments[x], angle))


def _calc_segment_score(segment, angle):
    """Calculates the turning angle score for a segment."""
    
    tangent = segment.derivative(0.)
    angle2 = math.atan2(tangent[1], tangent[0])
    
    turn = (angle2 - angle) % (2. * math.pi)
    if turn > math.pi:
        turn -= 2. * math.pi
    
    return turn
