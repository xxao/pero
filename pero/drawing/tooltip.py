#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import modules
from ..enums import *
from ..properties import *
from .frame import FrameProperty
from .glyphs import Glyph, Textbox


class Tooltip(Glyph):
    """
    Provides a base class for tooltip drawing.
    
    Properties:
        
        x: int, float or callable
            Specifies the x-coordinate of the anchor.
        
        y: int, float or callable
            Specifies the y-coordinate of the anchor.
        
        x_offset: int, float or callable
            Specifies the x-axis shift from the anchor.
        
        y_offset: int, float or callable
            Specifies the y-axis shift from the anchor.
        
        clip: pero.Frame, callable, None or UNDEF
            Specifies the available drawing frame.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    
    x_offset = NumProperty(6)
    y_offset = NumProperty(6)
    
    clip = FrameProperty(UNDEF)


class TextTooltip(Tooltip):
    """
    Provides a basic glyph to draw simple text tooltip.
    
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
    
    textbox = Include(Textbox, exclude=['angle'], line_color="#ccce", fill_color="#eeee", radius=4, padding=(3, 5))
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of TextTooltip."""
        
        super(Tooltip, self).__init__(**overrides)
        
        # init text box
        self._textbox = Textbox()
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw tooltip."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        x_offset = self.get_property('x_offset', source, overrides)
        y_offset = self.get_property('y_offset', source, overrides)
        text = self.get_property('text', source, overrides)
        padding = self.get_property('padding', source, overrides)
        clip = self.get_property('clip', source, overrides)
        
        # check data
        if not text:
            return
        
        # set text
        canvas.set_text_by(self, source=source, overrides=overrides)
        
        # get tooltip size
        text_width, text_height = canvas.get_text_size(text)
        bgr_width = text_width + padding[1] + padding[3]
        bgr_height = text_height + padding[0] + padding[2]
        
        # calc origin
        x = x - bgr_width - x_offset
        y = y - bgr_height - y_offset
        
        # check clipping frame
        if clip:
            
            # shift right if outside
            if x < clip.x1:
                x += 2*x_offset + bgr_width
            
            # shift bottom if outside
            if y < clip.y1:
                y += 2*y_offset + bgr_height
        
        # set glyph properties
        self._textbox.set_properties_from(self, source=source, overrides=overrides)
        
        # draw glyph
        self._textbox.draw(canvas,
            x = x,
            y = y,
            text_align = TEXT_ALIGN.LEFT,
            text_base = TEXT_BASELINE.TOP,
            angle = 0)
