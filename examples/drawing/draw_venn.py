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
        coords, radii = pero.venn.venn.venn(10, 8, 22, 6, 9, 4, 2, pero.VENN_MODE.SEMI)
        
        # scale to window
        coords, radii = pero.venn.venn.fit_into(coords, radii, padding, padding, width - 2 * padding, height - 2 * padding)
        
        # unpack values
        c_a, c_b, c_c = coords
        r_a, r_b, r_c = radii
        
        # draw circles
        pero.Circle(
            size = 2*r_a,
            line_width = 2,
            line_style = pero.SOLID,
            fill_color = "r",
            fill_alpha = 128,
            x = c_a[0],
            y = c_a[1]).draw(canvas)
        
        pero.Circle(
            size = 2*r_b,
            line_width = 2,
            line_style = pero.DOTTED,
            fill_color = "g",
            fill_alpha = 128,
            x = c_b[0],
            y = c_b[1]).draw(canvas)
        
        pero.Circle(
            size = 2*r_c,
            line_width = 2,
            line_style = pero.DASHED,
            fill_color = "b",
            fill_alpha = 128,
            x = c_c[0],
            y = c_c[1]).draw(canvas)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Venn Diagram", 400, 400)
