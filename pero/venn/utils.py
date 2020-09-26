#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy


def calc_venn(a, b, ab, c=0., ac=0., bc=0., abc=0., proportional=True):
    """
    Calculates radii and coordinates for three Venn diagram circles.
    
    Args:
        a: float
            Number of items unique to A.
        
        b: float
            Number of items unique to B.
        
        ab: float
            Number of items unique to AB overlap.
        
        c: float
            Number of items unique to C.
        
        ac: float
            Number of items unique to AC overlap.
        
        bc: float
            Number of items unique to BC overlap.
        
        abc: float
            Number of items unique to ABC overlap.
        
        proportional: bool
            Specifies whether circles should be proportional to their area.
    
    Returns:
        (float, float, float)
            Radius for individual circles (A, B, C).
        
        ((float, float), (float, float), (float, float))
            Center coordinates for individual circles (A, B, C).
    """
    
    # make proportional circles
    if proportional:
        
        # calc radii
        r_a = numpy.sqrt((a + ab + ac + abc) / numpy.pi)
        r_b = numpy.sqrt((b + ab + bc + abc) / numpy.pi)
        r_c = numpy.sqrt((c + ac + bc + abc) / numpy.pi)
        
        # calc distances
        d_ab = calc_distance(r_a, r_b, ab + abc)
        d_bc = calc_distance(r_b, r_c, bc + abc)
        d_ac = calc_distance(r_a, r_c, ac + abc)
    
    # make equal circles
    else:
        r_a = r_b = r_c = 100
        d_ab = d_bc = d_ac = 100
    
    # calc coords of circles center
    coords = calc_triangle((r_a, r_b, r_c), (d_ab, d_bc, d_ac))
    
    return (r_a, r_b, r_c), coords


def calc_distance(r1, r2, overlap, zero_spacing=0.1, max_error=0.001):
    """
    Calculates distance between two circles to achieve specified overlap area.
    
    Args:
        r1: float
            Radius of first circle.
        
        r2: float
            Radius of second circle.
        
        overlap: float
            Overlap between the circles.
        
        zero_spacing: float
            Relative distance factor used if there is no overlap between the
            circles, calculated from the biggest radius.
        
        max_error: float
            Maximum allowed relative error of the overlap area.
    
    Returns:
        float
            Distance between the circles.
    """
    
    # get limits
    lo = abs(r1 - r2)
    hi = r1 + r2
    max_error = overlap * max_error
    
    # no overlap
    if overlap == 0:
        return hi + max(r1, r2) * zero_spacing
    
    # find distance
    while True:
        
        # halve the distance
        dist = 0.5 * (lo + hi)
        
        # calc arc angles
        angle1 = 2 * numpy.arccos((dist*dist + r1*r1 - r2*r2) / (2 * dist * r1))
        angle2 = 2 * numpy.arccos((dist*dist + r2*r2 - r1*r1) / (2 * dist * r2))
        
        # calc overlap area
        area1 = 0.5 * r1*r1 * (angle1 - numpy.sin(angle1))
        area2 = 0.5 * r2*r2 * (angle2 - numpy.sin(angle2))
        error = area1 + area2 - overlap
        
        # error good enough
        if abs(error) <= max_error:
            break
        
        # update distance range
        if error > 0:
            lo = dist
        elif error < 0:
            hi = dist
    
    if dist < abs(r1 - r2):
        return abs(r1 - r2)
    
    return dist


