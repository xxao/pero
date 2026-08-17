#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from . import helpers

# define constants
PARAM_EPSILON = 1e-7
DIAGONAL_EPSILON = 1e-5
ENDPOINT_EPSILON = 1e-9
DISTANCE_FACTOR = 4.
SCALE_FACTOR = 1e-9
MATCH_FACTOR = 8.
THIN_FACTOR = 2.


def intersects(first, second=None, tolerance=None):
    """Gets intersection parameter pairs using one coordinate tolerance."""
    
    # get anchors and controls
    points = first.points
    if second is not None:
        points += second.points
    
    # adjust thresholds
    scale, numeric_tolerance = helpers.tolerances(points)
    tolerance = numeric_tolerance if tolerance is None else max(tolerance, numeric_tolerance)
    threshold = max(tolerance * DISTANCE_FACTOR, scale * SCALE_FACTOR)
    
    # calc self intersects
    if second is None:
        result = _intersect_self(first, threshold)
    
    # calc two curves intersects
    else:
        
        # check if any overlap
        if not first.overlaps(second, threshold):
            return tuple()
        
        # calc line-line intersects
        if first.is_line() and second.is_line():
            result = _intersect_line_line(first, second, tolerance)
        
        # calc line-curve intersects
        elif first.is_line():
            result = _intersect_line_curve(first, second, tolerance)
        
        # calc curve-line intersects
        elif second.is_line():
            result = _intersect_curve_line(first, second, tolerance)
        
        # calc curve-curve intersects
        else:
            result = _intersect_curve_curve(first, second, threshold, tolerance)
    
    # check results
    if not result:
        return tuple()
    
    # snap values to 0, 1
    result = [(helpers.snap_t(x[0], PARAM_EPSILON), helpers.snap_t(x[1], PARAM_EPSILON)) for x in result]
    
    # keep unique only
    return tuple(helpers.unique_pairs(result, PARAM_EPSILON))


def _intersect_line_line(first, second, tolerance):
    """Calculates intersections between two straight segments."""
    
    # get vectors
    p = first.start
    r = helpers.subtract(first.end, first.start)
    q = second.start
    s = helpers.subtract(second.end, second.start)
    rxs = helpers.cross(r, s)
    qmp = helpers.subtract(q, p)
    
    # adjust tolerance
    threshold = tolerance * max(
        helpers.distance(first.start, first.end),
        helpers.distance(second.start, second.end),
        1.)
    
    # calc regular intersect
    if abs(rxs) > threshold:
        u = helpers.cross(qmp, s)/rxs
        v = helpers.cross(qmp, r)/rxs
        if not (helpers.in_unit(u, ENDPOINT_EPSILON) and
                helpers.in_unit(v, ENDPOINT_EPSILON)):
            return []
        
        point = (p[0]+u*r[0], p[1]+u*r[1])
        params_first = _intersect_point(first, point, tolerance)
        params_second = _intersect_point(second, point, tolerance)
        
        return [(t1, t2) for t1 in params_first for t2 in params_second]
    
    # check collinear
    if abs(helpers.cross(qmp, r)) > threshold:
        return []
    
    # calc overlapping endpoints
    result = []
    for t1, point in ((0., first.start), (1., first.end)):
        for t2 in _intersect_point(second, point, tolerance):
            result.append((t1, t2))
    
    for t2, point in ((0., second.start), (1., second.end)):
        for t1 in _intersect_point(first, point, tolerance):
            result.append((t1, t2))
    
    # keep unique only
    return helpers.unique_pairs(result, ENDPOINT_EPSILON)


def _intersect_curve_line(curve, line, tolerance):
    """Calculates intersections between a curve and a straight segment."""
    
    # check empty line
    if helpers.distance(line.start, line.end) <= tolerance:
        return []
    
    # calc line cuts
    result = []
    for t1 in curve.cuts(*line.start, *line.end):
        
        # check within interval
        if not helpers.in_unit(t1, ENDPOINT_EPSILON):
            continue
        
        # get line intersect
        t1 = min(1., max(0., t1))
        point = curve.point(t1)
        for t2 in _intersect_point(line, point, tolerance):
            result.append((t1, t2))
    
    return result


def _intersect_line_curve(line, curve, tolerance):
    """Calculates intersections between a straight segment and a curve."""
    
    return [(b, a) for a, b in _intersect_curve_line(curve, line, tolerance)]


def _intersect_curve_curve(first, second, threshold, tolerance):
    """Calculates intersections between two non-linear curves."""
    
    # adjust tolerance
    match_tolerance = tolerance*MATCH_FACTOR
    
    # check if equal
    if first.equals(second, match_tolerance):
        return [(0., 0.), (1., 1.)]
    if first.equals(second.reversed(), match_tolerance):
        return [(0., 1.), (1., 0.)]
    
    # check for overlaps
    endpoints = _intersect_endpoints(first, second, tolerance)
    overlaps = _intersect_overlaps(first, second, endpoints, tolerance)
    if overlaps:
        return overlaps
    
    # check endpoints
    box_first = first.bbox()
    box_second = second.bbox()
    overlap_w = min(box_first.right, box_second.right) - max(box_first.left, box_second.left)
    overlap_h = min(box_first.bottom, box_second.bottom) - max(box_first.top, box_second.top)
    thin_tolerance = tolerance*THIN_FACTOR
    if endpoints and (overlap_w <= thin_tolerance or overlap_h <= thin_tolerance):
        return endpoints
    
    # calc regular curve-curve intersects
    return endpoints + _intersect_curves(first, second, threshold)


