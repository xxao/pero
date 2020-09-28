#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from ..enums import *


def calc_venn(a, b, ab, c=0., ac=0., bc=0., abc=0., mode=VENN_MODE_FULL, spacing=0.1):
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
        
        mode: str
            Specifies whether circles and overlaps should be proportional to
            their area as any item from the pero.VENN_MODE enum.
                VENN_MODE.NONE - non-proportional
                VENN_MODE.SEMI - circles are proportional but overlaps not
                VENN_MODE.FULL - circles and overlaps try to be proportional
        
        spacing: float
            Relative distance factor used if there is no overlap between the
            circles, calculated from the biggest radius.
    
    Returns:
        (float, float, float)
            Radius for individual circles (A, B, C).
        
        ((float, float), (float, float), (float, float))
            Center coordinates for individual circles (A, B, C).
    """
    
    # make fully proportional
    if mode == VENN_MODE_FULL:
        
        # calc radii
        r_a = numpy.sqrt((a + ab + ac + abc) / numpy.pi)
        r_b = numpy.sqrt((b + ab + bc + abc) / numpy.pi)
        r_c = numpy.sqrt((c + ac + bc + abc) / numpy.pi)
        
        # calc spacing
        spacing = max(r_a, r_b, r_c) * spacing
        
        # calc distances
        d_ab = _calc_distance(r_a, r_b, ab + abc, spacing)
        d_bc = _calc_distance(r_b, r_c, bc + abc, spacing)
        d_ac = _calc_distance(r_a, r_c, ac + abc, spacing)
    
    # make semi proportional
    elif mode == VENN_MODE_SEMI:
        
        # calc radii
        r_a = numpy.sqrt((a + ab + ac + abc) / numpy.pi)
        r_b = numpy.sqrt((b + ab + bc + abc) / numpy.pi)
        r_c = numpy.sqrt((c + ac + bc + abc) / numpy.pi)
        
        # calc distances
        d_ab = max(r_a, r_b) - abs(r_a - r_b)
        d_bc = max(r_b, r_c) - abs(r_b - r_c)
        d_ac = max(r_a, r_c) - abs(r_a - r_c)
    
    # make non-proportional
    else:
        r_a = r_b = r_c = 100
        d_ab = d_bc = d_ac = 100
    
    # calc coords of circles center
    coords = _calc_coords((r_a, r_b, r_c), (d_ab, d_bc, d_ac))
    
    return (r_a, r_b, r_c), coords


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
    bbox = _calc_bbox(radii, coords)
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


def _calc_distance(r1, r2, overlap, spacing=0, max_error=0.0001):
    """
    Calculates distance between two circles to achieve specified overlap area.
    
    Args:
        r1: float
            Radius of first circle.
        
        r2: float
            Radius of second circle.
        
        overlap: float
            Overlap between the circles.
        
        spacing: float
            Additional space between no overlapping circles.
        
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
        return hi + spacing
    
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


def _calc_coords(radii, distances):
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
    r_a, r_b, r_c = radii
    d_ab, d_bc, d_ac = distances
    
    # get intersections
    i_ab = d_ab < r_a + r_b
    i_bc = d_bc < r_b + r_c
    i_ac = d_ac < r_a + r_c
    
    # add A and B on line
    ax = 0
    ay = 0
    bx = d_ab
    by = 0
    
    # init C
    cx = 0
    cy = 0
    
    # try triangle first
    n = 0.5*(d_ac*d_ac - d_bc*d_bc + d_ab*d_ab) / d_ab
    m = d_ac*d_ac - n*n
    if m > 0:
        cx = n
        cy = numpy.sqrt(m)
    
    # AB BC AC
    elif i_ab and i_bc and i_ac:
        cx = ax + d_ac
    
    # AB BC
    elif i_ab and i_bc:
        cx = bx + d_bc
    
    # AB AC
    elif i_ab and i_ac:
        cx = ax - d_ac
    
    # BC AC
    elif i_bc and i_ac:
        ax = -d_ac
        bx = d_bc
    
    # AB
    elif i_ab:
        cx = max(ax + d_ac, bx + d_bc)
    
    # BC
    elif i_bc:
        cx = bx + d_bc
        ax = min(cx - d_ac, bx - d_ab)
    
    # AC
    elif i_ac:
        cx = ax - d_ac
        bx = max(ax + d_ab, cx + d_bc)
    
    # calc offset
    min_x, min_y, width, height = _calc_bbox(radii, ((ax, ay), (bx, by), (cx, cy)))
    x_off = ax - min_x - 0.5*width
    y_off = ay - min_y - 0.5*height
    
    # apply offset
    a = (ax+x_off, ay+y_off)
    b = (bx+x_off, by+y_off)
    c = (cx+x_off, cy+y_off)
    
    return a, b, c


def _calc_bbox(radii, coords):
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