def calc_triangle(radii, distances):
    """
    Calculates coordinates of the circles centers to achieve specified
    distances. The coordinates are calculated so that the center of resulting
    bounding box is at O,O. The first two circles are in line, the third
    is positioned below.
    
    Args:
        radii: (float, float, float)
            Radius for each of the three circles.
        
        distances: (float, float, float)
            Distances between the circles as (AB, BC, AC).
    
    Returns:
        ((float, float), (float, float), (float, float))
            XY coordinates of the circles centers.
    """
    
    # unpack data
    d_ab, d_bc, d_ac = distances
    
    # calc triangle zeroed on center of A
    ax = ay = by = 0
    bx = d_ab
    cx = 0.5*(d_ac*d_ac - d_bc*d_bc + d_ab*d_ab) / d_ab
    cy = numpy.sqrt(d_ac*d_ac - cx*cx)
    
    # calc offset
    min_x, min_y, width, height = calc_bbox(radii, ((ax, ay), (bx, by), (cx, cy)))
    x_off = ax - min_x - 0.5*width
    y_off = ay - min_y - 0.5*height
    
    return (ax+x_off, ay+y_off), (bx+x_off, by+y_off), (cx+x_off, cy+y_off)


def calc_intersections(c1, r1, c2, r2):
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
            there is no overlap.
    """
    
    # calc distance
    dx = c2[0] - c1[0]
    dy = c2[1] - c1[1]
    dist = numpy.sqrt(dx*dx + dy*dy)
    
    # non intersecting
    if dist > r1 + r2:
        return None
    
    # one inside another
    if dist < abs(r1-r2):
        return None
    
    # coincident circles
    if dist == 0 and r1 == r2:
        return None
    
    # calc intersections
    a = (r1**2 - r2**2 + dist**2) / (2*dist)
    h = numpy.sqrt(r1**2 - a**2)
    
    x = c1[0] + a*dx / dist
    y = c1[1] + a*dy / dist
    
    x1 = x + h*dy / dist
    y1 = y - h*dx / dist
    x2 = x - h*dy / dist
    y2 = y + h*dx / dist
    
    return (x1, y1), (x2, y2)


def calc_bbox(radii, coords):
    """
    Calculates bounding box of three given circles.
    
    Args:
        radii: (float, float, float)
            Radius for each of the three circles.
        
        coords: ((float, float), (float, float), (float, float))
            XY coordinates of the circles centers.
    
    Returns:
        (float, float, float, float)
            Bounding box as top-left corner coordinates, width and height
            (x, y, width, height).
    """
    
    # unpack data
    r_a, r_b, r_c = radii
    (ax, ay), (bx, by), (cx, cy) = coords
    
    # get limits
    min_x = min(ax-r_a, bx-r_b, cx-r_c)
    max_x = max(ax+r_a, bx+r_b, cx+r_c)
    min_y = min(ay-r_a, by-r_b, cy-r_c)
    max_y = max(ay+r_a, by+r_b, cy+r_c)
    
    return min_x, min_y, max_x-min_x, max_y-min_y


def fit_into(radii, coords, x, y, width, height):
    """
    Recalculates center coordinates to fit three circles into given rectangle.
    
    Args:
        radii: (float, float, float)
            Radius for each of the three circles.
        
        coords: ((float, float), (float, float), (float, float))
            XY coordinates of the circles centers.
        
        x: float
            X coordinate of the top left corner of the rectangle to fit into.
        
        y: float
            Y coordinate of the top left corner of the rectangle to fit into.
        
        width: float
            Width of the rectangle to fit into.
        
        height: float
            Height of the rectangle to fit into.
    
    Returns:
        (float, float, float)
            Recalculated radius for individual circles.
        
        ((float, float), (float, float), (float, float))
            Recalculated center coordinates for individual circles.
    """
    
    # unpack data
    r_a, r_b, r_c = radii
    (ax, ay), (bx, by), (cx, cy) = coords
    
    # calc scale
    bbox = calc_bbox(radii, coords)
    scale = min(width / bbox[2], height / bbox[3])
    
    # calc shift
    x_off = x+0.5*width
    y_off = y+0.5*height
    
    # apply to radii
    r_a *= scale
    r_b *= scale
    r_c *= scale
    
    # apply to coords
    ax = ax*scale + x_off
    ay = ay*scale + y_off
    bx = bx*scale + x_off
    by = by*scale + y_off
    cx = cx*scale + x_off
    cy = cy*scale + y_off
    
    return (r_a, r_b, r_c), ((ax, ay), (bx, by), (cx, cy))
