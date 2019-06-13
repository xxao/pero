#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for text properties drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.font_scale = 1.5
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init glyphs
        origin = pero.Plus(
            size = 20,
            line_width = 1,
            line_color = pero.colors.Red)
        
        label = pero.Text(
            angle = pero.rads(20),
            font_size = 12,
            font_name = "Arial",
            text_spacing = .5,
            text_bgr_color = pero.colors.Grey.opaque(.3))
        
        rect = pero.Rect(
            line_color = pero.colors.Green,
            fill_color = None)
        
        # init coords
        padding = 40
        
        # test alignment and baseline
        y = padding
        for base in (pero.TOP, pero.MIDDLE, pero.BOTTOM):
            
            x = padding
            for align in (pero.LEFT, pero.CENTER, pero.RIGHT):
                
                text = "%s\n%s" % (base.upper(), align.upper())
                label.draw(canvas, x=x, y=y, text=text, text_align=align, text_base=base)
                
                bbox = canvas.get_text_bbox(text, x, y, label.angle)
                rect.draw(canvas, x=bbox.x, y=bbox.y, width=bbox.width, height=bbox.height)
                
                origin.draw(canvas, x=x, y=y)
                
                x += 250/canvas.line_scale
            y += 150/canvas.line_scale


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Text", 700, 370)
