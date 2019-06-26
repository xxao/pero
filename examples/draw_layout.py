#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for layout drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init layout
        layout = pero.Layout(spacing=10, padding=20)
        
        for row in range(4):
            relative = bool(row % 2)
            layout.add_row(100, relative)
        
        for col in range(4):
            relative = bool(col % 2)
            layout.add_col(100, relative)
        
        # add glyphs
        for row in range(4):
            for col in range(4):
                
                # skip span
                if row == 1 and col == 2:
                    continue
                if row == 2 and col == 3:
                    continue
                
                # get data
                col_span = 2 if row == 1 and col == 1 else 1
                row_span = 2 if row == 1 and col == 3 else 1
                width = 20 if col in (0, 3) else pero.UNDEF
                height = 20 if row in (0, 3) else pero.UNDEF
                h_align = pero.LEFT if col == 0 else pero.RIGHT if col == 3 else pero.CENTER
                v_align = pero.TOP if row == 0 else pero.BOTTOM if row == 3 else pero.CENTER
                
                # init glyph
                label = "(%s, %s) (%s, %s)" % (row, col, row_span, col_span)
                glyph = pero.Framer(label=label)
                
                # add to layout
                layout.add(glyph, row, col,
                    col_span = col_span,
                    row_span = row_span,
                    clip = True,
                    width = width,
                    height = height,
                    padding = 0,
                    h_expand = False,
                    v_expand = False,
                    h_align = h_align,
                    v_align = v_align,
                    line_color = "#0003")
        
        # draw layout
        layout.draw(canvas)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Layout", 400, 400)
