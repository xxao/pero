#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for glyphs drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # set properties
        line_width = 1
        line_color = pero.colors.Blue
        fill_color = pero.colors.Blue.trans(0.7)
        
        # init glyphs
        origin = pero.Plus(
            size = 10,
            line_color = pero.colors.Red)
        
        label = pero.Text(
            text_align = pero.CENTER)
        
        # init coords
        x = 50
        y = 50
        
        # test annulus
        glyph = pero.Annulus(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, x=x, y=y, inner_radius=10, outer_radius=20)
        origin.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Annulus")
        
        x += 60
        
        # test arc
        glyph = pero.Arc(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, x=x, y=y, radius=20, start_angle=pero.rads(-145), end_angle=pero.rads(100))
        origin.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Arc")
        
        x += 60
        
        # test ellipse
        glyph = pero.Ellipse(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, x=x, y=y, width=50, height=30)
        origin.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Ellipse")
        
        x += 60
        
        # test line
        glyph = pero.Line(line_width=line_width, line_color=line_color)
        glyph.draw(canvas, x1=x-15, y1=y-15, x2=x+15, y2=y+15)
        label.draw(canvas, x=x, y=y+30, text="Line")
        
        x += 60
        
        # test polygon
        points = ((x-20, y-20), (x+20, y-20), (x+20, y-10), (x+10, y-10), (x+10, y+10), (x+20, y+10), (x+20, y+20), (x-10, y+20))
        glyph = pero.Polygon(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, points=points)
        label.draw(canvas, x=x, y=y+30, text="Polygon")
        
        x = 50
        y += 100
        
        # test ray
        glyph = pero.Ray(line_width=line_width, line_color=line_color, offset=5)
        glyph.draw(canvas, x=x-15, y=y-15, length=45, angle=pero.rads(45))
        origin.draw(canvas, x=x-15, y=y-15)
        label.draw(canvas, x=x, y=y+30, text="Ray")
        
        x += 60
        y -= 15
        
        # test rectangle
        glyph = pero.Rect(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, x=x-15, y=y-10, width=30, height=20)
        origin.draw(canvas, x=x-15, y=y-10)
        label.draw(canvas, x=x+40, y=y+45, text="Rect/Bar")
        
        x += 40
        
        # test round rectangle
        glyph = pero.Rect(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, x=x-15, y=y-10, width=30, height=20, radius=5)
        origin.draw(canvas, x=x-15, y=y-10)
        
        x += 40
        
        # test round rectangle
        glyph = pero.Rect(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, x=x-15, y=y-10, width=30, height=20, radius=(0, 5, 7, 10))
        origin.draw(canvas, x=x-15, y=y-10)
        
        x -= 95
        y += 20
        
        # test bar
        glyph = pero.Bar(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, left=x, top=y, right=x+30, bottom=y+20)
        
        x += 40
        
        # test round bar
        glyph = pero.Bar(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, left=x, top=y, right=x+30, bottom=y+20, radius=5)
        
        x += 40
        
        # test round bar
        glyph = pero.Bar(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, left=x, top=y, right=x+30, bottom=y+20, radius=(0, 5, 7, 10))
        
        x += 80
        y -= 5
        
        # test shape
        path = pero.Path.make_star(9, x=x, y=y, outer_radius=20, inner_radius=10)
        glyph = pero.Shape(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, path=path)
        origin.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Shape")
        
        x += 60
        
        # test wedge
        glyph = pero.Wedge(line_width=line_width, line_color=line_color, fill_color=fill_color)
        glyph.draw(canvas, x=x, y=y, inner_radius=10, outer_radius=20, start_angle=pero.rads(-145), end_angle=pero.rads(100))
        origin.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+30, text="Wedge")


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Glyphs", 365, 230)
