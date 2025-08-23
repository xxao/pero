#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for path shapes."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # init glyph
        glyph = pero.Pather(
            show_anchors = False,
            show_handles = False)
        
        # init label
        label = pero.Text(
            text_align = pero.CENTER)
        
        # init coords
        padding = 40
        spacing = 100
        x = padding
        y = padding
        
        # draw arc
        path = pero.make_arc(x=x+15, y=y+15, radius=30, start_angle=pero.rads(-120), end_angle=pero.rads(120))
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Arc")
        
        x += spacing
        
        # draw circle
        path = pero.make_circle(x=x+15, y=y+15, radius=30)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Circle")
        
        x += spacing
        
        # draw ellipse
        path = pero.make_ellipse(x=x+15, y=y+15, width=30, height=60)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Ellipse")
        
        x = padding
        y += spacing
        
        # draw rectangle
        path = pero.make_rect(x=x-5, y=y-10, width=40, height=60)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Rect")
        
        x += spacing
        
        # draw rectangle rounded
        path = pero.make_rect(x=x-5, y=y-10, width=40, height=60, radius=(10, 15, 7, 5))
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Rect Round")
        
        x = padding
        y += spacing
        
        # draw star
        path = pero.make_star(7, x=x+15, y=y+15, inner_radius=15, outer_radius=30)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Star")
        
        x += spacing
        
        # draw hexagon
        path = pero.make_ngon(6, x=x+15, y=y+15, radius=30)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Hexagon")
        
        x += spacing
        
        # draw annulus
        path = pero.make_annulus(x=x + 15, y=y + 15, inner_radius=15, outer_radius=30)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Annulus")
        
        x = padding
        y += spacing
        
        # add wedge
        path = pero.make_wedge(x=x+15, y=y+15, inner_radius=15, outer_radius=30, start_angle=pero.rads(-120), end_angle=pero.rads(120))
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Donut")
        
        x += spacing
        
        # add wedge rounded
        path = pero.make_wedge(x=x+15, y=y+15, inner_radius=15, outer_radius=30, start_angle=pero.rads(-120), end_angle=pero.rads(120), corners=5)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Donut Round")
        
        x += spacing
        
        # add wedge caped
        path = pero.make_wedge(x=x+15, y=y+15, inner_radius=15, outer_radius=30, start_angle=pero.rads(-120), end_angle=pero.rads(120), caped=True)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Donut Caped")
        
        x = padding
        y += spacing
        
        # add pizza
        path = pero.make_wedge(x=x+15, y=y+15, inner_radius=0, outer_radius=30, start_angle=pero.rads(-120), end_angle=pero.rads(120))
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Pie")
        
        x += spacing
        
        # add pizza
        path = pero.make_wedge(x=x+15, y=y+15, inner_radius=0, outer_radius=30, start_angle=pero.rads(-120), end_angle=pero.rads(120), corners=10)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Pie Round")


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Path Shapes", 320, 540)
