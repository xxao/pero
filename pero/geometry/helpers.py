#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from . utils import *

# define constants
COEFF_EPSILON = 1e-14
ROOT_EPSILON = 1e-9


def scale_t(t, ds, de, ts, te):
    """Scales given t-value into new range."""
    
    return ts + (te - ts) * (t - ds) / (de - ds)


def snap_t(value, epsilon):
    """Snaps given t-value to 0 or 1 if within given epsilon."""
    
    if abs(value) <= epsilon:
        return 0.
    
    if abs(value - 1.) <= epsilon:
        return 1.
    
    return value


def in_unit(value, epsilon):
    """Returns True if given value is within unit range with given epsilon."""
    
    return -epsilon <= value <= 1.+epsilon


def tolerances(points):
    """Calculates extent and tolerance for given points."""
    
    if not points:
        return 1., 1e-9
    
    xs = [float(x[0]) for x in points]
    ys = [float(x[1]) for x in points]
    
    magnitude = max([abs(x) for x in xs + ys] + [1.])
    precision = abs(numpy.spacing(magnitude)) * 32.
    
    extent = max(max(xs) - min(xs), max(ys) - min(ys), numpy.finfo(float).eps)
    tolerance = max(extent * 1e-10, precision, numpy.finfo(float).eps * 32.)
    
    return extent, tolerance


def relative(p1, p2, r):
    """Calculates a point relative to two given points and a ratio."""
    
    x = p1[0] + r*(p2[0] - p1[0])
    y = p1[1] + r*(p2[1] - p1[1])
    
    return x, y


def derivatives(*points):
    """Calculates derivatives for given control points."""
    
    d = []
    p = points
    
    i = len(p)
    c = i - 1
    
    while i > 1:
        
        buff = []
        for j in range(c):
            x = c * (p[j+1][0] - p[j][0])
            y = c * (p[j+1][1] - p[j][1])
            buff.append((x, y))
        
        d.append(buff)
        p = buff
        
        i -= 1
        c -= 1
    
    return d


def align(p1, p2, *points):
    """Aligns given points relative to a line defined by two points."""
    
    x1, y1 = p1
    x2, y2 = p2
    
    a = -numpy.arctan2(y2-y1, x2-x1)
    sin = numpy.sin(a)
    cos = numpy.cos(a)
    
    buff = []
    for px, py in points:
        x = (px-x1)*cos - (py-y1)*sin
        y = (px-x1)*sin + (py-y1)*cos
        buff.append((x, y))
    
    return buff


def align_y(p1, p2, *points):
    """Gets scale-safe y-values after aligning points to a line."""
    
    if p1 == p2:
        return None
    
    all_points = (p1, p2) + points
    
    scale = max(abs(v) for p in all_points for v in p)
    if scale:
        p1 = [v/scale for v in p1]
        p2 = [v/scale for v in p2]
        points = [[v/scale for v in p] for p in points]
    
    aligned = align(p1, p2, *points)
    
    return numpy.array([p[1] for p in aligned], dtype=float)


def roots(p1, p2, *points):
    """Finds cubic Bezier intersections with an infinite line as t-values."""
    
    ordinates = align_y(p1, p2, *points)
    if ordinates is None:
        return []
    
    scale = max(abs(v) for v in ordinates)
    if scale <= COEFF_EPSILON:
        return [0., 1.]
    
    a, b, c, d = ordinates/scale
    coeffs = (
        -a + 3*b - 3*c + d,
        3*a - 6*b + 3*c,
        -3*a + 3*b,
        a)
    
    values = real_roots(coeffs)
    values = (
        snap_t(x, ROOT_EPSILON)
        for x in values
        if in_unit(x, ROOT_EPSILON))
    
    return unique(values, ROOT_EPSILON)


def droots(p):
    """Gets the real roots of a linear or quadratic Bezier derivative."""
    
    values = numpy.asarray(p, dtype=float)
    if len(values) not in (2, 3):
        return []
    
    scale = max(abs(v) for v in values)
    if scale == 0:
        return []
    
    values = values/scale
    if len(values) == 2:
        a, b = values
        coeffs = (b-a, a)
    else:
        a, b, c = values
        coeffs = (a-2*b+c, 2*(b-a), a)
    
    return real_roots(coeffs)


def real_roots(coeffs):
    """Gets the unique real roots of a polynomial."""
    
    coeffs = numpy.asarray(coeffs, dtype=float)
    
    scale = max(abs(c) for c in coeffs)
    if scale == 0:
        return []
    
    coeffs = coeffs/scale
    while len(coeffs) > 1 and abs(coeffs[0]) <= COEFF_EPSILON:
        coeffs = coeffs[1:]
    
    if len(coeffs) <= 1:
        return []
    
    result = []
    for root in numpy.roots(coeffs):
        value = float(root.real)
        if (abs(root.imag) <= ROOT_EPSILON and
            abs(numpy.polyval(coeffs, value)) <= ROOT_EPSILON):
            result.append(value)
    
    return unique(result, ROOT_EPSILON)


def unique(values, tolerance):
    """Returns a list of unique values within a given tolerance."""
    
    values = sorted(values)
    result = []
    for value in values:
        if not result or abs(value - result[-1]) > tolerance:
            result.append(value)
            
    return result


def unique_pairs(values, tolerance):
    """Returns a list of unique pairs within a given tolerance."""
    
    values = sorted(values)
    result = []
    for value in values:
        if not any(abs(value[0] - x[0]) <= tolerance and
                   abs(value[1] - x[1]) <= tolerance for x in result):
            result.append(value)
    
    return result
