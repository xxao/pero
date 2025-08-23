#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from . import utils
from ..enums import *
from .path import Path
from .matrix import Matrix


def make_arc(x, y, radius, start_angle, end_angle, clockwise=True, fill_rule=EVENODD):
    """
    Creates an arc path.
    
    Args:
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        radius: int or float
            Radius of the arc.
        
        start_angle: float
            Start angle in radians.
        
        end_angle: float
            End angle in radians.
        
        clockwise: bool
            Specifies the direction of drawing. If set to True, the arc
            will be drawn in the clockwise direction.
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Arc path.
    """
    
    # make path
    path = Path(fill_rule)
    path.arc(x, y, radius, start_angle, end_angle, clockwise)
    
    return path


def make_circle(x, y, radius, fill_rule=EVENODD):
    """
    Creates a circle path.
    
    Args:
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        radius: int or float
            Radius of the circle.
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Circle path.
    """
    
    # make path
    path = Path(fill_rule)
    path.circle(x, y, radius)
    
    return path


def make_ellipse(x, y, width, height, fill_rule=EVENODD):
    """
    Creates an ellipse path.
    
    Args:
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        width: int or float
            Full width of the ellipse.
        
        height: int or float
            Full height of the ellipse.
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Ellipse path.
    """
    
    # make path
    path = Path(fill_rule)
    path.ellipse(x, y, width, height)
    
    return path


def make_rect(x, y, width, height, radius=0, fill_rule=EVENODD):
    """
    Creates a rectangle path.
    
    Args:
        x: int or float
            X-coordinate of the top left corner.
        
        y: int or float
            Y-coordinate of the top left corner.
        
        width: int or float
            Full rectangle width.
        
        height: int or float
            Full rectangle height.
        
        radius: int or float or collection of four int/float
            Radius of the corners as a single value or separate value for
            each corner individually, starting top-left.
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Rectangle path.
    """
    
    # make path
    path = Path(fill_rule)
    path.rect(x, y, width, height, radius)
    
    return path


def make_polygon(points, fill_rule=EVENODD):
    """
    Creates a closed polygon path.
    
    Args:
        points: list of (float, float)
            Collection of x,y coordinates of the points.
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Polygon path.
    """
    
    # make path
    path = Path(fill_rule)
    path.polygon(points)
    
    return path


def make_ngon(sides, x=0, y=0, radius=.5, angle=0, fill_rule=EVENODD):
    """
    Creates a closed symmetrical polygon path.
    
    Args:
        sides: int
            Number of sides/vertices.
        
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        radius: int or float
            Radius of the polygon.
        
        angle: float
            Angle in radians.
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            N-gon path.
    """
    
    # calc vertices
    theta = (PI2X / sides * numpy.arange(sides + 1)) - PI / 2.0
    r = numpy.full(sides + 1, radius, dtype=float)
    
    vertices = numpy.stack((r * numpy.cos(theta), r * numpy.sin(theta)), axis=1)
    vertices += numpy.array((x, y))
    
    # make path
    path = Path(fill_rule)
    path.polygon(vertices[:-1])
    
    # apply angle
    if angle:
        matrix = Matrix().rotate(angle, x=x, y=y)
        path.transform(matrix)
    
    return path


def make_star(rays, x=0, y=0, outer_radius=.5, inner_radius=.25, angle=0, fill_rule=EVENODD):
    """
    Creates a closed star-like path.
    
    Args:
        rays: int
            Number of rays.
        
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        outer_radius: int or float
            Outer radius of the rays.
        
        inner_radius: int or float
            Inner radius of the rays.
        
        angle: float
            Angle in radians.
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Star path.
    """
    
    # calc vertices
    sides = rays * 2
    theta = (PI2X / sides * numpy.arange(sides + 1)) - PI / 2.0
    
    r = numpy.full(sides + 1, outer_radius, dtype=float)
    r[1::2] = inner_radius
    
    vertices = numpy.stack((r * numpy.cos(theta), r * numpy.sin(theta)), axis=1)
    vertices += numpy.array((x, y))
    
    # make path
    path = Path(fill_rule)
    path.polygon(vertices[:-1])
    
    # apply angle
    if angle:
        matrix = Matrix().rotate(angle, x=x, y=y)
        path.transform(matrix)
    
    return path


