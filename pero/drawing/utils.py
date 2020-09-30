#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy


def rads(angle):
    """
    Converts given angle from degrees to radians.
    
    Args:
        angle: float
            Angle in degrees.
    
    Returns:
        float
            Angle in radians.
    """
    
    return numpy.deg2rad(angle)


def degs(angle):
    """
    Converts given angle from radians to degrees.
    
    Args:
        angle: float
            Angle in radians.
    
    Returns:
        float
            Angle in degrees.
    """
    
    return numpy.rad2deg(angle)


def equals(v1, v2, epsilon=0.000001):
    """
    Returns True if difference between given values is less then tolerance.
    
    Args:
        v1: float
            Value one.
        
        v2: float
            Value two
        
        epsilon: float
            Max allowed difference.
    
    Returns:
        bool
            True if values equal, False otherwise.
    """
    
    return abs(v1-v2) <= epsilon


def between(v, min_v, max_v, epsilon=0.000001):
    """
    Returns True if given value is equal or between minimum and maximum by
    specified tolerance.
    
    Args:
        v: float
            Value to check.
        
        min_v: float
            Minimum value.
        
        max_v: float
            Maximum value.
        
        epsilon: float
            Max allowed difference.
    
    Returns:
        bool
            True if value is equal or between, False otherwise.
    """
    
    return (min_v <= v <= max_v) or equals(v, min_v, epsilon) or equals(v, max_v, epsilon)


def angle(p1, p2, p3):
    """
    Calculates angle between two lines.
    
    Args:
        p1: (float, float)
            First point as (x, y) coordinates.
        
        p2: (float, float)
            Origin point as (x, y) coordinates.
        
        p3: (float, float)
            Second point as (x, y) coordinates.
    
    Returns:
        float
            Angle in radians.
    """
    
    dx1 = p1[0] - p2[0]
    dy1 = p1[1] - p2[1]
    dx2 = p3[0] - p2[0]
    dy2 = p3[1] - p2[1]
    
    cross = dx1*dy2 - dy1*dx2
    dot = dx1*dx2 + dy1*dy2
    
    return numpy.arctan2(cross, dot)


def inclination(p1, p2):
    """
    Calculates inclination angle the line has with x-axis.
    
    Args:
        p1: (float, float)
            Origin point as (x, y) coordinates.
        
        p2: (float, float)
            Second point as (x, y) coordinates.
    
    Returns:
        float
            Angle in radians.
    """
    
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    
    return numpy.arctan2(dy, dx)


def bisector(p1, p2, p3):
    """
    Calculates bisector angle between two lines.
    
    Args:
        p1: (float, float)
            First point as (x, y) coordinates.
        
        p2: (float, float)
            Origin point as (x, y) coordinates.
        
        p3: (float, float)
            Second point as (x, y) coordinates.
    
    Returns:
        float
            Angle in radians.
    """
    
    a1 = inclination(p2, p1)
    a2 = inclination(p2, p3)
    
    return 0.5 * (a1 + a2)


def distance(p1, p2):
    """
    Calculates Euclidean distance between two points.
    
    Args:
        p1: (float, float)
            Point 1 as (x, y) coordinates.
        
        p2: (float,float)
            Point 2 as (x, y) coordinates.
    
    Returns:
        float
            Distance between the points.
    """
    
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    sq = dx*dx + dy*dy
    
    return numpy.sqrt(sq) if sq > 0 else 0


def inline(*points):
    """
    Checks whether all given points are on a single line. The points order
    is not important.
    
    Args:
        *points: ((float, float),)
            Collection of points to check as (x,y) coordinates.
    
    Returns:
        bool
            Returns True if all points are on a single line, False otherwise.
    """
    
    if len(points) < 3:
        return True
    
    x1, y1 = points[0]
    x2, y2 = points[1]
    
    dx1 = x1 - x2
    dy1 = y1 - y2
    
    for x2, y2 in points[2:]:
        dx2 = x1 - x2
        dy2 = y1 - y2
        if (dy1*dx2) != (dx1*dy2):
            return False
    
    return True


def rotate(p, angle, center=(0, 0)):
    """
    Rotates given point around specified center.
    
    Args:
        p: (float, float)
            Point to rotate.
        
        angle: float
            Angle in radians.
        
        center: (float, float)
            Center of rotation.
    """
    
    dx = p[0]-center[0]
    dy = p[1]-center[1]
    
    sin = numpy.sin(angle)
    cos = numpy.cos(angle)
    
    x = center[0] + dx * cos - dy * sin
    y = center[1] + dx * sin + dy * cos
    
    return x, y


def ray(c, angle, distance):
    """
    Calculates point coordinates width distance and angle from origin.
    
    Args:
        c: (float, float)
            XY coordinates of the origin.
        
        angle: float
            Angle in radians.
        
        distance: float
            Distance from origin.
    
    Returns:
            (float, float)
                XY coordinates of calculated point.
    """
    
    x = c[0] + distance * numpy.cos(angle)
    y = c[1] + distance * numpy.sin(angle)
    
    return x, y


def inside_circle(p, c, r):
    """
    Checks whether given point is within specified circle.
    
    Args:
        p: (float, float)
            XY coordinates of the point to test.
        
        c: (float, float)
            XY coordinates of the circle center.
        
        r: float
            Radius of the circle.
    
    Returns:
        bool
            Returns True if the point lies inside the circle, False otherwise.
    """
    
    return distance(c, p) < r


