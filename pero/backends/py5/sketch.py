#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import py5
from . canvas import Py5Canvas


class ShowSketch(py5.Sketch):
    """Custom helper py5.Sketch to draw and show given graphics."""
    
    
    def __init__(self, graphics, title, width, height, **options):
        """
        Initializes a new instance of ShowSketch.
        
        Args:
            graphics: pero.Graphics
                Graphics to draw.
            
            title: str
                Sketch window title.
            
            width: int
                Sketch size.
            
            height: int
                Sketch height.
            
            options: key:value pairs
                Optional properties passed into canvas creation.
        """
        
        # init buffs
        self._graphics = graphics
        self._title = title
        self._width = width
        self._height = height
        self._options = options
        
        # init base
        super().__init__()
    
    
    def settings(self):
        """Applies main sketch settings."""
        
        self.size(self._width, self._height)
    
    
    def setup(self):
        """Initializes canvas and draws current graphics."""
        
        # set title
        if self._title:
            self.window_title(self._title)
        
        # init py5 graphics
        pg = self.create_graphics(self._width, self._height)
        
        # init canvas
        canvas = Py5Canvas(pg, self, **self._options)
        
        # draw graphics
        with pg.begin_draw():
            self._graphics.draw(canvas)
        
        # finalize image
        self.image(pg, 0, 0)


class ExportSketch(py5.Sketch):
    """Custom helper py5.Sketch to export given graphics."""
    
    
    def __init__(self, graphics, path, width, height, **options):
        """
        Initializes a new instance of ExportSketch.
        
        Args:
            graphics: pero.Graphics
                Graphics to draw.
            
            path: str
                Export path
            
            width: int
                Sketch size.
            
            height: int
                Sketch height.
            
            options: key:value pairs
                Optional properties passed into canvas creation.
        """
        
        # init buffs
        self._graphics = graphics
        self._path = path
        self._width = width
        self._height = height
        self._options = options
        
        # init base
        super().__init__()
    
    
    def settings(self):
        """Applies main sketch settings."""
        
        self.size(self._width, self._height, py5.HIDDEN)
        self.pixel_density(1)
    
    
    def setup(self):
        """Initializes canvas and exports current graphics."""
        
        # export PDF
        if self._path.lower().endswith('.pdf'):
            self._export_pdf()
        
        # export SVG
        elif self._path.lower().endswith('.svg'):
            self._export_svg()
        
        # export raster
        else:
            self._export_raster()
        
        # close window
        self.exit_sketch()
    
    
    def _export_pdf(self):
        """Initializes canvas and exports current graphics as PDF."""
        
        # init py5 graphics
        pg = self.create_graphics(self._width, self._height, py5.PDF, self._path)
        
        # init canvas
        canvas = Py5Canvas(pg, self, **self._options)
        
        # draw graphics
        with self.begin_record(pg):
            self._graphics.draw(canvas)
    
    
    def _export_svg(self):
        """Initializes canvas and exports current graphics as SVG."""
        
        # init py5 graphics
        pg = self.create_graphics(self._width, self._height, py5.SVG, self._path)
        
        # init canvas
        canvas = Py5Canvas(pg, self, **self._options)
        
        # draw graphics
        with self.begin_record(pg):
            self._graphics.draw(canvas)
    
    
    def _export_raster(self):
        """Initializes canvas and exports current graphics as raster."""
        
        # init py5 graphics
        pg = self.create_graphics(self._width, self._height)
        
        # init canvas
        canvas = Py5Canvas(pg, self, **self._options)
        
        # draw graphics
        with pg.begin_draw():
            self._graphics.draw(canvas)
        
        # finalize image
        self.image(pg, 0, 0)
        
        # save image
        pg.save(self._path)
