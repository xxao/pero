#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
from ..enums import *
from ..properties import *
from .graphics import OutGraphics


class Title(OutGraphics):
    """
    Title provides a simple drawing mechanism to include a title to the plot.
    
    Properties:
        
        text: str, None or UNDEF
            Specifies the text to show.
        
        text properties:
            Includes pero.TextProperties to specify the text properties.
    """
    
    text = StringProperty(UNDEF, dynamic=False)
    font = Include(TextProperties, dynamic=False, font_size=12, font_weight=BOLD, text_align=CENTER)
    
    
    def get_extent(self, canvas):
        """
        This method is automatically called by parent plot to get amount of
        logical space needed to draw the object.
        """
        
        # get text
        text = self.get_property('text', None, None)
        if not text:
            return 0
        
        # set text
        canvas.set_text_by(self)
        
        # get size
        return canvas.get_text_size(text)[1]
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the title."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        position = self.get_property('position', source, overrides)
        align = self.get_property('text_align', source, overrides)
        text = self.get_property('text', source, overrides)
        
        # check data
        if not text:
            return
        
        # set text
        canvas.set_text_by(self, source=source, overrides=overrides)
        
        # get coords
        angle = 0
        x, y, width, height = frame.rect
        
        if position in (TOP, BOTTOM):
            angle = 0
            y += 0.5*height
            
            if align == CENTER:
                x += 0.5*width
            elif align == RIGHT:
                x += width
        
        elif position == LEFT:
            angle = -0.5*math.pi
            x += 0.5*width
            
            if align == CENTER:
                y += 0.5*height
            elif align == LEFT:
                y += height
        
        elif position == RIGHT:
            angle = 0.5*math.pi
            x += 0.5*width
            
            if align == CENTER:
                y += 0.5*height
            elif align == RIGHT:
                y += height
        
        # draw text
        canvas.text_base = MIDDLE
        canvas.draw_text(text, x, y, angle=angle)
