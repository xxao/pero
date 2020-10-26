import pero
import numpy

# define cases
selected = None
cases = (
    
    # circle regions
    (pero.venn.CircleRegion((25, 50), 20), (75, 50), 20),
    (pero.venn.CircleRegion((40, 50), 30), (60, 50), 30),
    (pero.venn.CircleRegion((50, 50), 40), (55, 50), 30),
    (pero.venn.CircleRegion((55, 50), 30), (50, 50), 40),
    
    # ring regions
    (pero.venn.RingRegion((30, 50), 25, (35, 50), 15), (75, 50), 15),
    (pero.venn.RingRegion((50, 50), 40, (40, 50), 20), (45, 50), 10),
    (pero.venn.RingRegion((50, 50), 40, (40, 50), 20), (50, 50), 45),
    (pero.venn.RingRegion((50, 50), 40, (30, 50), 15), (70, 50), 15),
    (pero.venn.RingRegion((50, 50), 40, (40, 50), 20), (55, 50), 15),
    (pero.venn.RingRegion((40, 50), 35, (30, 50), 20), (75, 50), 20),
    (pero.venn.RingRegion((35, 50), 25, (40, 50), 15), (65, 50), 25),
    (pero.venn.RingRegion((55, 50), 25, (60, 50), 15), (35, 50), 25),
    
    # arcs regions
    (pero.venn.CircleRegion((40, 50), 35).overlay((60, 50), 35)[1], (50, 50), 40),
    (pero.venn.CircleRegion((40, 50), 35).overlay((60, 50), 35)[1], (50, 50), 20),
    (pero.venn.CircleRegion((40, 50), 35).overlay((60, 50), 35)[1], (75, 50), 20),
    (pero.venn.CircleRegion((40, 50), 35).overlay((60, 50), 35)[1], (25, 50), 20),
    (pero.venn.CircleRegion((40, 50), 35).overlay((60, 50), 35)[1], (50, 25), 20),
    (pero.venn.CircleRegion((40, 50), 35).overlay((60, 50), 35)[1], (50, 75), 20),
    
    (pero.venn.CircleRegion((60, 50), 30).overlay((80, 50), 30)[0], (50, 50), 40),
    (pero.venn.CircleRegion((50, 50), 30).overlay((70, 50), 30)[0], (75, 50), 20),
    (pero.venn.CircleRegion((80, 50), 30).overlay((100, 50), 30)[0], (25, 50), 20),
    (pero.venn.CircleRegion((60, 50), 30).overlay((80, 50), 30)[0], (40, 50), 7),
    (pero.venn.CircleRegion((60, 50), 30).overlay((80, 50), 30)[0], (25, 50), 20),
    (pero.venn.CircleRegion((60, 50), 30).overlay((80, 50), 30)[0], (55, 50), 20),
    (pero.venn.CircleRegion((60, 50), 30).overlay((80, 50), 30)[0], (55, 25), 20),
    (pero.venn.CircleRegion((60, 50), 30).overlay((80, 50), 30)[0], (55, 75), 20),
    (pero.venn.CircleRegion((60, 50), 30).overlay((80, 50), 30)[0], (40, 50), 20),
    (pero.venn.CircleRegion((50, 50), 30).overlay((60, 50), 22)[0], (60, 50), 30),
    (pero.venn.CircleRegion((35, 50), 30).overlay((45, 50), 22)[0], (65, 50), 35),
    (pero.venn.CircleRegion((75, 50), 30).overlay((85, 50), 22)[0], (45, 50), 35),
)


class DrawTest(pero.Graphics):
    """Test case for regions overlay."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # fill image
        canvas.fill("w")
        
        # get size
        width, height = canvas.viewport.wh
        
        # get cases
        items = [cases[selected]] if selected is not None else cases
        
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
                self.draw_case(canvas, item[0], item[1], item[2])
            col += 1
            if not col % cols:
                row += 1
                col = 0
    
    
    def draw_case(self, canvas, region, center, radius):
        """Draws region overlay into canvas."""
        
        # init scale
        scale = min(canvas.viewport.wh) / 100
        matrix = pero.Matrix().scale(scale, scale)
        
        # subtract circle from region
        remains, overlap = region.overlay(center, radius)
        
        # get and scale paths
        region_path = region.path().transformed(matrix)
        remains_path = remains.path().transformed(matrix)
        overlap_path = overlap.path().transformed(matrix)
        
        # get and scale label
        remains_label = matrix.transform(*remains.label()) if remains.label() else None
        overlap_label = matrix.transform(*overlap.label()) if overlap.label() else None
        
        # scale circle
        radius = scale*radius
        center = matrix.transform(center[0], center[1])
        
        # draw region
        pero.Shape(
            visible = True,
            path = region_path,
            line_color = pero.colors.Gray,
            line_style = pero.SOLID,
            fill_style = pero.TRANS
            ).draw(canvas)
        
        # draw circle
        pero.Circle(
            visible = True,
            x = center[0],
            y = center[1],
            size = 2*radius,
            line_color = pero.colors.Gray,
            line_style = pero.DOTTED,
            fill_style = pero.TRANS
            ).draw(canvas)
        
        # draw remaining part
        pero.Shape(
            visible = True,
            path = remains_path,
            line_width = 0,
            fill_color = pero.colors.Green,
            fill_alpha = 128,
            ).draw(canvas)
        
        # draw overlapping part
        pero.Shape(
            visible = True,
            path = overlap_path,
            line_width = 0,
            fill_color = pero.colors.Blue,
            fill_alpha = 128,
            ).draw(canvas)
        
        # init label
        label = pero.Text(
            visible = True,
            text_base = pero.MIDDLE,
            text_align = pero.CENTER,
            font_size = 10,
            font_weight = pero.BOLD)
        
        # draw remaining label
        if remains_label is not None:
            label.draw(canvas,
                text = "Re",
                x = remains_label[0],
                y = remains_label[1])
        
        # draw overlapping label
        if overlap_label is not None:
            label.draw(canvas,
                text = "Ov",
                x = overlap_label[0],
                y = overlap_label[1])


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Regions Calculations", 800, 600)
