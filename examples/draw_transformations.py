#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for matrix transformations."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init path
        path = pero.Path()
        path.move_to(0, 0)
        path.line_to(40, 0)
        path.line_to(40, 40)
        path.line_to(0, 40)
        path.close()
        
        # init glyphs
        ghost = pero.Shape(
            path = path,
            line_color = pero.colors.Blue.trans(0.25),
            fill_color = pero.colors.Blue.trans(0.5))
        
        shape = pero.Shape(
            line_color = pero.colors.Orange,
            fill_color = pero.colors.Orange.trans(0.25))
        
        origin = pero.Plus(
            x = 0,
            y = 0,
            size = 10,
            line_color = pero.colors.Red)
        
        label = pero.Text(
            x = 0,
            y = 60,
            text_align = pero.LEFT)
        
        # draw original shape
        x = 50
        y = 50
        
        # translate
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().translate(10, 10)
        shape.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, text="Translate")
        
        x += 100
        
        # ray
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().ray(10, pero.rads(-45))
        shape.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, text="Ray")
        
        x += 100
        
        # rotate from origin
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().rotate(pero.rads(45))
        shape.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, text="Rotate")
        
        x += 100
        
        # rotate from point
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().rotate(pero.rads(45), x=20, y=20)
        shape.draw(canvas, path=path.transformed(matrix))
        origin.draw(canvas, x=20, y=20, line_color=pero.colors.White)
        label.draw(canvas, text="Rotate (ori)")
        
        x = 50
        y += 120
        
        # scale from origin
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().scale(0.75, 1.5)
        shape.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, text="Scale")
        
        x += 100
        
        # scale from point
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().scale(0.75, 1.5, x=20, y=20)
        shape.draw(canvas, path=path.transformed(matrix))
        origin.draw(canvas, x=20, y=20, line_color=pero.colors.White)
        label.draw(canvas, text="Scale (ori)")
        
        x += 100
        
        # skew from origin
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().skew(pero.rads(20), 10)
        shape.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, text="Skew")
        
        x += 100
        
        # skew from point
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().skew(pero.rads(20), 10, x=20, y=20)
        shape.draw(canvas, path=path.transformed(matrix))
        origin.draw(canvas, x=20, y=20, line_color=pero.colors.White)
        label.draw(canvas, text="Skew (ori)")
        
        x = 50
        y += 120
        
        # init flipping path
        path = pero.Path()
        path.move_to(0, 0)
        path.line_to(15, 0)
        path.line_to(40, 40)
        path.line_to(0, 40)
        path.close()
        
        ghost.path = path
        
        # flip horizontally from origin
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().hflip()
        shape.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, text="H Flip")
        
        x += 100
        
        # flip horizontally from point
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().hflip(20)
        shape.draw(canvas, path=path.transformed(matrix))
        origin.draw(canvas, x=20, y=20, line_color=pero.colors.White)
        label.draw(canvas, text="H Flip (ori)")
        
        x += 100
        
        # flip vertically from origin
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().vflip()
        shape.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, text="V Flip")
        
        x += 100
        
        # flip vertically from point
        canvas.view(x, y)
        ghost.draw(canvas)
        origin.draw(canvas)
        
        matrix = pero.Matrix().vflip(20)
        shape.draw(canvas, path=path.transformed(matrix))
        origin.draw(canvas, x=20, y=20, line_color=pero.colors.White)
        label.draw(canvas, text="V Flip (ori)")


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Matrix Transformations", 450, 400)