def make_wedge(x, y, inner_radius, outer_radius, start_angle, end_angle, clockwise=True, corners=None, caped=False):
    """
    Creates a wedge path. Unlike the others, this function automatically
    decides what kind of wedge should be created based on given parameters.
    It is recommended to always use this method instead of specific ones.
    
    Args:
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        inner_radius: int, float or callable
            Inner radius.
        
        outer_radius: int, float or callable
            Outer radius.
        
        start_angle: float
            Start angle in radians.
        
        end_angle: float
            End angle in radians.
        
        clockwise: bool
            Specifies the direction of drawing. If set to True, the wedge
            will be drawn in the clockwise direction.
        
        corners: (float, float, float, float)
            Radii for individual corners as (outer-start, outer-end, inner-end, inner-start).
        
        caped: bool
            Specifies the wedge ends style. If set to True and no specific corners
            provided, the ends will be circular. This only applies to donut-like wedges.
    
    Returns:
        pero.Path
            Wedge path.
    """
    
    # empty
    if start_angle == end_angle:
        path = Path()
        return path
    
    # normalize angles
    start_angle = start_angle % PI2X
    end_angle = end_angle % PI2X
    
    # circle or annulus
    if start_angle == end_angle:
        return make_annulus(x, y, inner_radius, outer_radius)
    
    # prepare corners
    if isinstance(corners, (int, float)):
        corners = 4 * [corners]
    
    # pie wedge rounded
    if not inner_radius and corners:
        return make_pie_rounded(x, y, outer_radius, start_angle, end_angle, clockwise, corners[:3])
    
    # pie wedge sharp
    if not inner_radius:
        return make_pie(x, y, outer_radius, start_angle, end_angle, clockwise)
    
    # donut wedge rounded
    if corners:
        return make_donut_rounded(x, y, inner_radius, outer_radius, start_angle, end_angle, clockwise, corners)
    
    # donut wedge caped
    if caped:
        return make_donut_caped(x, y, inner_radius, outer_radius, start_angle, end_angle, clockwise)
    
    # donut wedge sharp
    return make_donut(x, y, inner_radius, outer_radius, start_angle, end_angle, clockwise)


def make_annulus(x, y, inner_radius, outer_radius):
    """
    Creates an annulus path.
    
    Args:
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        inner_radius: int, float or callable
            Inner radius.
        
        outer_radius: int, float or callable
            Outer radius.
    
    Returns:
        pero.Path
            Annulus path.
    """
    
    # create path
    path = Path(EVENODD)
    path.circle(x, y, outer_radius)
    if inner_radius:
        path.circle(x, y, inner_radius)
    
    return path


def make_donut(x, y, inner_radius, outer_radius, start_angle, end_angle, clockwise, fill_rule=EVENODD):
    """
    Creates a donut wedge path.
    
    Args:
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        inner_radius: int, float or callable
            Inner radius.
        
        outer_radius: int, float or callable
            Outer radius.
        
        start_angle: float
            Start angle in radians.
        
        end_angle: float
            End angle in radians.
        
        clockwise: bool
            Specifies the direction of drawing. If set to True, the wedge
            will be drawn in the clockwise direction.
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Donut wedge path.
    """
    
    # get inner end point
    iep = utils.ray((x, y), end_angle, inner_radius)
    
    # create path
    path = Path(fill_rule)
    path.arc(x, y, outer_radius, start_angle, end_angle, clockwise)
    path.line_to(*iep)
    path.arc_around(x, y, start_angle, not clockwise)
    path.close()
    
    return path


def make_donut_rounded(x, y, inner_radius, outer_radius, start_angle, end_angle, clockwise, corners, fill_rule=WINDING):
    """
    Creates a donut wedge path with rounded corners.
    
    Args:
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        inner_radius: int, float or callable
            Inner radius.
        
        outer_radius: int, float or callable
            Outer radius.
        
        start_angle: float
            Start angle in radians.
        
        end_angle: float
            End angle in radians.
        
        clockwise: bool
            Specifies the direction of drawing. If set to True, the wedge
            will be drawn in the clockwise direction.
        
        corners: (float, float, float, float)
            Radii for individual corners as (outer-start, outer-end, inner-end, inner-start).
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Donut wedge path.
    """
    
    # get corners
    r1, r2, r3, r4 = corners
    
    # get direction
    direction = 1 if clockwise else -1
    
    # get central points
    cr = inner_radius + 0.5 * (outer_radius - inner_radius)
    rsp = utils.ray((x, y), start_angle, cr)
    rep = utils.ray((x, y), end_angle, cr)
    
    # get outer start points
    angle = numpy.atan(r1 / cr)
    start_angle_os = start_angle + direction * angle
    osp = utils.ray((x, y), start_angle_os, outer_radius)
    osc = utils.ray(osp, start_angle_os - direction * PI2, r1)
    
    # get outer end points
    angle = numpy.atan(r2 / cr)
    end_angle_os = end_angle - direction * angle
    oep = utils.ray((x, y), end_angle_os, outer_radius)
    oec = utils.ray(oep, end_angle_os + direction * PI2, r2)
    
    # get inner end points
    angle = numpy.atan(r3 / cr)
    end_angle_is = end_angle - direction * angle
    iep = utils.ray((x, y), end_angle_is, inner_radius)
    iec = utils.ray(iep, end_angle_is + direction * PI2, r3)
    
    # get inner start points
    angle = numpy.atan(r4 / cr)
    start_angle_is = start_angle + direction * angle
    isp = utils.ray((x, y), start_angle_is, inner_radius)
    isc = utils.ray(isp, start_angle_is - direction * PI2, r4)
    
    # create rounded wedge
    path = Path(fill_rule)
    path.move_to(*rsp)
    path.arc_to(*osc, *osp, r1)
    path.arc_around(x, y, end_angle_os, clockwise)
    path.arc_to(*oec, *rep, r2)
    path.arc_to(*iec, *iep, r3)
    path.arc_around(x, y, start_angle_is, not clockwise)
    path.arc_to(*isc, *rsp, r4)
    path.close()
    
    return path


