#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from .. enums import *
from .. properties import *
from .. drawing import Matrix, Path
from . glyph import Glyph


class Text(Glyph):
    """
    Defines a text glyph.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the anchor.
        
        y: int, float or callable
            Specifies the y-coordinate of the anchor.
        
        angle properties:
            Includes pero.AngleProperties to specify the text angle.
        
        text: str, callable, None or UNDEF
            Specifies the text to be drawn.
        
        text properties:
            Includes pero.TextProperties to specify the font.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    angle = Include(AngleProperties)
    
    text = StringProperty(UNDEF)
    font = Include(TextProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        text = self.get_property('text', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # check data
        if not text:
            return
        
        # set text
        canvas.set_text_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_text(text, x, y, angle)


class Textbox(Text):
    """
    Defines a text box glyph.
    
    Properties:
        
        anchor: pero.POSITION_COMPASS or callable
            Specifies the anchor position as any item from the
            pero.POSITION_COMPASS enum. If set to UNDEF, anchor is derived from
            text alignment and baseline.
        
        radius: int, float, (int,), (float,) callable or UNDEF
            Specifies the corner radius as a single value or values for
            individual corners starting from top-left.
        
        padding: int, float, (int,), (float,) callable or UNDEF
            Specifies the inner space as a single value or values for individual
            sides starting from top.
        
        line properties:
            Includes pero.LineProperties to specify the glyph outline.
        
        fill properties:
            Includes pero.FillProperties to specify the glyph fill.
    """
    
    anchor = EnumProperty(UNDEF, enum=POSITION_COMPASS)
    
    radius = QuadProperty(0)
    padding = QuadProperty(5)
    
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw glyph."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        anchor = self.get_property('anchor', source, overrides)
        radius = self.get_property('radius', source, overrides)
        padding = self.get_property('padding', source, overrides)
        text = self.get_property('text', source, overrides)
        align = self.get_property('text_align', source, overrides)
        base = self.get_property('text_base', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # check data
        if not text:
            return
        
        # set text
        canvas.set_text_by(self, source=source, overrides=overrides)
        
        # get size
        padding = padding or (0, 0, 0, 0)
        text_width, text_height = canvas.get_text_size(text)
        bgr_width = text_width + padding[1] + padding[3]
        bgr_height = text_height + padding[0] + padding[2]
        
        # get anchor
        if anchor is UNDEF:
            anchors = set(POSITION_COMPASS)
            
            if align == TEXT_ALIGN_LEFT or align == UNDEF:
                anchors = anchors.intersection(POSITION_COMPASS_LEFT)
            elif align == TEXT_ALIGN_CENTER:
                anchors = anchors.intersection(POSITION_COMPASS_CENTER)
            elif align == TEXT_ALIGN_RIGHT:
                anchors = anchors.intersection(POSITION_COMPASS_RIGHT)
            
            if base == TEXT_BASE_TOP or base == UNDEF:
                anchors = anchors.intersection(POSITION_COMPASS_TOP)
            elif base == TEXT_BASE_MIDDLE:
                anchors = anchors.intersection(POSITION_COMPASS_MIDDLE)
            elif base == TEXT_BASE_BOTTOM:
                anchors = anchors.intersection(POSITION_COMPASS_BOTTOM)
            
            anchor = anchors.pop()
        
        # get background coords
        bgr_x = x
        bgr_y = y
        
        if anchor == POS_N:
            bgr_x -= 0.5 * bgr_width
        elif anchor == POS_NE:
            bgr_x -= bgr_width
        elif anchor == POS_E:
            bgr_x -= bgr_width
            bgr_y -= 0.5 * bgr_height
        elif anchor == POS_SE:
            bgr_x -= bgr_width
            bgr_y -= bgr_height
        elif anchor == POS_S:
            bgr_x -= 0.5 * bgr_width
            bgr_y -= bgr_height
        elif anchor == POS_SW:
            bgr_y -= bgr_height
        elif anchor == POS_W:
            bgr_y -= 0.5 * bgr_height
        elif anchor == POS_C:
            bgr_x -= 0.5 * bgr_width
            bgr_y -= 0.5 * bgr_height
        
        # init text coords
        text_x = bgr_x + padding[3]
        text_y = bgr_y + padding[0]
        
        if align == TEXT_ALIGN_CENTER:
            text_x += 0.5*text_width
        elif align == TEXT_ALIGN_RIGHT:
            text_x += text_width
        
        if base == TEXT_BASE_MIDDLE:
            text_y += 0.5*text_height
        elif base == TEXT_BASE_BOTTOM:
            text_y += text_height
        
        if angle:
            dx = text_x - x
            dy = text_y - y
            text_x = x + dx * math.cos(angle) - dy * math.sin(angle)
            text_y = y + dx * math.sin(angle) + dy * math.cos(angle)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # start drawing group
        canvas.group()
        
        # draw angled rect
        if angle:
            path = Path()
            path.rect(bgr_x, bgr_y, bgr_width, bgr_height, radius)
            path.transform(Matrix().rotate(angle, x, y))
            canvas.draw_path(path)
        
        # strait rectangle
        else:
            canvas.draw_rect(bgr_x, bgr_y, bgr_width, bgr_height, radius)
        
        # draw text
        canvas.draw_text(text, text_x, text_y, angle)
        
        # end drawing group
        canvas.ungroup()
