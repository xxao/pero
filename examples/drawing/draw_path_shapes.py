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
        x = 40
        y = 40
        
        # draw star
        path = pero.Path.make_star(7, x=x+15, y=y+15, inner_radius=15, outer_radius=30)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Star")
        
        x += 80
        
        # draw hexagon
        path = pero.Path.make_ngon(6, x=x+15, y=y+15, radius=30)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Hexagon")
        
        x += 80
        
        # draw annulus
        path = pero.Path.make_annulus(x=x+15, y=y+15, inner_radius=15, outer_radius=30)
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Annulus")
        
        x += 80
        
        # add annulus
        path = pero.Path.make_wedge(x=x+15, y=y+15, inner_radius=15, outer_radius=30, start_angle=pero.rads(-120), end_angle=pero.rads(120))
        glyph.draw(canvas, path=path)
        label.draw(canvas, x=x+15, y=y+60, text="Wedge")


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Path Shapes", 350, 130)