def make_donut_caped(x, y, inner_radius, outer_radius, start_angle, end_angle, clockwise, fill_rule=WINDING):
    """
    Creates a donut wedge path with circular ends.
    
    Args:
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        inner_radius: int, float or callable
            Inner radius.
        
        outer_radius: int, float or callable
            Outer radius.
        
        start_angle: float
            Start angle in radians.
        
        end_angle: float
            End angle in radians.
        
        clockwise: bool
            Specifies the direction of drawing. If set to True, the wedge
            will be drawn in the clockwise direction.
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Donut wedge path.
    """
    
    # get direction
    direction = 1 if clockwise else -1
    
    # calc shrink
    r = 0.5 * (outer_radius - inner_radius)
    cr = inner_radius + 0.5 * (outer_radius - inner_radius)
    shrink = numpy.atan(r / cr)
    
    # shrink angles
    start_angle_s = (start_angle + direction * shrink) % PI2X
    end_angle_s = (end_angle - direction * shrink) % PI2X
    
    # get control points
    start = utils.ray((x, y), start_angle_s, outer_radius)
    start_center = utils.ray((x, y), start_angle_s, cr)
    end_center = utils.ray((x, y), end_angle_s, cr)
    
    # make circle if too small
    diff = utils.angle_difference(start_angle, end_angle, clockwise)
    if abs(diff) <= abs(2 * shrink):
        path = Path(fill_rule)
        path.circle(*start_center, r)
        return path
    
    # create rounded wedge
    path = Path(fill_rule)
    path.move_to(*start)
    path.arc_around(x, y, end_angle_s, clockwise)
    path.arc_around(*end_center, end_angle_s - PI, clockwise)
    path.arc_around(x, y, start_angle_s, not clockwise)
    path.arc_around(*start_center, start_angle_s, clockwise)
    path.close()
    
    return path


def make_pie(x, y, radius, start_angle, end_angle, clockwise, fill_rule=EVENODD):
    """
    Makes pie wedge path.
    
    Args:
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        radius: int, float or callable
            Outer radius.
        
        start_angle: float
            Start angle in radians.
        
        end_angle: float
            End angle in radians.
        
        clockwise: bool
            Specifies the direction of drawing. If set to True, the wedge
            will be drawn in the clockwise direction.
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Pie wedge path.
    """
    
    # create path
    path = Path(fill_rule)
    path.arc(x, y, radius, start_angle, end_angle, clockwise)
    path.line_to(x, y)
    path.close()
    
    return path


def make_pie_rounded(x, y, radius, start_angle, end_angle, clockwise, corners, fill_rule=EVENODD):
    """
    Makes pie wedge path with rounded corners.
    
    Args:
        x: int or float
            X-coordinate of the center.
        
        y: int or float
            Y-coordinate of the center.
        
        radius: int, float or callable
            Outer radius.
        
        start_angle: float
            Start angle in radians.
        
        end_angle: float
            End angle in radians.
        
        clockwise: bool
            Specifies the direction of drawing. If set to True, the wedge
            will be drawn in the clockwise direction.
        
        corners: (float, float, float)
            Radii for individual corners (outer-start, outer-end, center).
        
        fill_rule: pero.FILL_RULE
            Specifies the fill rule to be used for drawing as a value from
            pero.FILL_RULE enum.
    
    Returns:
        pero.Path
            Pie wedge path.
    """
    
    # get corners
    r1, r2, r3 = corners
    
    # get direction
    direction = 1 if clockwise else -1
    
    # create start points
    angle = numpy.atan(r1 / radius)
    start_angle_s = start_angle + direction * angle
    osp = utils.ray((x, y), start_angle_s, radius)
    osc = utils.ray(osp, start_angle_s - direction * PI2, r1)
    
    # create end points
    angle = numpy.atan(r2 / radius)
    end_angle_s = end_angle - direction * angle
    oep = utils.ray((x, y), end_angle_s, radius)
    oec = utils.ray(oep, end_angle_s + direction * PI2, r2)
    
    # create path
    path = Path(fill_rule)
    path.move_to(x, y)
    path.arc_to(*osc, *osp, r1, before=False)
    path.arc_around(x, y, end_angle_s, clockwise)
    path.arc_to(*oec, x, y, r2)
    path.arc_to(x, y, *osc, r3)
    path.close()
    
    return path
