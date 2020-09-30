#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from ..enums import *


def venn(a, b, ab, c=0., ac=0., bc=0., abc=0., mode=VENN_MODE_FULL, spacing=0.1):
    """
    Calculates coordinates and radii for three Venn diagram circles.
    
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
        ((float, float), (float, float), (float, float))
            Center coordinates for individual A, B, C circles.
        
        (float, float, float)
            Radius for individual A, B, C circles.
    """
    
    # calc radii
    r_a = numpy.sqrt((a + ab + ac + abc) / numpy.pi)
    r_b = numpy.sqrt((b + ab + bc + abc) / numpy.pi)
    r_c = numpy.sqrt((c + ac + bc + abc) / numpy.pi)

    # make fully proportional
    if mode == VENN_MODE_FULL:
        
        # calc spacing
        spacing = max(r_a, r_b, r_c) * spacing
        
        # calc distances
        d_ab = calc_distance(r_a, r_b, ab + abc, spacing)
        d_ac = calc_distance(r_a, r_c, ac + abc, spacing)
        d_bc = calc_distance(r_b, r_c, bc + abc, spacing)
    
    # make semi proportional
    elif mode == VENN_MODE_SEMI:
        
        # calc distances
        d_ab = max(r_a, r_b)
        d_ac = max(r_a, r_c)
        d_bc = max(r_b, r_c)
    
    # make non-proportional
    else:
        r_a = r_b = r_c = max(r_a, r_b, r_c)
        d_ab = d_ac = d_bc = r_a
    
    # calc coords of circles center
    coords = calc_coords((r_a, r_b, r_c), (d_ab, d_ac, d_bc))
    
    return coords, (r_a, r_b, r_c)


def calc_bbox(coords, radii):
    """
    Calculates bounding box of given circles. Circles with zero radius are
    excluded.
    
    Args:
        coords: ((float, float), (float, float), (float, float))
            Center coordinates for individual A, B, C circles.
        
        radii: (float, float, float)
            Radius for individual A, B, C circles.
    
    Returns:
        (float, float, float, float)
            Bounding box as top-left corner coordinates, width and height
            (x, y, width, height).
    """
    
    # get non-zero circles
    circles = [(c, r) for c, r in zip(coords, radii) if r > 0]
    
    # get limits
    min_x = min((c[0] - r for c, r in circles))
    max_x = max((c[0] + r for c, r in circles))
    min_y = min((c[1] - r for c, r in circles))
    max_y = max((c[1] + r for c, r in circles))
    
    return min_x, min_y, max_x-min_x, max_y-min_y


def calc_distance(r1, r2, overlap, spacing=0, max_error=0.0001):
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
    min_r = min(r1, r2)
    max_error = overlap * max_error
    
    # no overlap
    if overlap == 0:
        return hi + spacing
    
    # full overlap
    if abs(overlap-numpy.pi*min_r*min_r) <= max_error:
        return 0 if r1 == r2 else lo*(1-numpy.sqrt(max_error))
    
    # find distance
    cycles = 0
    while True:
        
        # update cycle count
        cycles += 1
        
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
        
        # check cycles
        if cycles > 100:
            break
    
    if dist < abs(r1 - r2):
        return abs(r1 - r2)
    
    return dist


def calc_coords(radii, distances):
    """
    Calculates coordinates of the circles centers to achieve specified
    distances. The coordinates are calculated so that the center of resulting
    bounding box is at O,O.
    
    Args:
        radii: (float, float, float)
            Radius for individual A, B, C circles.
        
        distances: (float, float, float)
            Distance between individual AB, AC, BC circles.
    
    Returns:
        ((float, float), (float, float), (float, float))
            Center coordinates for individual A, B, C circles.
    """
    
    # unpack data
    r_a, r_b, r_c = radii
    d_ab, d_ac, d_bc = distances
    order = (0, 1, 2)
    
    # reorder if 1st or 2nd is empty
    if r_a == 0:
        r_a, r_b, r_c = r_b, r_c, r_a
        d_ab, d_ac, d_bc = d_bc, d_ab, d_ac
        order = (2, 0, 1)
    
    elif r_b == 0:
        r_a, r_b, r_c = r_a, r_c, r_b
        d_ab, d_ac, d_bc = d_ac, d_ab, d_bc
        order = (0, 2, 1)
    
    # get intersections
    i_ab = d_ab < r_a + r_b
    i_ac = d_ac < r_a + r_c
    i_bc = d_bc < r_b + r_c
    
    # add 1st and 2nd on line
    a_x, a_y = 0, 0
    b_x, b_y = d_ab, 0
    c_x, c_y = 0, 0
    
    # try if triangle works
    n = 0.5*(d_ab*d_ab + d_ac*d_ac - d_bc*d_bc) / d_ab if d_ab else 0.0
    m = d_ac*d_ac - n*n
    if n != 0 and m > 0:
        c_x = n
        c_y = numpy.sqrt(m)
    
    # AB AC BC
    elif i_ab and i_ac and i_bc:
        c_x = a_x + d_ac
    
    # AB AC
    elif i_ab and i_ac:
        c_x = a_x - d_ac
    
    # AB BC
    elif i_ab and i_bc:
        c_x = b_x + d_bc
    
    # BC AC
    elif i_bc and i_ac:
        a_x = -d_ac
        b_x = d_bc
    
    # AB
    elif i_ab:
        c_x = max(a_x + d_ac, b_x + d_bc)
    
    # AC
    elif i_ac:
        c_x = a_x - d_ac
        b_x = max(a_x + d_ab, c_x + d_bc)
    
    # BC
    elif i_bc:
        c_x = b_x + d_bc
        a_x = min(c_x - d_ac, b_x - d_ab)
    
    # calc offset to bbox center
    min_x, min_y, width, height = calc_bbox(((a_x, a_y), (b_x, b_y), (c_x, c_y)), (r_a, r_b, r_c))
    x_off = a_x - min_x - 0.5*width
    y_off = a_y - min_y - 0.5*height
    
    # apply offset
    centers = (
        (a_x + x_off, a_y + y_off),
        (b_x + x_off, b_y + y_off),
        (c_x + x_off, c_y + y_off))
    
    return centers[order[0]], centers[order[1]], centers[order[2]]


def fit_into(coords, radii, x, y, width, height):
    """
    Recalculates center coordinates and radii to fit circles into given
    rectangle. Circles with zero radius are excluded.
    
    Args:
        coords: ((float, float), (float, float), (float, float))
            Center coordinates for individual A, B, C circles.
        
        radii: (float, float, float)
            Radius for individual A, B, C circles.
        
        x: float
            X coordinate of the top left corner of the rectangle to fit into.
        
        y: float
            Y coordinate of the top left corner of the rectangle to fit into.
        
        width: float
            Width of the rectangle to fit into.
        
        height: float
            Height of the rectangle to fit into.
    
    Returns:
        ((float, float), (float, float), (float, float))
            Recalculated center coordinates for individual A, B, C circles.
        
        (float, float, float)
            Recalculated radius for individual A, B, C circles.
    """
    
    # unpack data
    (ax, ay), (bx, by), (cx, cy) = coords
    r_a, r_b, r_c = radii
    
    # calc scale
    bbox = calc_bbox(coords, radii)
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
    
    return ((ax, ay), (bx, by), (cx, cy)), (r_a, r_b, r_c)
