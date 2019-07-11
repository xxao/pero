#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for polar text drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # init canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init glyphs
        circle = pero.Circle(
            line_width = 1,
            line_color = pero.colors.Red,
            fill_color = None)
        
        origin = pero.Plus(
            line_width = 1,
            line_color = pero.colors.Red,
            size = 10)
        
        top_label = pero.Text(
            text_align = pero.CENTER)
        
        side_label = pero.Text(
            text_align = pero.CENTER,
            angle = -90,
            angle_units = pero.DEG)
        
        # set text properties
        canvas.font_size = 12
        
        # init values
        positions = (
            pero.OUTSIDE,
            pero.CENTER,
            pero.INSIDE)
        
        rotations = {
            pero.NONE: 'None',
            pero.FOLLOW: 'Follow',
            pero.NATURAL: 'Natural',
            pero.FACEOUT: 'Faceout',
            pero.FACEIN: 'Facein'}
        
        # draw top labels
        top_label.draw(canvas, text="OUTSIDE", x=120, y=20)
        top_label.draw(canvas, text="CENTER", x=120+150, y=20)
        top_label.draw(canvas, text="INSIDE", x=120+300, y=20)
        
        # draw tests
        y = 120
        for rotation in rotations:
            
            x = 20
            side_label.draw(canvas, text=rotations[rotation].upper(), x=x, y=y)
            
            canvas.font_name = 'Arial'
            canvas.font_size = 11
            
            x += 100
            for position in positions:
                radius = 50
                
                origin.draw(canvas, x=x, y=y)
                circle.draw(canvas, x=x, y=y, size=2*radius)
                
                for angle in range(0, 360, 30):
                    label = "%d" % angle
                    angle = pero.rads(angle)
                    canvas.draw_text_polar(label, x, y, radius, angle, position=position, rotation=rotation)
                
                x += 150
            y += 150


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Polar Text", 500, 800)
