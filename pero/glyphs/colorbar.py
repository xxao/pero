#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from . glyph import Glyph


class ColorBar(Glyph):
    """
    Color bar provides a simple tool to visualize a color gradient range. It is
    typically used together with an axis as part of a plot.
    
    By default the gradient direction goes the same ways as device units, i.e.
    from left to right and from top to bottom. This behavior can be changed by
    setting the 'reverse' property to True.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the top-left corner.
        
        y: int, float or callable
            Specifies the y-coordinate of the top-left corner.
        
        length: int, float or callable
            Specifies the bar length.
        
        thickness: int, float or callable
            Specifies the bar thickness.
        
        orientation: pero.ORIENTATION or callable
            Specifies the bar orientation as any item from the
            pero.ORIENTATION enum.
        
        reverse: bool or callable
            Specifies whether the gradient is drawn considering the top/left
            side (False) or the bottom/right side (True) as its start.
        
        gradient: pero.Gradient, pero.Palette, tuple, str or callable
            Specifies the color gradient as a sequence of colors,
            pero.Palette, palette name or pero.Gradient.
        
        steps: int or callable
            Specifies the number of color steps to use to draw the gradient.
        
        line properties:
            Includes pero.LineProperties to specify the outline.
        
        fill properties:
            Includes pero.FillProperties to specify the background fill.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    length = NumProperty(0)
    thickness = NumProperty(7)
    orientation = EnumProperty(ORI_HORIZONTAL, enum=ORIENTATION)
    reverse = BoolProperty(False)
    
    gradient = GradientProperty(UNDEF)
    steps = NumProperty(128)
    
    line = Include(LineProperties, line_color="#000")
    fill = Include(FillProperties, fill_color=UNDEF)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the bar."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        length = self.get_property('length', source, overrides)
        thickness = self.get_property('thickness', source, overrides)
        orientation = self.get_property('orientation', source, overrides)
        reverse = self.get_property('reverse', source, overrides)
        gradient = self.get_property('gradient', source, overrides)
        steps = self.get_property('steps', source, overrides)
        
        # get step size
        step = float(length) / steps
        
        # get direction
        direction = 1 if reverse else 0
        
        # get gradient values
        start = gradient.stops[0]
        grange = gradient.stops[-1] - start
        
        # get coords
        if orientation == ORI_HORIZONTAL:
            width = length
            height = thickness
            step_width = step
            step_height = thickness
            step_x = step
            step_y = 0
            
        else:
            width = thickness
            height = length
            step_width = thickness
            step_height = step
            step_x = 0
            step_y = step
        
        # start drawing group
        canvas.group(tag, "colorbar")
        
        # set pen and brush for background
        canvas.line_width = 0
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw background
        canvas.draw_rect(x, y, width, height)
        
        # draw gradient
        for i in range(steps):
            value = start + grange * abs(direction-float(i)/steps)
            canvas.fill_color = gradient.color_at(value)
            canvas.draw_rect(x+i*step_x, y+i*step_y, step_width, step_height)
        
        # set pen and brush for outline
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_color = None
        
        # draw outline
        canvas.draw_rect(x, y, width, height)
        
        # end drawing group
        canvas.ungroup()
