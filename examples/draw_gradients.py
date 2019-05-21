#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for gradients drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # set properties
        steps = 128
        padding = 10
        spacer = 10
        indent = 80
        
        # select palettes
        palettes = (
            pero.colors.Spectral,
            
            pero.colors.Blues,
            pero.colors.Greens,
            pero.colors.Greys,
            pero.colors.Oranges,
            pero.colors.Purples,
            pero.colors.Reds,
            
            pero.colors.Inferno,
            pero.colors.Magma,
            pero.colors.Plasma,
            pero.colors.Viridis,
            
            pero.colors.BrBG,
            pero.colors.BuGn,
            pero.colors.BuPu,
            pero.colors.GnBu,
            pero.colors.OrRd,
            pero.colors.PiYG,
            pero.colors.PRGn,
            pero.colors.PuBu,
            pero.colors.PuBuGn,
            pero.colors.PuOr,
            pero.colors.PuRd,
            pero.colors.RdBu,
            pero.colors.RdGy,
            pero.colors.RdPu,
            pero.colors.RdYlBu,
            pero.colors.RdYlGn,
            pero.colors.YlGn,
            pero.colors.YlGnBu,
            pero.colors.YlOrBr,
            pero.colors.YlOrRd)
        
        # init coords
        width, height = canvas.viewport.wh
        length = width - indent - 2*padding
        thickness = (height - 2*padding) / len(palettes) - padding
        y = padding
        
        # init glyphs
        label = pero.Text(
            text_align = pero.RIGHT,
            text_base = pero.MIDDLE)
        
        glyph = pero.ColorBar(
            orientation = pero.HORIZONTAL,
            x = padding+indent,
            length = length,
            thickness = thickness,
            steps = steps)
        
        # draw gradients
        for palette in palettes:
            
            label.draw(canvas, x=padding+indent-10, y=y+0.5*thickness, text=palette.name)
            glyph.draw(canvas, y=y, gradient=palette)
            
            y += spacer + thickness


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Gradients", 600, 800)
