#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for text bbox calculation."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init glyphs
        label = pero.Text(
            text_bgr_color = "lightgrey",
            font_name = "Arial",
            text_spacing = 0.5,
            text_base = pero.TOP)
        
        rect = pero.Rect(
            line_color = pero.colors.Red.trans(0.5),
            fill_color = None)
        
        middle = pero.Ray(
            line_color = pero.colors.Red.trans(0.5))
        
        # init coords
        x = 20
        y = 20
        padding = 20
        
        # draw texts
        for size in (8, 12, 16, 24):
            
            text = "Normal Size %s" % size
            label.draw(canvas, x=x, y=y, text=text, font_size=size)
            bbox = canvas.get_text_bbox(text, x, y)
            rect.draw(canvas, x=bbox.x, y=bbox.y, width=bbox.width, height=bbox.height)
            middle.draw(canvas, x=bbox.x, y=bbox.y+.5*bbox.height, length=bbox.width)
            
            x += bbox.width + padding
            
            text = "Bold Size %s" % size
            label.draw(canvas, x=x, y=y, text=text, font_size=size, font_weight=pero.BOLD)
            bbox = canvas.get_text_bbox(text, x, y)
            rect.draw(canvas, x=bbox.x, y=bbox.y, width=bbox.width, height=bbox.height)
            middle.draw(canvas, x=bbox.x, y=bbox.y+.5*bbox.height, length=bbox.width)
            
            x += bbox.width + padding
            
            text = "Italic Size %s" % size
            label.draw(canvas, x=x, y=y, text=text, font_size=size, font_style=pero.ITALIC)
            bbox = canvas.get_text_bbox(text, x, y)
            rect.draw(canvas, x=bbox.x, y=bbox.y, width=bbox.width, height=bbox.height)
            middle.draw(canvas, x=bbox.x, y=bbox.y+.5*bbox.height, length=bbox.width)
            
            x = 20
            y += bbox.height + padding
        
        # draw multi-line
        text = "This is some\nmulti-line text\nwithout empty lines."
        label.draw(canvas, x=x, y=y, text=text, font_size=12)
        bbox = canvas.get_text_bbox(text, x, y)
        rect.draw(canvas, x=bbox.x, y=bbox.y, width=bbox.width, height=bbox.height)
        
        x += bbox.width + 20
        
        # draw multi-line with blanks
        text = "\nThis is some\n\nmulti-line text with empty lines."
        label.draw(canvas, x=x, y=y, text=text, font_size=12)
        bbox = canvas.get_text_bbox(text, x, y)
        rect.draw(canvas, x=bbox.x, y=bbox.y, width=bbox.width, height=bbox.height)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Text Bounding Box", 700, 400)