def _intersect_self(curve, threshold):
    """Calculates all intersection points of a curve with itself."""
    
    # no intersects for line
    if curve.is_line():
        return []
    
    # get reduced segments
    reduced = curve.reduced()
    
    # get segments intersects
    result = []
    for i in range(len(reduced)-2):
        first = reduced[i]
        for second in reduced[i+2:]:
            if first.overlaps(second):
                result += _intersect_simple(first, second, threshold)
    
    # filter diagonals
    result = [t for t in result if abs(t[0] - t[1]) > DIAGONAL_EPSILON]
    
    return result


def _intersect_point(curve, point, tolerance):
    """Gets parameters at which a curve passes through a point."""
    
    # adjust threshold
    threshold = tolerance * MATCH_FACTOR
    
    # cut linearized line
    if curve.is_linear():
        
        direction = helpers.subtract(curve.end, curve.start)
        squared_length = helpers.dot(direction, direction)
        if squared_length == 0:
            return []
        
        sub = helpers.subtract(point, curve.start)
        roots = [helpers.dot(sub, direction) / squared_length]
    
    # cut curve
    else:
        dx = max(x[0] for x in curve.points) - min(x[0] for x in curve.points)
        dy = max(x[1] for x in curve.points) - min(x[1] for x in curve.points)
        roots = curve.xcuts(point[0]) if dx >= dy else curve.ycuts(point[1])
    
    # filter results
    result = []
    for t in roots:
        if helpers.in_unit(t, ENDPOINT_EPSILON) and helpers.distance(curve.point(t), point) <= threshold:
            result.append(min(1., max(0., t)))
    
    # keep unique only
    return helpers.unique(result, ENDPOINT_EPSILON)


def _intersect_curves(first, second, threshold):
    """Calculates recursive intersections between two curves."""
    
    # get reduced segments
    reduced_first = first.reduced()
    reduced_second = second.reduced()
    result = []
    
    # get segments intersects
    for part_first in reduced_first:
        for part_second in reduced_second:
            if part_first.overlaps(part_second):
                result += _intersect_simple(part_first, part_second, threshold)
    
    return result


def _intersect_simple(first, second, threshold):
    """Calculates intersections between two simple curve segments."""
    
    # get bbox
    box_first = first.bbox()
    box_second = second.bbox()
    
    # threshold reached
    if box_first.w+box_first.h < threshold and box_second.w+box_second.h < threshold:
        t1 = .5*(first._t1+first._t2)
        t2 = .5*(second._t1+second._t2)
        return ((t1, t2),)
    
    # get first segment and split if needed
    parts_first = (first,)
    if box_first.w+box_first.h >= threshold:
        parts_first = first.split(.5)
    
    # get second segment and split if needed
    parts_second = (second,)
    if box_second.w+box_second.h >= threshold:
        parts_second = second.split(.5)
    
    # intersect recursion
    result = []
    for part_first in parts_first:
        for part_second in parts_second:
            if part_first.overlaps(part_second):
                result += _intersect_simple(part_first, part_second, threshold)
    
    return result


def _intersect_endpoints(first, second, tolerance):
    """Gets matching endpoint parameter pairs."""
    
    # adjust threshold
    threshold = tolerance*MATCH_FACTOR
    
    # get matches
    result = []
    for t1, p1 in ((0., first.start), (1., first.end)):
        for t2, p2 in ((0., second.start), (1., second.end)):
            if helpers.distance(p1, p2) <= threshold:
                result.append((t1, t2))
    
    return result


def _intersect_overlaps(first, second, candidates, tolerance):
    """Gets the endpoint pairs of coincident curve spans."""
    
    # make list
    candidates = list(candidates)
    
    # add first endpoints overlaps
    for t1, point in ((0., first.start), (1., first.end)):
        for t2 in _intersect_point(second, point, tolerance):
            candidates.append((t1, t2))
    
    # add second endpoints overlaps
    for t2, point in ((0., second.start), (1., second.end)):
        for t1 in _intersect_point(first, point, tolerance):
            candidates.append((t1, t2))
    
    # keep unique only
    candidates = helpers.unique_pairs(candidates, ENDPOINT_EPSILON)
    if len(candidates) < 2:
        return []
    
    # explore overlaps
    result = []
    for i, left in enumerate(candidates[:-1]):
        for right in candidates[i+1:]:
            
            if abs(left[0]-right[0]) <= ENDPOINT_EPSILON:
                continue
            if abs(left[1]-right[1]) <= ENDPOINT_EPSILON:
                continue
            
            part_first = _directed_slice(first, left[0], right[0])
            part_second = _directed_slice(second, left[1], right[1])
            
            if part_first.equals(part_second, tolerance):
                result.extend((left, right))
    
    # keep unique only
    return helpers.unique_pairs(result, ENDPOINT_EPSILON)


def _directed_slice(curve, t1, t2):
    """Gets a slice preserving the direction of its parameter interval."""
    
    if t1 <= t2:
        return curve.slice(t1, t2)
    
    return curve.slice(t2, t1).reversed()
