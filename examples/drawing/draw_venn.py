#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for manually assembled venn diagram."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # calc coordinates
        padding = 15
        width, height = canvas.viewport.wh
        
        # calc venn
        radii, coords = pero.venn.calc_venn(10, 8, 22, 6, 9, 4, 2, proportional=True)
        radii, coords = pero.venn.fit_into(radii, coords, padding, padding, width-2*padding, height-2*padding)
        
        # unpack values
        r_a, r_b, r_c = radii
        c_a, c_b, c_c = coords
        
        # calc intersections
        int_ab = pero.venn.calc_intersections(c_a, r_a, c_b, r_b)
        int_bc = pero.venn.calc_intersections(c_b, r_b, c_c, r_c)
        int_ac = pero.venn.calc_intersections(c_a, r_a, c_c, r_c)
        
        # draw circles
        pero.Circle(
            size = 2*r_a,
            line_width = 0,
            fill_color = "r",
            fill_alpha = 128,
            x = c_a[0],
            y = c_a[1]).draw(canvas)
        
        pero.Circle(
            size = 2*r_b,
            line_width = 0,
            fill_color = "g",
            fill_alpha = 128,
            x = c_b[0],
            y = c_b[1]).draw(canvas)
        
        pero.Circle(
            size = 2*r_c,
            line_width = 0,
            fill_color = "b",
            fill_alpha = 128,
            x = c_c[0],
            y = c_c[1]).draw(canvas)
        
        # draw intersections
        marker = pero.Circle(
            size = 9,
            line_width = 0,
            fill_color = "k")
        
        for p in (int_ab, int_bc, int_ac):
            if p is not None:
                marker.draw(canvas, x=p[0][0], y=p[0][1])
                marker.draw(canvas, x=p[1][0], y=p[1][1])


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Venn Diagram", 400, 400)
