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
    Returns True if given value is between minimum and maximum by specified
    tolerance.
    
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
            True if value is between, False otherwise.
    """
    
    return (min_v <= v <= max_v) or equals(v, min_v, epsilon) or equals(v, max_v, epsilon)


def angle(p1, p2, p3):
    """
    Calculates angle between lines p1,p2 and p2,p3.
    
    Args:
        p1: (float, float)
            Point 1 as (x, y) coordinates.
        
        p2: (float, float)
            Point 2 as (x, y) coordinates.
        
        p3: (float, float)
            Point 3 as (x, y) coordinates.
    
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
    
    return numpy.sqrt(dx*dx + dy*dy)


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
