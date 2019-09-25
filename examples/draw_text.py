#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for text properties drawing."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init glyphs
        line = pero.Line(
            line_width = 1,
            line_color = pero.colors.Red)
        
        label = pero.Text(
            font_size = 12,
            font_name = "Arial")
        
        # init coords
        x = 20
        y = 20
        
        # test family
        label.draw(canvas, x=x, y=y, text="serif", font_family=pero.FONT_FAMILY_SERIF, font_name=pero.UNDEF)
        x += 60
        label.draw(canvas, x=x, y=y, text="sans-serif", font_family=pero.FONT_FAMILY_SANS, font_name=pero.UNDEF)
        x += 60
        label.draw(canvas, x=x, y=y, text="monospace", font_family=pero.FONT_FAMILY_MONO, font_name=pero.UNDEF)
        
        x = 20
        y += 30
        
        # test name
        label.draw(canvas, x=x, y=y, text="arial", font_name='Arial', font_size=12)
        x += 60
        label.draw(canvas, x=x, y=y, text="times", font_name="Times New Roman", font_size=12)
        x += 60
        label.draw(canvas, x=x, y=y, text="courier", font_name="Courier New", font_size=12)
        
        x = 20
        y += 30
        
        # test style
        label.draw(canvas, x=x, y=y, text="normal", font_style=pero.FONT_STYLE_NORMAL)
        x += 60
        label.draw(canvas, x=x, y=y, text="italic", font_style=pero.FONT_STYLE_ITALIC)
        
        x = 20
        y += 30
        
        # test weight
        label.draw(canvas, x=x, y=y, text="normal", font_weight=pero.FONT_WEIGHT_NORMAL)
        x += 60
        label.draw(canvas, x=x, y=y, text="light", font_weight=pero.FONT_WEIGHT_LIGHT)
        x += 60
        label.draw(canvas, x=x, y=y, text="bold", font_weight=pero.FONT_WEIGHT_BOLD)
        
        x = 20
        y += 30
        
        # test size
        label.draw(canvas, x=x, y=y, text="size 10", font_size=10)
        x += 60
        label.draw(canvas, x=x, y=y, text="size 12", font_size=12)
        x += 60
        label.draw(canvas, x=x, y=y, text="size 14", font_size=14)
        
        x = 20
        y += 30
        
        # test color
        label.draw(canvas, x=x, y=y, text="black", text_color=pero.colors.Black, text_bgr_color=None)
        x += 50
        label.draw(canvas, x=x, y=y, text="blue", text_color=pero.colors.Blue, text_bgr_color=None)
        x += 50
        label.draw(canvas, x=x, y=y, text="background", text_color=pero.colors.LightGrey, text_bgr_color=pero.colors.Black)
        
        x = 20
        y += 30
        
        # test alignment
        line.draw(canvas, x1=x, y1=y-5, x2=x, y2=y+17)
        label.draw(canvas, x=x, y=y, text="LEFT", text_align=pero.TEXT_ALIGN_LEFT)
        x += 100
        line.draw(canvas, x1=x, y1=y-5, x2=x, y2=y+17)
        label.draw(canvas, x=x, y=y, text="CENTER", text_align=pero.TEXT_ALIGN_CENTER)
        x += 100
        line.draw(canvas, x1=x, y1=y-5, x2=x, y2=y+17)
        label.draw(canvas, x=x, y=y, text="RIGHT", text_align=pero.TEXT_ALIGN_RIGHT)
        
        x = 20
        y += 50
        
        # test baseline
        line.draw(canvas, x1=x-5, y1=y, x2=x+50, y2=y)
        label.draw(canvas, x=x, y=y, text="TOP", text_base=pero.TEXT_BASE_TOP)
        x += 100
        line.draw(canvas, x1=x-5, y1=y, x2=x+50, y2=y)
        label.draw(canvas, x=x, y=y, text="MIDDLE", text_base=pero.TEXT_BASE_MIDDLE)
        x += 100
        line.draw(canvas, x1=x-5, y1=y, x2=x+55, y2=y)
        label.draw(canvas, x=x, y=y, text="BOTTOM", text_base=pero.TEXT_BASE_BOTTOM)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Text", 350, 280)
