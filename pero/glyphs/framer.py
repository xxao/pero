#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from . glyph import Glyph


class Framer(Glyph):
    """
    Defines a utility glyph visualizing the details of given rectangle. If the
    'width' or 'height' property is set to pero.UNDEF, corresponding value is
    taken directly from given canvas when drawn.
    
    Properties:
        
        show_label: bool, callable
            Specifies whether label should be shown.
        
        show_size: bool, callable
            Specifies whether width and height should be shown.
        
        x: int, float or callable
            Specifies the x-coordinate of the top-left corner.
        
        y: int, float or callable
            Specifies the y-coordinate of the top-left corner.
        
        width: int, float or callable
            Specifies the width. If not defined, the value is taken
            automatically from given canvas.
        
        height: int, float or callable
            Specifies the height. If not defined, the value is taken
            automatically from given canvas.
        
        line properties:
            Includes pero.LineProperties to specify the path outline.
        
        fill properties:
            Includes pero.FillProperties to specify the path fill.
        
        text properties:
            Includes pero.TextProperties to specify the label properties.
            Some of them (e.g. alignment, angle, baseline) are set automatically
            and cannot be changed.
    """
    
    show_label = BoolProperty(True)
    show_size = BoolProperty(True)
    
    label = StringProperty(UNDEF)
    
    x = NumProperty(0)
    y = NumProperty(0)
    width = NumProperty(UNDEF)
    height = NumProperty(UNDEF)
    
    outline = Include(LineProperties, line_color=None)
    fill = Include(FillProperties, fill_color="#ccc")
    font = Include(TextProperties)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the frame."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        show_label = self.get_property('show_label', source, overrides)
        show_size = self.get_property('show_size', source, overrides)
        label = self.get_property('label', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        
        # get size from canvas
        if width is UNDEF:
            width = canvas.viewport.width - x
        if height is UNDEF:
            height = canvas.viewport.height - y
        
        # get full label
        labels = []
        
        if show_label:
            labels.append("%s" % label)
        if show_size:
            labels.append("%s x %s" % (width, height))
        
        label = "\n".join(labels)
        
        # set text
        canvas.set_text_by(self, source=source, overrides=overrides)
        canvas.text_align = TEXT_ALIGN_CENTER
        canvas.text_base = TEXT_BASE_MIDDLE
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # start drawing group
        canvas.group(tag, "framer")
        
        # draw
        canvas.draw_rect(x, y, width, height)
        canvas.draw_text(label, x+0.5*width, y+0.5*height)
        
        # end drawing group
        canvas.ungroup()
