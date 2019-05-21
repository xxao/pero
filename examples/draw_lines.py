#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for profile drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # calc coordinates
        padding = 30
        margin = 60
        width, height = canvas.viewport.wh
        x1 = padding
        x2 = width - padding
        y = padding
        
        # init glyphs
        label = pero.Text()
        
        pather = pero.Pather(
            line_width = 15,
            line_cap = pero.BUTT,
            fill_color = None,
            anchor_size = 6,
            anchor_fill_color = pero.colors.Red,
            cursor = None)
        
        line = pero.Line(
            line_color = pero.colors.Black,
            line_width = 5,
            line_cap = pero.BUTT,
            line_join = pero.MITER)
        
        # draw line caps
        x = x1
        path = pero.Path().line_to(80, 0)
        
        mat = pero.Matrix().translate(x, y)
        pather.draw(canvas, path=path.transformed(mat), line_cap=pero.BUTT)
        label.draw(canvas, x=x, y=y+15, text="Butt")
        
        x += 120
        mat = pero.Matrix().translate(x, y)
        pather.draw(canvas, path=path.transformed(mat), line_cap=pero.ROUND)
        label.draw(canvas, x=x, y=y+15, text="Round")
        
        x += 120
        mat = pero.Matrix().translate(x, y)
        pather.draw(canvas, path=path.transformed(mat), line_cap=pero.SQUARE)
        label.draw(canvas, x=x, y=y+15, text="Square")
        
        y += margin + 50
        
        # draw line join
        x = x1
        path = pero.Path().line_to(40, -60).line_to(80, 0)
        
        mat = pero.Matrix().translate(x, y)
        pather.draw(canvas, path=path.transformed(mat), line_join=pero.MITER)
        label.draw(canvas, x=x, y=y+15, text="Miter")
        
        x += 120
        mat = pero.Matrix().translate(x, y)
        pather.draw(canvas, path=path.transformed(mat), line_join=pero.ROUND)
        label.draw(canvas, x=x, y=y+15, text="Round")
        
        x += 120
        mat = pero.Matrix().translate(x, y)
        pather.draw(canvas, path=path.transformed(mat), line_join=pero.BEVEL)
        label.draw(canvas, x=x, y=y+15, text="Bevel")
        
        y += margin
        
        # update line properties
        line.line_cap = pero.BUTT
        line.line_join = pero.MITER
        
        # draw solid line
        line.draw(canvas, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.SOLID)
        label.draw(canvas, x=x1, y=y+10, text="Solid")
        
        # draw dashed line
        y += margin
        line.draw(canvas, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.DASHED)
        label.draw(canvas, x=x1, y=y+10, text="Dashed")
        
        # draw dashed line
        y += margin
        line.draw(canvas, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.DOTTED)
        label.draw(canvas, x=x1, y=y+10, text="Dotted")
        
        # draw dash-dotted line
        y += margin
        line.draw(canvas, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.DASHDOTTED)
        label.draw(canvas, x=x1, y=y+10, text="Dash-Dotted")
        
        # draw custom line
        y += margin
        line.draw(canvas, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.CUSTOM, line_dash=[5, 7, 1, 2, 1, 7])
        label.draw(canvas, x=x1, y=y+10, text="Custom")


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Line Styles", 400, 500)
