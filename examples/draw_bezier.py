#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for arc drawing."""
    
    
    def draw_hull(self, canvas, curve):
        """Draws hull test."""
        
        # init glyphs
        pather = pero.Pather(fill_color=None, show_cursor=False)
        point = pero.Circle(fill_color="r", line_color="w", size=8)
        line = pero.Line(line_color="r")
        
        # draw curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        t = .4
        
        # draw hull
        for stage in curve.hull(t):
            
            if len(stage) == 1:
                point.draw(canvas, x=stage[0][0], y=stage[0][1])
                continue
            
            p1 = stage[0]
            for p2 in stage[1:]:
                line.draw(canvas, x1=p1[0], y1=p1[1], x2=p2[0], y2=p2[1])
                p1 = p2
        
        # draw point
        x,y = curve.point(t)
        point.draw(canvas, x=x, y=y, line_color="r", fill_color=None, size=10)
    
    
    def draw_slice(self, canvas, curve):
        """Draws slice test."""
        
        # init glyphs
        pather = pero.Pather(fill_color=None, show_cursor=False)
        
        # draw curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        # draw slice
        segment = curve.slice(.25, .75)
        path = pero.Path.from_bezier(segment)
        pather.draw(canvas, path=path, line_color="r", line_width=3, anchor_fill_color="r")
    
    
    def draw_extremes(self, canvas, curve):
        """Draws extremes tests."""
        
        # init glyphs
        pather = pero.Pather(fill_color=None, show_cursor=False)
        point = pero.Circle(fill_color="r", line_color="w", size=8)
        frame = pero.Rect(line_color="r", fill_color=None)
        label = pero.Text(font_size=8, text_base=pero.BOTTOM)
        
        # draw curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        # draw bbox
        bbox = curve.bbox()
        frame.draw(canvas, x=bbox.x, y=bbox.y, width=bbox.w, height=bbox.h)
        
        # draw extremes
        extremes = curve.extremes()
        for t in extremes[0]+extremes[1]:
            x,y = curve.point(t)
            point.draw(canvas, x=x, y=y)
        
        # draw length
        length = "len: %.2f" % curve.length()
        label.draw(canvas, text=length, x=bbox.x1+5, y=bbox.y2-5)
    
    
    def draw_normals(self, canvas, curve):
        """Draws normals tests."""
        
        # init glyphs
        pather = pero.Pather(fill_color=None, show_cursor=False)
        point = pero.Circle(fill_color="r", line_color="w", size=8)
        line = pero.Line()
        
        # draw curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        # draw normals
        t = 0
        d = 20
        while t <= 1:
            
            x,y = curve.point(t)
            nx,ny = curve.normal(t)
            tx,ty = curve.tangent(t)
            
            if nx is not None:
                line.draw(canvas, x1=x, y1=y, x2=x+d*nx, y2=y+d*ny, line_color="r")
                line.draw(canvas, x1=x, y1=y, x2=x+d*tx, y2=y+d*ty, line_color="g")
            
            point.draw(canvas, x=x, y=y)
            
            t += 0.1
    
    
    def draw_inflections(self, canvas, curve):
        """Draws inflections test."""
        
        # init objects
        pather = pero.Pather(fill_color=None, show_cursor=False)
        point = pero.Circle(fill_color="r", line_color="w", size=8)
        
        # draw curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        # draw inflections
        for t in curve.inflections():
            x,y = curve.point(t)
            point.draw(canvas, x=x, y=y)
    
    
    def draw_reduce(self, canvas, curve):
        """Draws line reduce test."""
        
        # init objects
        pather = pero.Pather(fill_color=None, show_cursor=False)
        point = pero.Circle(fill_color="r", line_color="w", size=8)
        
        # draw curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        # draw segments
        for segment in curve.reduce():
            coords = segment.coords
            point.draw(canvas, x=coords[0], y=coords[1])
            point.draw(canvas, x=coords[-2], y=coords[-1])
    
    
    def draw_projections(self, canvas, curve):
        """Draws projections tests."""
        
        # init glyphs
        pather = pero.Pather(fill_color=None, show_cursor=False)
        point = pero.Circle(fill_color="r", line_color="w", size=8)
        line = pero.Line(line_color="r")
        
        # draw curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        # init points
        points = (
            (50, 10), (50,50), (50,100), (50,150),
            (90, 10), (90,50), (90,100), (90,150), (140,200))
        
        # draw projections
        for px, py in points:
            x, y, t, dist = curve.project(px, py)
            point.draw(canvas, x=px, y=py)
            line.draw(canvas, x1=px, y1=py, x2=x, y2=y)
    
    
    def draw_cuts(self, canvas, curve):
        """Draws line cuts test."""
        
        # init objects
        pather = pero.Pather(fill_color=None, show_cursor=False)
        point = pero.Circle(fill_color="r", line_color="w", size=8)
        line = pero.Line(line_color="r")
        
        # draw curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        # init cuts
        bbox = curve.bbox()
        xcut = 75
        ycut = 75
        lcut = (bbox.x1-20, bbox.y1-10, bbox.x2-10, bbox.y2+10)
        
        # draw lines
        line.draw(canvas, x1=xcut, y1=bbox.y1-10, x2=xcut, y2=bbox.y2+10)
        line.draw(canvas, x1=bbox.x1-10, y1=ycut, x2=bbox.x2, y2=ycut)
        line.draw(canvas, x1=lcut[0], y1=lcut[1], x2=lcut[2], y2=lcut[3])
        
        # draw x-cuts
        for t in curve.xcuts(xcut):
            x,y = curve.point(t)
            point.draw(canvas, x=x, y=y)
        
        # draw y-cuts
        for t in curve.ycuts(ycut):
            x,y = curve.point(t)
            point.draw(canvas, x=x, y=y)
        
        # draw line cuts
        for t in curve.cuts(*lcut):
            x,y = curve.point(t)
            point.draw(canvas, x=x, y=y)
        
    
    def draw_intersects_line(self, canvas, curve):
        """Draws line intersection test."""
        
        # init objects
        pather = pero.Pather(fill_color=None, show_cursor=False)
        point = pero.Circle(fill_color="r", line_color="w", size=8)
        
        # init line
        curve2 = pero.Bezier(75,15 , 75,25 , 75,185 , 75,205)
        
        # draw 1st curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        # draw 2nd curve
        path = pero.Path.from_bezier(curve2)
        pather.draw(canvas, path=path, line_color="r", show_anchors=False, show_handles=False)
        
        # draw intersections
        for t1,t2 in curve.intersects(curve2):
            
            x,y = curve.point(t1)
            point.draw(canvas, x=x, y=y)
            
            x,y = curve2.point(t2)
            point.draw(canvas, x=x, y=y, size=10, fill_color=None, line_color="r")
    
    
    def draw_intersects_curve(self, canvas, curve):
        """Draws curve intersection test."""
        
        # init objects
        pather = pero.Pather(fill_color=None, show_cursor=False)
        point = pero.Circle(fill_color="r", line_color="w", size=8)
        
        # init 2nd curve
        curve2 = pero.Bezier(25,50 , 170,50 , 20,170 , 150,150)
        
        # draw 1st curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        # draw 2nd curve
        path = pero.Path.from_bezier(curve2)
        pather.draw(canvas, path=path, line_color="r", show_anchors=False, show_handles=False)
        
        # draw intersections
        for t1,t2 in curve.intersects(curve2):
            
            x,y = curve.point(t1)
            point.draw(canvas, x=x, y=y)
            
            x,y = curve2.point(t2)
            point.draw(canvas, x=x, y=y, size=10, fill_color=None, line_color="r")
    
    
    def draw_intersects_self(self, canvas):
        """Draws self intersection test."""
        
        # init objects
        pather = pero.Pather(fill_color=None, show_cursor=False)
        point = pero.Circle(fill_color="r", line_color="w", size=8)
        
        # init curve
        curve = pero.Bezier(120,50 , 30,150 , 160,150 , 70,50)
        
        # draw curve
        path = pero.Path.from_bezier(curve)
        pather.draw(canvas, path=path)
        
        # draw intersections
        for t1,t2 in curve.intersects():
            
            x,y = curve.point(t1)
            point.draw(canvas, x=x, y=y)
            
            x,y = curve.point(t2)
            point.draw(canvas, x=x, y=y, size=10, fill_color=None, line_color="r")
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init label
        label = pero.Text(text_align=pero.CENTER, x=100, y=220)
        
        # init curve
        curve = pero.Bezier(100,25 , 10,90 , 110,100 , 150,195)
        
        # draw tests
        canvas.set_viewport(20, 20, relative=True)
        self.draw_hull(canvas, curve)
        label.draw(canvas, text="Hull")
        
        canvas.set_viewport(170, 0, relative=True)
        self.draw_slice(canvas, curve)
        label.draw(canvas, text="Slice")
        
        canvas.set_viewport(170, 0, relative=True)
        self.draw_extremes(canvas, curve)
        label.draw(canvas, text="Extremes")
        
        canvas.set_viewport(170, 0, relative=True)
        self.draw_normals(canvas, curve)
        label.draw(canvas, text="Normals")
        
        canvas.set_viewport(170, 0, relative=True)
        self.draw_inflections(canvas, curve)
        label.draw(canvas, text="Inflections")
        
        canvas.set_viewport(170, 0, relative=True)
        self.draw_reduce(canvas, curve)
        label.draw(canvas, text="Reduced")
        
        canvas.set_viewport(20, 270, relative=False)
        self.draw_projections(canvas, curve)
        label.draw(canvas, text="Projections")
        
        canvas.set_viewport(170, 0, relative=True)
        self.draw_cuts(canvas, curve)
        label.draw(canvas, text="XY Cuts")
        
        canvas.set_viewport(170, 0, relative=True)
        self.draw_intersects_line(canvas, curve)
        label.draw(canvas, text="Line Intersections")
        
        canvas.set_viewport(170, 0, relative=True)
        self.draw_intersects_curve(canvas, curve)
        label.draw(canvas, text="Curve Intersections")
        
        canvas.set_viewport(170, 0, relative=True)
        self.draw_intersects_self(canvas)
        label.draw(canvas, text="Self Intersections")


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Bezier", 1100, 550)
