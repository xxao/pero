#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for markers drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # set properties
        size = 20
        line_width = 1
        line_color = pero.colors.Blue
        fill_color = pero.colors.Blue.lighter(0.7)
        
        # init glyphs
        line = pero.Line(
            line_color = pero.colors.Red)
        
        label = pero.Text(
            text_align = pero.CENTER)
        
        # init coords
        x = 50
        y = 50
        
        # draw guidelines
        line.draw(canvas, x1=x-30, y1=y-0.5*size, x2=x+450, y2=y-0.5*size, line_color=pero.colors.LightGrey)
        line.draw(canvas, x1=x-30, y1=y, x2=x+450, y2=y)
        line.draw(canvas, x1=x-30, y1=y+0.5*size, x2=x+450, y2=y+0.5*size, line_color=pero.colors.LightGrey)
        
        # test asterisk
        marker = pero.Asterisk(line_width=line_width, line_color=line_color, fill_color=fill_color, size=size)
        marker.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Asterisk")
        
        x += 60
        
        # test cross
        marker = pero.Cross(line_width=line_width, line_color=line_color, fill_color=fill_color, size=size)
        marker.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Cross")
        
        x += 60
        
        # test plus
        marker = pero.Plus(line_width=line_width, line_color=line_color, fill_color=fill_color, size=size)
        marker.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Plus")
        
        x += 60
        
        # test circle
        marker = pero.Circle(line_width=line_width, line_color=line_color, fill_color=fill_color, size=size)
        marker.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Circle")
        
        x += 60
        
        # test diamond
        marker = pero.Diamond(line_width=line_width, line_color=line_color, fill_color=fill_color, size=size)
        marker.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Diamond")
        
        x += 60
        
        # test triangle
        marker = pero.Triangle(line_width=line_width, line_color=line_color, fill_color=fill_color, size=size)
        marker.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Triangle")
        
        x += 60
        
        # test square
        marker = pero.Square(line_width=line_width, line_color=line_color, fill_color=fill_color, size=size)
        marker.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Square")
        
        x += 60
        
        # test symbol
        path = pero.Path.make_ngon(6)
        marker = pero.Symbol(path=path, line_width=line_width, line_color=line_color, fill_color=fill_color, size=size)
        marker.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Symbol")


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Markers", 520, 120)
