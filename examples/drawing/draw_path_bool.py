#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for path boolean operations drawing."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # init coords
        padding = 20
        offset = 0.5
        width, height = canvas.viewport.wh
        size = min((width-4*padding) / 3, (height-2*padding)) * 2/3
        shift = offset * size
        
        # init matrix
        mat = pero.Matrix().translate(x_shift=size+shift+padding)
        
        # init paths
        path_1 = pero.make_star(
            x = padding + 0.5 * size,
            y = 0.5 * height - 0.5 * shift,
            outer_radius = 0.5 * size,
            inner_radius = 0.25 * size,
            rays = 6)
        
        path_2 = pero.make_star(
            x = padding + 0.5 * size + shift,
            y = 0.5 * height + 0.5 * shift,
            outer_radius = 0.5 * size,
            inner_radius = 0.25 * size,
            rays = 6)
        
        path_3 = pero.make_circle(
            x = padding + 0.5 * size + shift,
            y = 0.5 * height - 0.5 * shift,
            radius = 0.4 * size)
        
        # init glyphs
        shape_1 = pero.Shape(
            line_width = 6,
            line_color = pero.colors.Green.trans(0.5),
            fill_color = pero.colors.Transparent)
        
        shape_2 = pero.Shape(
            line_width = 6,
            line_color = pero.colors.Blue.trans(0.5),
            fill_color = pero.colors.Transparent)
        
        shape_3 = pero.Shape(
            line_width = 6,
            line_color = pero.colors.Orange.trans(0.5),
            fill_color = pero.colors.Transparent)
        
        pather = pero.Pather(
            line_width = 2,
            line_color = pero.colors.Black,
            fill_color = pero.colors.Gray.trans(0.5))
        
        # draw union
        result = path_1.clone().union(path_2).union(path_3)
        shape_1.draw(canvas, path=path_1)
        shape_2.draw(canvas, path=path_2)
        shape_3.draw(canvas, path=path_3)
        pather.draw(canvas, path=result)
        
        # offset paths
        path_1.transform(mat)
        path_2.transform(mat)
        path_3.transform(mat)
        
        # draw subtract
        result = path_1.clone().subtract(path_2).subtract(path_3)
        shape_1.draw(canvas, path=path_1)
        shape_2.draw(canvas, path=path_2)
        shape_3.draw(canvas, path=path_3)
        pather.draw(canvas, path=result)
        
        # offset paths
        path_1.transform(mat)
        path_2.transform(mat)
        path_3.transform(mat)
        
        # draw intersect
        result = path_1.clone().intersect(path_2).intersect(path_3)
        shape_1.draw(canvas, path=path_1)
        shape_2.draw(canvas, path=path_2)
        shape_3.draw(canvas, path=path_3)
        pather.draw(canvas, path=result)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Path Boolean Operations", 700, 250)
