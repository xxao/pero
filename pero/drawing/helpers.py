#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
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
    """pass"""
    
    roots = []
    
    p = align(p1, p2, *points)
    f = lambda x: 0 <= x <= 1
    
    pa = p[0][1]
    pb = p[1][1]
    pc = p[2][1]
    pd = p[3][1]
    
    d = float(-pa + 3*pb - 3*pc + pd)
    a = (3*pa - 6*pb + 3*pc) / d
    b = (-3*pa + 3*pb) / d
    c = pa / d
    p = (3*b - a*a)/3.
    p3 = p/3.
    q = (2*a*a*a - 9*a*b + 27*c)/27.
    q2 = q/2.
    
    discr = q2*q2 + p3*p3*p3
    tau = 2*numpy.pi
    
    if discr < 0:
        
        mp3 = -p/3.
        mp33 = mp3*mp3*mp3
        r = numpy.sqrt(mp33)
        t = -q/(2*r)
        
        cosphi = t
        if t < -1:
            cosphi = -1
        elif t > 1:
            cosphi = 1
        
        phi = numpy.arccos(cosphi)
        crtr = crt(r)
        t1 = 2*crtr
        
        x1 = t1 * numpy.cos(phi/3) - a/3
        x2 = t1 * numpy.cos((phi+tau)/3) - a/3
        x3 = t1 * numpy.cos((phi+2*tau)/3) - a/3
        
        roots = [x1, x2, x3]
    
    elif discr == 0:
        
        u1 = crt(-q2) if q2 < 0 else -crt(q2)
        x1 = 2*u1 - a/3.
        x2 = -u1 - a/3.
        
        roots = [x1, x2]
    
    else:
        sd = numpy.sqrt(discr)
        u1 = crt(-q2+sd)
        v1 = crt(q2+sd)
        
        roots = [u1-v1-a/3.]
    
    return list(filter(f, roots))


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
