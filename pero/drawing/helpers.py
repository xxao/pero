#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import math
from . utils import *

# Legendre-Gauss abscissas
T_VALUES = (
  -0.0640568928626056260850430826247450385909,
   0.0640568928626056260850430826247450385909,
  -0.1911188674736163091586398207570696318404,
   0.1911188674736163091586398207570696318404,
  -0.3150426796961633743867932913198102407864,
   0.3150426796961633743867932913198102407864,
  -0.4337935076260451384870842319133497124524,
   0.4337935076260451384870842319133497124524,
  -0.5454214713888395356583756172183723700107,
   0.5454214713888395356583756172183723700107,
  -0.6480936519369755692524957869107476266696,
   0.6480936519369755692524957869107476266696,
  -0.7401241915785543642438281030999784255232,
   0.7401241915785543642438281030999784255232,
  -0.8200019859739029219539498726697452080761,
   0.8200019859739029219539498726697452080761,
  -0.8864155270044010342131543419821967550873,
   0.8864155270044010342131543419821967550873,
  -0.9382745520027327585236490017087214496548,
   0.9382745520027327585236490017087214496548,
  -0.9747285559713094981983919930081690617411,
   0.9747285559713094981983919930081690617411,
  -0.9951872199970213601799974097007368118745,
   0.9951872199970213601799974097007368118745)

# Legendre-Gauss weights
C_VALUES = (
  0.1279381953467521569740561652246953718517,
  0.1279381953467521569740561652246953718517,
  0.1258374563468282961213753825111836887264,
  0.1258374563468282961213753825111836887264,
  0.1216704729278033912044631534762624256070,
  0.1216704729278033912044631534762624256070,
  0.1155056680537256013533444839067835598622,
  0.1155056680537256013533444839067835598622,
  0.1074442701159656347825773424466062227946,
  0.1074442701159656347825773424466062227946,
  0.0976186521041138882698806644642471544279,
  0.0976186521041138882698806644642471544279,
  0.0861901615319532759171852029837426671850,
  0.0861901615319532759171852029837426671850,
  0.0733464814110803057340336152531165181193,
  0.0733464814110803057340336152531165181193,
  0.0592985849154367807463677585001085845412,
  0.0592985849154367807463677585001085845412,
  0.0442774388174198061686027482113382288593,
  0.0442774388174198061686027482113382288593,
  0.0285313886289336631813078159518782864491,
  0.0285313886289336631813078159518782864491,
  0.0123412297999871995468056670700372915759,
  0.0123412297999871995468056670700372915759)


def tolerances(points):
    """Calculates extent and tolerance for given points."""
    
    if not points:
        return 1., 1e-9
    
    xs = [float(x[0]) for x in points]
    ys = [float(x[1]) for x in points]
    
    extent = max(max(xs) - min(xs), max(ys) - min(ys), numpy.finfo(float).eps)
    magnitude = max([abs(x) for x in xs + ys] + [1.])
    precision = abs(numpy.spacing(magnitude)) * 32.
    tolerance = max(extent * 1e-10, precision, numpy.finfo(float).eps * 32.)
    
    return extent, tolerance


def relative(p1, p2, r):
    """pass"""
    
    x = p1[0] + r*(p2[0] - p1[0])
    y = p1[1] + r*(p2[1] - p1[1])
    
    return x, y


def derivatives(*points):
    """pass"""
    
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
    """pass"""
    
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


def crt(v):
    """pass"""
    
    s = -1 if v < 0 else 1
    return s*numpy.power(s*v, 1./3)


def roots(p1, p2, *points):
    """Finds cubic Bezier intersections with an infinite line as t-values."""

    aligned = align(p1, p2, *points)
    pa, pb, pc, pd = (x[1] for x in aligned)
    coefficients = [
        -pa + 3*pb - 3*pc + pd,
        3*pa - 6*pb + 3*pc,
        -3*pa + 3*pb,
        pa]

    scale = max(abs(x) for x in coefficients)
    if scale == 0:
        return []

    cutoff = scale*1e-14
    while coefficients and abs(coefficients[0]) <= cutoff:
        coefficients.pop(0)
    if len(coefficients) <= 1:
        return []

    values = []
    for root in numpy.roots(coefficients):
        if abs(root.imag) > 1e-8:
            continue
        value = float(root.real)
        if -1e-9 <= value <= 1.+1e-9:
            values.append(min(1., max(0., value)))

    values.sort()
    roots = []
    for value in values:
        if not roots or abs(value-roots[-1]) > 1e-8:
            roots.append(value)

    return roots


def droots(p):
    """pass"""
    
    if len(p) == 2:
        a, b = p
        if a != b:
            return [float(a) / (a - b)]
    
    elif len(p) == 3:
        a, b, c = p
        d = float(a - 2*b + c)
        e = b*b - a*c
        
        if e < 0:
            return []
        
        if d != 0:
            m1 = -numpy.sqrt(e)
            m2 = -a + b
            v1 = -(m1 + m2)/d
            v2 = -(-m1 + m2)/d
            
            return [v1, v2]
        
        elif b != c:
            return [float(2*b - c) / (2*(b - c))]
    
    return []


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


def subtract(p1, p2):
    """pass"""
    
    return p1[0]-p2[0], p1[1]-p2[1]


def dot(p1, p2):
    """pass"""
    
    return p1[0]*p2[0]+p1[1]*p2[1]


def cross(p1, p2):
    """pass"""
    
    return p1[0]*p2[1]-p1[1]*p2[0]


def length(value):
    """pass"""
    
    return math.hypot(value[0], value[1])


def in_unit(value, epsilon):
    """pass"""
    
    return -epsilon <= value <= 1.+epsilon


def snap(value, epsilon):
    """pass"""
    
    if abs(value) <= epsilon:
        return 0.
    
    if abs(value - 1.) <= epsilon:
        return 1.
    
    return value


def line_distance(p1, p2, p):
    """Gets distance from line to give point."""
    
    direction = subtract(p2, p1)
    length_value = length(direction)
    
    if length_value == 0:
        return distance(p, p1)
    
    return abs(cross(subtract(p, p1), direction)) / length_value
