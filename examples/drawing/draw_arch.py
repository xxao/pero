#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for arch calculations."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # draw tests
        self.draw_tests(canvas, -15, 90)
    
    
    def draw_tests(self, canvas, angle1, angle2):
        """Draws all tests."""
        
        w = canvas.viewport.w / 2
        h = canvas.viewport.h / 2
        
        with canvas.view(0, 0, w, h):
            self.draw_test(canvas, angle1, angle2, True)
        
        with canvas.view(w, 0, w, h):
            self.draw_test(canvas, angle1, angle2, False)
        
        with canvas.view(0, h, w, h):
            self.draw_test(canvas, angle2, angle1, True)
        
        with canvas.view(w, h, w, h):
            self.draw_test(canvas, angle2, angle1, False)
    
    
    def draw_test(self, canvas, start_angle, end_angle, clockwise):
        """Draws tests for single arch."""
        
        # init arch
        x = canvas.viewport.w / 2
        y = canvas.viewport.h / 2
        r = min(x, y) - 30
        arch = pero.Arch(x, y, r, pero.rads(start_angle), pero.rads(end_angle), clockwise)
        
        # draw tests
        self.draw_bbox(canvas, arch)
        self.draw_rays(canvas, arch)
        self.draw_arch(canvas, arch)
        self.draw_intersects(canvas, arch)
    
    
    def draw_arch(self, canvas, arch):
        """Draws the arch."""
        
        # init glyph
        label = pero.Textbox(
            radius = 3,
            padding = (1, 3),
            line_width = 0,
            fill_color = "b",
            text_color = "w",
            text_base = pero.MIDDLE,
            text_align = pero.CENTER,
            font_size = 7,
            font_weight = pero.BOLD)
        
        # draw circle
        canvas.line_style = pero.SOLID
        canvas.line_color = pero.colors.LightGray
        canvas.line_width = 1
        canvas.fill_style = pero.TRANS
        canvas.draw_circle(arch.x, arch.y, arch.radius)
        
        # draw arch
        canvas.line_color = "b"
        canvas.line_width = 2
        canvas.draw_arc(arch.x, arch.y, arch.radius, arch.start_angle, arch.end_angle, arch.clockwise)
        
        # draw angle
        angle = "%.0f°" % pero.degs(arch.angle())
        label.draw(canvas, x=arch.x, y=arch.y, text=angle, font_size=9)
        
        # draw points
        start_point = arch.start_point()
        label.draw(canvas, x=start_point[0], y=start_point[1], text="S")
        
        end_point = arch.end_point()
        label.draw(canvas, x=end_point[0], y=end_point[1], text="E")
        
        mid_point = arch.mid_point()
        label.draw(canvas, x=mid_point[0], y=mid_point[1], text="M")
    
    
    def draw_rays(self, canvas, arch):
        """Draws the contains angle test."""
        
        # init glyphs
        label = pero.Textbox(
            radius = 3,
            padding = (1, 3),
            line_width = 0,
            fill_color = "b",
            text_color = "w",
            text_base = pero.MIDDLE,
            text_align = pero.CENTER,
            font_size = 8,
            font_weight = pero.BOLD)
        
        ray = pero.Ray(
            x = arch.x,
            y = arch.y,
            length = arch.radius,
            line_width = 1)
        
        norm = pero.Ray(
            x = arch.x,
            y = arch.y,
            offset = arch.radius,
            length = 15,
            line_width = 2,
            line_color = "b")
        
        point = pero.Circle(
            line_width = 0,
            size = 6)
        
        # draw rays
        for angle in range(0, 360, 15):
            
            angle = pero.rads(angle)
            inside = arch.contains_angle(angle)
            color = "g" if inside else pero.colors.LightGray
            ray.draw(canvas, angle=angle, line_color=color)
            
            p = arch.angle_as_point(angle)
            inside = arch.contains_point(p[0], p[1])
            color = "g" if inside else pero.colors.LightGray
            point.draw(canvas, x=p[0], y=p[1], fill_color=color)
        
        # draw points
        for p in (arch.start_point(), arch.mid_point(), arch.end_point()):
            
            angle = arch.point_as_angle(p[0], p[1])
            norm.draw(canvas, angle=angle)
            
            x, y = pero.ray(p, angle, norm.length+5)
            text = "%.0f°" % pero.degs(angle)
            label.draw(canvas, x=x, y=y, text=text)
    
    
    def draw_bbox(self, canvas, arch):
        """Draws the bbox test."""
        
        # init glyph
        rect = pero.Rect(
            line_color = pero.colors.LightBlue,
            fill_style = pero.TRANS,
            x = lambda d: d.x,
            y = lambda d: d.y,
            width = lambda d: d.w,
            height = lambda d: d.h)
        
        # draw bbox
        rect.draw(canvas, arch.bbox())
    
    
    def draw_intersects(self, canvas, arch):
        """Draws the intersections test."""
        
        # init glyph
        label = pero.Textbox(
            radius = 3,
            padding = (1, 3),
            line_width = 0,
            fill_color = "r",
            text_color = "w",
            text_base = pero.MIDDLE,
            text_align = pero.CENTER,
            font_size = 8,
            font_weight = pero.BOLD)
        
        # init arches
        top_arch = pero.Arch(arch.x, arch.y - 1.5*arch.radius, 0.9*arch.radius, pero.rads(20), pero.rads(160), True)
        right_arch = pero.Arch(arch.x + 1.5*arch.radius, arch.y, 0.9*arch.radius, pero.rads(-110), pero.rads(110), False)
        bottom_arch = pero.Arch(arch.x, arch.y + 1.5*arch.radius, 0.9*arch.radius, pero.rads(-20), pero.rads(-160), False)
        left_arch = pero.Arch(arch.x - 1.5*arch.radius, arch.y, 0.9*arch.radius, pero.rads(-70), pero.rads(70), True)
        
        # draw arches
        canvas.line_style = pero.SOLID
        canvas.line_color = pero.colors.LightGray
        canvas.line_width = 1
        canvas.fill_style = pero.TRANS
        
        canvas.draw_arc(top_arch.x, top_arch.y, top_arch.radius, top_arch.start_angle, top_arch.end_angle, top_arch.clockwise)
        canvas.draw_arc(right_arch.x, right_arch.y, right_arch.radius, right_arch.start_angle, right_arch.end_angle, right_arch.clockwise)
        canvas.draw_arc(bottom_arch.x, bottom_arch.y, bottom_arch.radius, bottom_arch.start_angle, bottom_arch.end_angle, bottom_arch.clockwise)
        canvas.draw_arc(left_arch.x, left_arch.y, left_arch.radius, left_arch.start_angle, left_arch.end_angle, left_arch.clockwise)
        
        # draw intersections
        for i, p in enumerate(arch.intersect_arch(top_arch)):
            label.draw(canvas, x=p[0], y=p[1], text=i)
        
        for i, p in enumerate(arch.intersect_arch(right_arch)):
            label.draw(canvas, x=p[0], y=p[1], text=i)
        
        for i, p in enumerate(arch.intersect_arch(bottom_arch)):
            label.draw(canvas, x=p[0], y=p[1], text=i)
        
        for i, p in enumerate(arch.intersect_arch(left_arch)):
            label.draw(canvas, x=p[0], y=p[1], text=i)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Arch", 600, 600)