def inside_triangle(p, p1, p2, p3):
    """
    Checks whether given point is within specified triangle.
    
    Args:
        p: (float, float)
            XY coordinates of the point to test.
        
        p1: (float, float)
            XY coordinates of the triangle point.
        
        p2: (float, float)
            XY coordinates of the triangle point.
        
        p3: (float, float)
            XY coordinates of the triangle point.
    
    Returns:
        bool
            Returns True if the point lies inside the circle, False otherwise.
    """
    
    xp, yp = p
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    
    c1 = (x2-x1)*(yp-y1)-(y2-y1)*(xp-x1)
    c2 = (x3-x2)*(yp-y2)-(y3-y2)*(xp-x2)
    c3 = (x1-x3)*(yp-y3)-(y1-y3)*(xp-x3)
    
    return (c1 < 0 and c2 < 0 and c3 < 0) or (c1 > 0 and c2 > 0 and c3 > 0)


def intersect_circles(c1, r1, c2, r2):
    """
    Calculates intersection points between two circles.
    
    Args:
        c1: (float, float)
            XY coordinates of the center of circle A.
        
        r1: float
            Radius of the circle A.
        
        c2: (float, float)
            XY coordinate of the center of circle B.
        
        r2: float
            Radius of the circle b.
    
    Returns:
        ((float, float), (float, float)) or None
            XY coordinates of the two intersection points. Returns None if
            there is no intersection.
    """
    
    # calc distance
    dx = c2[0] - c1[0]
    dy = c2[1] - c1[1]
    dist = numpy.sqrt(dx*dx + dy*dy)
    
    # non intersecting
    if dist >= r1 + r2:
        return None
    
    # one inside another
    if dist <= abs(r1-r2):
        return None
    
    # coincident circles
    if dist == 0 and r1 == r2:
        return None
    
    # calc intersections
    a = (r1**2 - r2**2 + dist**2) / (2*dist)
    n = r1**2 - a**2
    h = numpy.sqrt(n if n > 0 else 0)
    
    x = c1[0] + a*dx / dist
    y = c1[1] + a*dy / dist
    
    x1 = x + h*dy / dist
    y1 = y - h*dx / dist
    x2 = x - h*dy / dist
    y2 = y + h*dx / dist
    
    return (x1, y1), (x2, y2)


def intersect_lines(p1, p2, p3, p4):
    """
    Calculates intersection point between two lines defined as (p1, p2)
    and (p3, p4).
    
    Args:
        p1: (float, float)
            Point 1 as (x, y) coordinates.
        
        p2: (float, float)
            Point 2 as (x, y) coordinates.
        
        p3: (float, float)
            Point 3 as (x, y) coordinates.
        
        p4: (float, float)
            Point 4 as (x, y) coordinates.
    
    Returns:
        (float, float) or None
            XY coordinates of the intersection point. Returns None if
            there is no intersection.
    """
    
    a_dx = p2[0] - p1[0]
    a_dy = p1[1] - p2[1]
    a_sq = p2[0]*p1[1] - p1[0]*p2[1]
    
    b_dx = p4[0] - p3[0]
    b_dy = p3[1] - p4[1]
    b_sq = p4[0]*p3[1] - p3[0]*p4[1]
    
    d = a_dy * b_dx - a_dx * b_dy
    dx = a_sq * b_dx - a_dx * b_sq
    dy = a_dy * b_sq - a_sq * b_dy
    
    if d == 0:
        return None
    
    return dx/d, dy/d


def intersect_rays(p1, a1, p2, a2):
    """
    Calculates intersection point between two lines defined as a point
    coordinates and angle.
    
    Args:
        p1: (float, float)
            First line point 1 as (x, y) coordinates.
        
        a1: float
            First line angle in radians.
        
        p2: (float, float)
            Second line point as (x, y) coordinates.
        
        a2: float
            Second line angle in radians.
    
    Returns:
        (float, float) or None
            XY coordinates of the intersection point. Returns None if
            there is no intersection.
    """
    
    l1 = (p1[0] + numpy.cos(a1), p1[1] + numpy.sin(a1))
    l2 = (p2[0] + numpy.cos(a2), p2[1] + numpy.sin(a2))
    
    return intersect_lines(p1, l1, p2, l2)


def polygon_centroid(*points):
    """
    Calculates center point of given polygon.
    
    Args:
        points: ((float, float),)
            Collection of points as (x, y) coordinates.
    
    Returns:
        (float, float)
            Center point as (x, y) coordinates.
    """
    
    x = sum(p[0] for p in points) / len(points)
    y = sum(p[1] for p in points) / len(points)
    
    return x, y


def triangle_incircle(p1, p2, p3):
    """
    Calculates position and size of the biggest circle inscribed into
    specified triangle.
    
    Args:
        p1: (float, float)
            Point 1 as (x, y) coordinates.
        
        p2: (float, float)
            Point 2 as (x, y) coordinates.
        
        p3: (float, float)
            Point 3 as (x, y) coordinates.
    
    Returns:
        (float, float)
            XY coordinates of the circle center.
        
        float
            Circle radius.
    """
    
    # calc sides
    a = distance(p1, p2)
    b = distance(p2, p3)
    c = distance(p3, p1)
    
    # calc radius
    p = 0.5 * sum((a, b, c))
    area = numpy.sqrt(p * (p - a) * (p - b) * (p - c))
    radius = area / p
    
    # calc center
    bis1 = bisector(p2, p1, p3)
    bis2 = bisector(p1, p2, p3)
    c = intersect_rays(p1, bis1, p2, bis2)
    
    return c, radius
