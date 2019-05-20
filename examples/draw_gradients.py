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
            pero.Palette.Spectral,
            
            pero.Palette.Blues,
            pero.Palette.Greens,
            pero.Palette.Greys,
            pero.Palette.Oranges,
            pero.Palette.Purples,
            pero.Palette.Reds,
            
            pero.Palette.Inferno,
            pero.Palette.Magma,
            pero.Palette.Plasma,
            pero.Palette.Viridis,
            
            pero.Palette.BrBG,
            pero.Palette.BuGn,
            pero.Palette.BuPu,
            pero.Palette.GnBu,
            pero.Palette.OrRd,
            pero.Palette.PiYG,
            pero.Palette.PRGn,
            pero.Palette.PuBu,
            pero.Palette.PuBuGn,
            pero.Palette.PuOr,
            pero.Palette.PuRd,
            pero.Palette.RdBu,
            pero.Palette.RdGy,
            pero.Palette.RdPu,
            pero.Palette.RdYlBu,
            pero.Palette.RdYlGn,
            pero.Palette.YlGn,
            pero.Palette.YlGnBu,
            pero.Palette.YlOrBr,
            pero.Palette.YlOrRd)
        
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
