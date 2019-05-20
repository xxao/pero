#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for path details drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init paths
        path1 = pero.Path.from_svg("""
            M60.51,6.398
            C55.927,6.419 51.549,6.81 47.698,7.492
            C36.351,9.496 34.291,13.692 34.291,21.429
            L34.291,31.648
            L61.104,31.648
            L61.104,35.054
            L34.291,35.054
            L24.229,35.054
            C16.436,35.054 9.613,39.738 7.479,48.648
            C5.017,58.861 4.908,65.234 7.479,75.898
            C9.385,83.836 13.936,89.492 21.729,89.492
            L30.948,89.492
            L30.948,77.242
            C30.948,68.392 38.605,60.585 47.698,60.585
            L74.479,60.585
            C81.934,60.585 87.885,54.447 87.885,46.96
            L87.885,21.429
            C87.885,14.163 81.755,8.704 74.479,7.492
            C69.873,6.725 65.094,6.377 60.51,6.398
            Z
            
            M46.01,14.617
            C48.78,14.617 51.041,16.915 51.041,19.742
            C51.041,22.558 48.78,24.835 46.01,24.835
            C43.231,24.835 40.979,22.558 40.979,19.742
            C40.979,16.915 43.231,14.617 46.01,14.617
            Z""")
        
        path2 = pero.Path.from_svg("""
            M91.229,35.054
            L91.229,46.96
            C91.229,56.191 83.403,63.96 74.479,63.96
            L47.698,63.96
            C40.362,63.96 34.291,70.239 34.291,77.585
            L34.291,103.117
            C34.291,110.383 40.61,114.657 47.698,116.742
            C56.185,119.237 64.324,119.688 74.479,116.742
            C81.229,114.787 87.885,110.854 87.885,103.117
            L87.885,92.898
            L61.104,92.898
            L61.104,89.492
            L101.291,89.492
            C109.084,89.492 111.988,84.056 114.698,75.898
            C117.497,67.499 117.378,59.422 114.698,48.648
            C112.772,40.891 109.094,35.054 101.291,35.054
            L91.229,35.054
            Z
            
            M76.166,99.71
            C78.946,99.71 81.198,101.988 81.198,104.804
            C81.198,107.631 78.946,109.929 76.166,109.929
            C73.397,109.929 71.135,107.631 71.135,104.804
            C71.135,101.988 73.397,99.71 76.166,99.71
            Z""")
        
        # scale paths to fill window
        padding = 20
        width, height = canvas.viewport.wh
        
        bbox = path1.bbox()
        bbox.extend(path2.bbox())
        
        scale = min((width-2*padding)/bbox.w, (height-2*padding)/bbox.h)
        matrix = pero.Matrix().translate(-bbox.cx, -bbox.cy).scale(scale, scale).translate(.5*width, .5*height)
        
        path1.transform(matrix)
        path2.transform(matrix)
        
        # draw paths
        glyph = pero.Pather()
        glyph.draw(canvas, path=path1, fill_color=(48,105,152))
        glyph.draw(canvas, path=path2, fill_color=(255,232,115))


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Path Details", 400, 400)
