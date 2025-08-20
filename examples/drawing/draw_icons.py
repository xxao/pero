#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for icons drawing."""
    
    
    def make_circle(self):
        """Makes circle background symbol."""
        
        # make circle
        path = pero.Path()
        path.circle(50, 50, 50)
        
        # make symbol
        return path.symbol()
    
    
    def make_triangle(self, radius=5):
        """Makes rounded triangle background symbol."""
        
        # make triangle
        path = pero.Path()
        path.move_to(50, 20)
        path.arc_to(80, 80, 20, 80, radius, before=False)
        path.arc_to(20, 80, 50, 20, radius)
        path.arc_to(50, 20, 80, 80, radius)
        path.close()
        
        # make symbol
        return path.symbol()
    
    
    def make_hexagon(self, radius=10):
        """Makes rounded hexagon background symbol."""
        
        # make hexagon
        path = pero.Path()
        path.move_to(75, 5)
        path.arc_to(100, 50, 75, 95, radius, before=False)
        path.arc_to(75, 95, 25, 95, radius)
        path.arc_to(25, 95, 0, 50, radius)
        path.arc_to(0, 50, 25, 5, radius)
        path.arc_to(25, 5, 75, 5, radius)
        path.arc_to(75, 5, 100, 50, radius)
        path.close()
        
        # make symbol
        return path.symbol()
    
    
    def make_exclamation_mark(self, radius=4, scale=0.6, offset=0.0):
        """Makes exclamation mark symbol."""
        
        # make exclamation mark
        path = pero.Path()
        path.move_to(50, 72)
        path.arc_to(40, 30, 60, 30, radius, before=True)
        path.arc_to(60, 30, 50, 72, radius)
        path.arc_to(50, 72, 40, 30, radius)
        path.close()
        path.circle(50, 70, 5)
        
        # make symbol
        symbol = path.symbol()
        
        # scale down and offset
        mat = pero.Matrix().scale(scale, scale).translate(0, offset)
        symbol = symbol.transformed(mat)
        
        return symbol
    
    
    def draw_icon(self, canvas, x, y, size, bgr_path, symbol_path, color, outline):
        """Draws icon."""
        
        # scale and shift paths
        mat = pero.Matrix().scale(size, size).translate(x, y)
        bgr_path = bgr_path.transformed(mat)
        symbol_path = symbol_path.transformed(mat)
        
        # draw background
        canvas.line_color = pero.Color(color).darker(0.2)
        canvas.line_width = outline
        canvas.fill_color = color
        canvas.draw_path(bgr_path)
        
        # draw symbol
        canvas.line_color = None
        canvas.line_width = 0
        canvas.fill_color = "#0009"
        canvas.draw_path(symbol_path)
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # init
        size = 100
        space = 50
        outline = 4
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # init coords
        x = space + 0.5*size
        y = 0.5*canvas.height
        
        # draw INFO icon
        bgr_path = self.make_circle()
        symbol_path = self.make_exclamation_mark()
        self.draw_icon(canvas, x, y, size, bgr_path, symbol_path, "#8af", outline)
        
        # shift x
        x += size + space
        
        # draw WARNING icon
        bgr_path = self.make_triangle()
        symbol_path = self.make_exclamation_mark(offset=0.1)
        self.draw_icon(canvas, x, y, size, bgr_path, symbol_path, "#fb0", outline)
        
        # shift x
        x += size + space
        
        # draw ERROR icon
        bgr_path = self.make_triangle()
        symbol_path = self.make_exclamation_mark(offset=0.1)
        self.draw_icon(canvas, x, y, size, bgr_path, symbol_path, "#f55", outline)
        
        # shift x
        x += size + space
        
        # draw STOP icon
        bgr_path = self.make_hexagon()
        symbol_path = self.make_exclamation_mark()
        self.draw_icon(canvas, x, y, size, bgr_path, symbol_path, "#f55", outline)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Rounded Icons", 650, 200)
