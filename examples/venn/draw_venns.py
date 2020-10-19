import pero
import numpy

# define image
mode = pero.FULL
sizes = (5, 8, 7, 6, 9, 4, 2)

venn = ""
region = ""

# calc venn
venns = (
    
    # no overlap
    "A B C",
    "A B",
    "A C",
    "B C",
    
    # full overlap
    "ABC",
    "AB",
    "AC",
    "BC",
    
    "A BC",
    "B AC",
    "C AB",
    
    "A AB",
    "A AC",
    "B AB",
    "B BC",
    "C AC",
    "C BC",

    "A AB C",
    "A AC B",
    "A BC C",
    
    # two overlaps
    "A B AB",
    "A C AC",
    "B C BC",
    
    "A B C AB",
    "A B C AC",
    "A B C BC",
    
    "A B C AB BC",
    "A B C AB AC",
    "A B C AC BC",
    
    # three overlaps
    "AB AC BC ABC",
    "A B ABC",
    "A C ABC",
    "B C ABC",
    
    # full
    "A B C AB AC BC ABC",
)


class DrawTest(pero.Graphics):
    """Test case for venn calculations."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # fill image
        canvas.fill("w")
        
        # get size
        width, height = canvas.viewport.wh
        
        # select specific
        items = [venn] if venn else venns
        
        # init grid
        cols = 6 if len(items) > 1 else 1
        rows = int(numpy.ceil(len(items) / cols))
        cell_w = width / cols
        cell_h = height / rows
        
        # draw grid
        canvas.line_color = pero.colors.LightGray
        for i in range(1, rows):
            canvas.draw_line(0, i * cell_h, width, i * cell_h)
        for i in range(1, cols):
            canvas.draw_line(i * cell_w, 0, i * cell_w, height)
        
        # draw venn
        row = col = 0
        for item in items:
            with canvas.view(col * cell_w, row * cell_h, cell_w, cell_h):
                self.draw_venn(canvas, item, region, len(items) == 1)
            col += 1
            if not col % cols:
                row += 1
                col = 0
    
    
    def draw_venn(self, canvas, venn, region, solo):
        """Draws venn diagram into canvas."""
        
        # log title
        print(venn)
        
        # get values
        indices = ('A', 'B', 'AB', 'C', 'AC', 'BC', 'ABC')
        values = [0, 0, 0, 0, 0, 0, 0]
        
        for item in venn.split():
            idx = indices.index(item)
            values[idx] = sizes[idx]
        
        # calc venn
        coords, radii = pero.venn.calc_venn(*values, mode=mode)
        
        # scale to canvas view
        padding = 20
        w, h = canvas.viewport.wh
        coords, radii = pero.venn.fit_into(coords, radii, padding, padding + 5, w - 2 * padding, h - 2 * padding - 5)
        
        # unpack values
        c_a, c_b, c_c = coords
        r_a, r_b, r_c = radii
        
        # calc intersections
        int_ab = pero.intersect_circles(c_a, r_a, c_b, r_b)
        int_bc = pero.intersect_circles(c_b, r_b, c_c, r_c)
        int_ac = pero.intersect_circles(c_a, r_a, c_c, r_c)
        
        # make regions
        regions = pero.venn.make_regions(coords, radii)
        
        # init glyphs
        header = pero.Text(
            x = 0.5*w,
            y = 5,
            text_base = pero.TOP,
            text_align = pero.CENTER)
        
        circle = pero.Circle(
            x = lambda d: d[0][0],
            y = lambda d: d[0][1],
            size = lambda d: 2*d[1] or 4,
            line_width = lambda d: 0 if d[1] else 1,
            line_color = pero.colors.Gray,
            fill_style = lambda d: pero.SOLID if d[1] else pero.TRANS,
            fill_alpha = lambda d: 128 if region else 0)
        
        shape = pero.Shape(
            line_color = "r",
            line_width = 2 if region and solo else 0,
            fill_alpha = 255 if region else 150)
        
        point = pero.Circle(
            x = lambda d: d[0],
            y = lambda d: d[1],
            size = 5,
            line_width = 0,
            fill_color = "r")
        
        label = pero.Textbox(
            x = lambda d: d[0],
            y = lambda d: d[1],
            text_align = pero.CENTER,
            text_base = pero.MIDDLE,
            text_color = "w",
            font_size = 8,
            radius = 3,
            padding = (1, 3),
            line_width = 0,
            fill_color = "k")
        
        # draw venn
        header.draw(canvas, text=venn)
        circle.draw(canvas, source=(c_a, r_a), fill_color="r")
        circle.draw(canvas, source=(c_b, r_b), fill_color="g")
        circle.draw(canvas, source=(c_c, r_c), fill_color="b")
        
        # draw regions
        palette = pero.colors.Pero
        for i, key in enumerate(('a', 'b', 'c', 'ab', 'ac', 'bc', 'abc')):
            if not region or key == region:
                
                reg = regions[key]
                color = palette[i] if not region else "k"
                shape.draw(canvas, path=reg.path(), fill_color=color)
                
                if region and solo:
                    for j, p in enumerate(reg.points()):
                        label.draw(canvas, p, text=j)
        
        # draw intersections
        for inter in (int_ab, int_bc, int_ac):
            if inter:
                point.draw_many(canvas, source=inter)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Venn Calculations", 800, 600)
