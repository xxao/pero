#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for available fonts."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # set properties
        padding = 30
        spacing = 5
        
        # init glyphs
        label = pero.Text(
            text_align = pero.TEXT_ALIGN_LEFT,
            text_base = pero.TEXT_BASE_TOP,
            font_size = 12)
        
        # init coords
        x = padding
        y = padding
        column = 0
        
        # draw fonts
        last_name = None
        for font in sorted(pero.FONTS.fonts, key=lambda d: d.name):
            
            # skip same font variants
            if font.name == last_name:
                continue
            last_name = font.name
            
            # skip some fonts
            if font.name.startswith('.'):
                continue
            if "Noto Sans " in font.name:
                continue
            if font.name.startswith("STIX"):
                continue
            
            # get regular font variant
            font = pero.FONTS.get_font(font.name, label.font_style, label.font_weight)
            
            # show font
            label.draw(canvas, x=x, y=y, text=font.name, font_name=font.name)
            
            # update coords
            w, h = canvas.get_line_size(font.name)
            y += h + spacing
            column = max(column, w)
            
            # check row
            if y + padding > canvas.height:
                y = padding
                x += column + padding
                column = 0


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Fonts", 1200, 700)
