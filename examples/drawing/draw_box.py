#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for box drawing."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # init size
        size = 30
        spacing = 10
        total = size + spacing
        
        # init text glyph
        text = pero.Text(
            font_weight = pero.BOLD,
            text_align = pero.CENTER,
            text_base = pero.MIDDLE)
        
        # init box glyph
        box = pero.Box(
            graphics = text,
            line_width = 1,
            line_color = "k",
            fill_color = "a",
            fill_alpha = 150,
            radius = 7,
            v_align = pero.CENTER,
            h_align = pero.CENTER)
        
        # draw horizontally stretched top boxes
        margin = [spacing, total+spacing, spacing, spacing]
        
        box.draw(canvas,
            graphics_text = "NW / H",
            anchor = pero.NW,
            height = size,
            margin = margin)
        
        margin[0] += total
        margin[1] += total
        margin[3] += total
        
        box.draw(canvas,
            graphics_text = "N / H",
            anchor = pero.N,
            x = 0.5*canvas.width,
            height = size,
            margin = margin)
        
        margin[0] += total
        margin[1] += total
        margin[3] += total
        
        box.draw(canvas,
            graphics_text = "NE / H",
            anchor = pero.NE,
            x = canvas.width,
            height = size,
            margin = margin)
        
        # draw horizontally stretched bottom boxes
        margin = [spacing, spacing, spacing, total+spacing]
        
        box.draw(canvas,
            graphics_text = "SW / H",
            anchor = pero.SW,
            y = canvas.height,
            height = size,
            margin = margin)
        
        margin[1] += total
        margin[2] += total
        margin[3] += total
        
        box.draw(canvas,
            graphics_text = "S / H",
            anchor = pero.S,
            x = 0.5*canvas.width,
            y = canvas.height,
            height = size,
            margin = margin)
        
        margin[1] += total
        margin[2] += total
        margin[3] += total
        
        box.draw(canvas,
            graphics_text = "SE / H",
            anchor = pero.SE,
            x = canvas.width,
            y = canvas.height,
            height = size,
            margin = margin)
        
        # draw vertically stretched left boxes
        margin = [total+spacing, spacing, spacing, spacing]
        
        box.draw(canvas,
            graphics_text = "NW / V",
            graphics_angle = pero.rads(90),
            anchor = pero.NW,
            width = size,
            margin = margin)
        
        margin[0] += total
        margin[2] += total
        margin[3] += total
        
        box.draw(canvas,
            graphics_text = "W / V",
            graphics_angle = pero.rads(90),
            anchor = pero.W,
            y = 0.5*canvas.height,
            width = size,
            margin = margin)
        
        margin[0] += total
        margin[2] += total
        margin[3] += total
        
        box.draw(canvas,
            graphics_text = "SW / V",
            graphics_angle = pero.rads(90),
            anchor = pero.SW,
            y = canvas.height,
            width = size,
            margin = margin)
        
        # draw vertically stretched right boxes
        margin = [spacing, spacing, total+spacing, spacing]
        
        box.draw(canvas,
            graphics_text = "NE / V",
            graphics_angle = pero.rads(90),
            anchor = pero.NE,
            x = canvas.width,
            width = size,
            margin = margin)
        
        margin[0] += total
        margin[1] += total
        margin[2] += total
        
        box.draw(canvas,
            graphics_text = "E / V",
            graphics_angle = pero.rads(90),
            anchor = pero.E,
            x = canvas.width,
            y = 0.5*canvas.height,
            width = size,
            margin = margin)
        
        margin[0] += total
        margin[1] += total
        margin[2] += total
        
        box.draw(canvas,
            graphics_text = "SE / V",
            graphics_angle = pero.rads(90),
            anchor = pero.SE,
            x = canvas.width,
            y = canvas.height,
            width = size,
            margin = margin)
        
        # draw horizontally and vertically stretched center boxe
        margin = 4*[3*total+spacing]
        
        box.draw(canvas,
            graphics_text = "C / HV",
            anchor = pero.C,
            x = 0.5*canvas.width,
            y = 0.5*canvas.height,
            margin = margin)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Box", 500, 500)
