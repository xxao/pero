#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. drawing import FrameProperty
from . glyph import Glyph


class Tooltip(Glyph):
    """
    Provides a base class for tooltip drawing.
    
    The pero.Tooltip classes can be used directly to draw tooltip or as
    descriptor to create a pero.Tooltip instances from real data and using the
    'clone' method and a data source.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the anchor.
        
        y: int, float or callable
            Specifies the y-coordinate of the anchor.
        
        x_offset: int, float or callable
            Specifies the x-axis shift from the anchor.
        
        y_offset: int, float or callable
            Specifies the y-axis shift from the anchor.
        
        anchor: pero.POSITION_COMPASS or callable
            Specifies the anchor position as any item from the
            pero.POSITION_COMPASS enum.
        
        clip: pero.Frame, callable, None or UNDEF
            Specifies the available drawing frame.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    
    x_offset = NumProperty(10)
    y_offset = NumProperty(10)
    
    anchor = EnumProperty(UNDEF, enum=POSITION_COMPASS)
    clip = FrameProperty(UNDEF)


class TextTooltip(Tooltip):
    """
    Provides a basic glyph to draw simple text box tooltip.
    
    Properties:
        
        text: str, callable, None or UNDEF
            Specifies the text to be drawn.
        
        text properties:
            Includes pero.TextProperties to specify the text properties. Some
            of them (e.g. alignment, angle, baseline) are set automatically.
        
        radius: int, float, tuple, callable or UNDEF
            Specifies the corner radius of the box as a single value or values
            for individual corners starting from top-left.
        
        padding: int, float, tuple, callable or UNDEF
            Specifies the inner space of the box as a single value or values for
            individual sides starting from top.
        
        line properties:
            Includes pero.LineProperties to specify the box outline.
        
        fill properties:
            Includes pero.FillProperties to specify the box fill.
    """
    
    text = StringProperty(UNDEF)
    
    font = Include(TextProperties)
    
    radius = QuadProperty(3)
    padding = QuadProperty(5)
    
    line = Include(LineProperties, line_color="#ccce")
    fill = Include(FillProperties, fill_color="#eeee")
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw tooltip."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        anchor = self.get_property('anchor', source, overrides)
        x_offset = self.get_property('x_offset', source, overrides)
        y_offset = self.get_property('y_offset', source, overrides)
        radius = self.get_property('radius', source, overrides)
        padding = self.get_property('padding', source, overrides)
        text = self.get_property('text', source, overrides)
        align = self.get_property('text_align', source, overrides)
        base = self.get_property('text_base', source, overrides)
        clip = self.get_property('clip', source, overrides)
        
        # check text
        if not text:
            return
        
        # set text
        canvas.set_text_by(self, source=source, overrides=overrides)
        
        # get size
        padding = padding or (0, 0, 0, 0)
        text_width, text_height = canvas.get_text_size(text)
        bgr_width = text_width + padding[1] + padding[3]
        bgr_height = text_height + padding[0] + padding[2]
        
        # shift anchor
        if anchor == POS_N:
            x -= 0.5 * bgr_width
        elif anchor == POS_NE:
            x -= bgr_width
        elif anchor == POS_E:
            x -= bgr_width
            y -= 0.5 * bgr_height
        elif anchor == POS_SE:
            x -= bgr_width
            y -= bgr_height
        elif anchor == POS_S:
            x -= 0.5 * bgr_width
            y -= bgr_height
        elif anchor == POS_SW:
            y -= bgr_height
        elif anchor == POS_W:
            y -= 0.5 * bgr_height
        elif anchor == POS_C:
            x -= 0.5 * bgr_width
            y -= 0.5 * bgr_height
        
        # apply offset
        x += x_offset
        y += y_offset
        
        # check clipping frame
        if clip:
            
            # shift horizontally if outside
            if x < clip.x1:
                x += 2*x_offset + bgr_width
            elif x + bgr_width > clip.x2 and x > clip.cx:
                x -= 2*x_offset + bgr_width
            
            # shift vertically if outside
            if y < clip.y1:
                y += 2*y_offset + bgr_height
            elif y + bgr_height > clip.y2 and y > clip.cy:
                y -= 2*y_offset + bgr_height
        
        # get text coords
        text_x = x + padding[3]
        text_y = y + padding[0]
        
        if align == TEXT_ALIGN_CENTER:
            text_x += 0.5*text_width
        elif align == TEXT_ALIGN_RIGHT:
            text_x += text_width
        
        if base == TEXT_BASE_MIDDLE:
            text_y += 0.5*text_height
        elif base == TEXT_BASE_BOTTOM:
            text_y += text_height
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # start drawing group
        canvas.group(tag, "tooltip")
        
        # draw background
        canvas.draw_rect(x, y, bgr_width, bgr_height, radius)
        
        # draw text
        canvas.draw_text(text, text_x, text_y)
        
        # end drawing group
        canvas.ungroup()
