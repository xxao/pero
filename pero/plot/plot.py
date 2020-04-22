#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. import colors
from ..enums import *
from ..properties import *
from ..drawing import Graphics, Frame, Path
from ..scales import OrdinalScale
from .enums import PLOT_TAG, ANNOTS_Z, GRID_Z, LABELS_Z, LEGEND_Z, SERIES_Z, TITLE_Z
from .graphics import InGraphics, OutGraphics
from .axes import Axis
from .grid import Grid
from .legend import Legend
from .title import Title
from .labels import Labels
from .annotation import Annotation
from .rangebar import RangeBar
from .series import Series


class Plot(Graphics):
    """
    This class provides main functionality to construct and draw Cartesian plot.
    
    By default the plot already contains x and y axes and corresponding grids.
    Additional objects can be added by using 'add' method. If you replace
    default objects by your own, it is recommended to use corresponding property
    name as tag (e.g. use 'x_axis' for x-axis).
    
    Main x and y axes needs to be initialized together with the plot (i.e. they
    should be provided via plot constructor) since other objects will be linked
    to them.
    
    For each additional non-axis object, dependent axis/axes should be
    specified, to share the scale. If an object is dependent on just one scale
    it must contain 'scale' property. If an object is dependent on two axes it
    must contain 'x_scale' and 'y_scale' properties.
    
    All the objects added into the plot must have the 'tag' property set to a
    unique string identifier. This value must not be change later!
    
    To position multiple plots onto a single canvas, the main plot coordinates
    can be specified as 'x' and 'y' for top-left corner and 'width' and 'height'
    for size. If not provided, full canvas is used. In addition, exact
    coordinates of the inside area of the plot can be specified as 'plot_x1' for
    left edge, 'plot_x2' for right edge, 'plot_y1' for top edge and 'plot_y2'
    for bottom edge. These can be used to nicely align multiple plots in a grid.
    The edges, which are not specified are calculated automatically using
    available space.
    
    Properties:
        
        x: int or float
            Specifies the x-coordinate of the top-left corner
        
        y: int or float
            Specifies the y-coordinate of the top-left corner
        
        width: int, float or UNDEF
            Specifies the full plot width. If set to UNDEF the full area of
            given canvas is used.
        
        height: int, float or UNDEF
            Specifies the full plot height. If set to UNDEF the full area of
            given canvas is used.
        
        padding: int, float or tuple
            Specifies the inner space of the plot as a single value or values
            for individual sides starting from top.
        
        plot_x1: int, float or UNDEF
            Specifies the fixed x-coordinate of the left edge of the inside
            area. If not provided it is determined automatically by plot
            graphics.
        
        plot_x2: int, float or UNDEF
            Specifies the fixed x-coordinate of the right edge of the inside
            area. If not provided it is determined automatically by plot
            graphics.
        
        plot_y1: int, float or UNDEF
            Specifies the fixed y-coordinate of the top edge of the inside area.
            If not provided it is determined automatically by plot graphics.
        
        plot_y2: int, float or UNDEF
            Specifies the fixed y-coordinate of the bottom edge of the inside
            area. If not provided it is determined automatically by plot
            graphics.
        
        bgr_line properties:
            Includes pero.LineProperties to specify the full plot outline.
        
        bgr_fill properties:
            Includes pero.FillProperties to specify the full plot fill.
        
        plot_line properties:
            Includes pero.LineProperties to specify the inside area outline.
        
        plot_fill properties:
            Includes pero.FillProperties to specify the inside area fill.
        
        palette: pero.Palette, tuple, str
            Specifies the default color palette as a sequence of colors,
            pero.Palette or palette name. This is used to automatically
            provide new color for data series.
        
        title: pero.plot.Title, None or UNDEF
            Specifies the title display graphics.
        
        legend: pero.plot.Legend, None or UNDEF
            Specifies the legend display graphics.
        
        labels: pero.plot.Labels, None or UNDEF
            Specifies the labels display graphics.
        
        x_axis: pero.plot.Axis
            Specifies the x-axis graphics.
        
        y_axis: pero.plot.Axis
            Specifies the y-axis graphics.
        
        x_grid: pero.plot.Grid, None or UNDEF
            Specifies the x-axis grid-lines graphics.
        
        y_grid: pero.plot.Grid, None or UNDEF
            Specifies the y-axis grid-lines graphics.
        
        x_rangebar: pero.plot.RangeBar, None or UNDEF
            Specifies the x-data range bar graphics.
        
        y_rangebar: pero.plot.RangeBar, None or UNDEF
            Specifies the y-data range bar graphics.
    """
    
    x = NumProperty(0, dynamic=False)
    y = NumProperty(0, dynamic=False)
    width = NumProperty(UNDEF, dynamic=False)
    height = NumProperty(UNDEF, dynamic=False)
    padding = QuadProperty(10, dynamic=False)
    
    plot_x1 = NumProperty(UNDEF, dynamic=False)
    plot_x2 = NumProperty(UNDEF, dynamic=False)
    plot_y1 = NumProperty(UNDEF, dynamic=False)
    plot_y2 = NumProperty(UNDEF, dynamic=False)
    
    bgr_line = Include(LineProperties, prefix="bgr", dynamic=False, line_width=0)
    bgr_fill = Include(FillProperties, prefix="bgr", dynamic=False, fill_color="#fff")
    
    plot_line = Include(LineProperties, prefix="plot", dynamic=False, line_color="#000")
    plot_fill = Include(FillProperties, prefix="plot", dynamic=False, fill_color=None)
    
    palette = PaletteProperty(colors.Pero, dynamic=False, nullable=True)
    
    title = Property(UNDEF, types=(Title,), dynamic=False, nullable=True)
    legend = Property(UNDEF, types=(Legend,), dynamic=False, nullable=True)
    labels = Property(UNDEF, types=(Labels,), dynamic=False, nullable=True)
    x_axis = Property(UNDEF, types=(Axis,), dynamic=False)
    y_axis = Property(UNDEF, types=(Axis,), dynamic=False)
    x_grid = Property(UNDEF, types=(Grid,), dynamic=False, nullable=True)
    y_grid = Property(UNDEF, types=(Grid,), dynamic=False, nullable=True)
    x_rangebar = Property(UNDEF, types=(RangeBar,), dynamic=False, nullable=True)
    y_rangebar = Property(UNDEF, types=(RangeBar,), dynamic=False, nullable=True)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Plot."""
        
        # init main graphics
        if 'title' not in overrides:
            overrides['title'] = Title(tag='title', position=POS_TOP, z_index=TITLE_Z)
        
        if 'legend' not in overrides:
            overrides['legend'] = Legend(tag='legend', z_index=LEGEND_Z)
        
        if 'labels' not in overrides:
            overrides['labels'] = Labels(tag='labels', z_index=LABELS_Z)
        
        if 'x_axis' not in overrides:
            overrides['x_axis'] = Axis(tag='x_axis', position=POS_BOTTOM, level=1, margin=0)
        
        if 'y_axis' not in overrides:
            overrides['y_axis'] = Axis(tag='y_axis', position=POS_LEFT, level=2, margin=0)
        
        if 'x_grid' not in overrides:
            overrides['x_grid'] = Grid(tag='x_grid', z_index=GRID_Z)
        
        if 'y_grid' not in overrides:
            overrides['y_grid'] = Grid(tag='y_grid', z_index=GRID_Z)
        
        if 'x_rangebar' not in overrides:
            overrides['x_rangebar'] = RangeBar(tag='x_rangebar', position=POS_TOP)
        
        if 'y_rangebar' not in overrides:
            overrides['y_rangebar'] = RangeBar(tag='y_rangebar', position=POS_RIGHT)
        
        # init base
        super().__init__(**overrides)
        
        # init containers
        self._graphics = {}
        self._axes = []
        self._series = []
        self._annots = []
        self._mapping = {}
        self._frame = Frame(0, 0, 1, 1)
        
        # register main graphics
        self._init_graphics()
        
        # init color scale
        self._init_colors()
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_plot_property_changed)
    
    
    @property
    def axes(self):
        """
        Gets all available axes.
        
        Returns:
            (pero.plot.Axis,)
                All available axes.
        """
        
        return self._axes[:]
    
    
    @property
    def series(self):
        """
        Gets all available series.
        
        Returns:
            (pero.plot.Series,)
                All available series.
        """
        
        return self._series[:]
    
    
    def get_frame(self, tag=PLOT_TAG):
        """
        Gets bounding box of an object specified by given tag. In addition, a
        frame for the main plot area is also available using the pero.plot.PLOT_TAG
        enum value.
        
        Args:
            tag: str
                Object's unique tag.
        
        Returns:
            pero.Frame or None
                Bounding box of specified object or None if object not known.
        """
        
        # data frame
        if tag == PLOT_TAG:
            return self._frame
        
        # object frame
        obj = self.get_obj(tag)
        return obj.frame if obj is not None else None
    
    
    def get_obj(self, tag):
        """
        Gets object for given tag.
        
        Args:
            tag: str
                Object's unique tag.
        
        Returns:
            pero.Graphics or None
                Requested object or None if not available.
        """
        
        return self._graphics.get(tag, None)
    
    
    def get_obj_axes(self, obj):
        """
        Gets the axes associated with specified object.
        
        Args:
            obj: str or pero.Graphics
                Object's unique tag or the object itself.
        
        Returns:
            (str,)
                Associated axes tags.
        """
        
        tag = obj.tag if isinstance(obj, Graphics) else obj
        
        mapping = self._mapping.get(tag, None)
        if not mapping:
            return []
        
        return tuple(mapping.keys())
    
    
    def get_obj_below(self, x, y):
        """
        Gets the top-most object for which given coordinates fall into its
        bounding box. This method checks only the outside objects. For inside
        plot area it always returns the pero.plot.PLOT_TAG.
        
        Args:
            x: int or float
                X-coordinate of the point.
            
            y: int or float
                Y-coordinate of the point.
        
        Returns:
            pero.Graphics, str or None
                Corresponding object, pero.plot.PLOT_TAG or None.
        """
        
        # check plot area first
        if self._frame.contains(x, y):
            return PLOT_TAG
        
        # get all matching objects
        objs = [o for o in self._graphics.values() if o.frame.contains(x, y)]
        if not objs:
            return None
        
        # sort by z-axis
        objs.sort(key=lambda d: d.z_index, reverse=True)
        
        return objs[0]
    
    
    def get_series_limits(self, axis, x_range=None, y_range=None, exact=False):
        """
        Gets minimum and maximum value from all visible series connected to
        specified axis. The range can be used to crop data in particular
        dimension (e.g. provide x_range to get minimum and maximum values of the
        cropped data in y dimension).
        
        Args:
            axis: str or pero.plot.Axis
                Axis's unique tag or the axis itself.
            
            x_range: (float, float) or None
                X-range limits.
            
            y_range: (float, float) or None
                Y-range limits.
            
            exact: bool
                If set to True, the limits are retrieved for data only, i.e. any
                additional space like margin is ignored.
        
        Returns:
            (float, float)
                Minimum and maximum value of the axis from related series.
        """
        
        minimum = None
        maximum = None
        
        # check axis
        if axis is None:
            return minimum, maximum
        
        # get axis
        if not isinstance(axis, Axis):
            axis = self._graphics[axis]
        
        # add series
        for series in self._series:
            
            # skip invisible
            if not series.visible:
                continue
            
            # get series axes
            mappings = self._mapping.get(series.tag, {})
            
            # check if dependent
            if axis.tag not in mappings:
                continue
            
            # get axis mapping
            mapping = mappings[axis.tag]
            
            # use specific function
            if mapping['limits'] is not None:
                
                limits = mapping['limits'](x_range, y_range, exact)
                if limits is None:
                    continue
                
                lo, hi = limits
            
            # get standard limits
            else:
                
                limits = series.get_limits(x_range=x_range, y_range=y_range, exact=exact)
                if limits is None:
                    continue
                
                limits = limits[0] if axis.position in (POS_TOP, POS_BOTTOM) else limits[1]
                if limits is None:
                    continue
                
                lo, hi = limits
            
            # update range
            if minimum is None or lo < minimum:
                minimum = lo
            
            if maximum is None or hi > maximum:
                maximum = hi
        
        return minimum, maximum
    
    
    def get_parent_axes(self, axis):
        """
        Gets parent axes, which are used by any visible series together with
        given child axis. Parent axes must have the 'level' property lower than
        given axis.
        
        Args:
            axis: str or pero.plot.Axis
                Axis's unique tag or the axis itself.
        
        Returns:
            (pero.plot.Axis,)
                Parent axes.
        """
        
        # get axis
        if not isinstance(axis, Axis):
            axis = self._graphics[axis]
        
        # init buffer
        parents = set()
        
        # check series
        for series in self._series:
            
            # skip invisible
            if not series.visible:
                continue
            
            # get series axes
            mappings = self._mapping.get(series.tag, {})
            
            # check if dependent
            if axis.tag not in mappings:
                continue
            
            # get parents
            for item_tag in mappings:
                
                # check same axis
                if item_tag == axis.tag:
                    continue
                
                # get axis
                item = self._graphics[item_tag]
                
                # check if parent
                if item.level < axis.level:
                    parents.add(item)
        
        return list(parents)
    
    
    def get_child_axes(self, axis):
        """
        Gets child axes, which are used by any visible series together with
        given parent axis. Parent axes must have the 'level' property higher
        than given axis.
        
        Args:
            axis: str or pero.plot.Axis
                Axis's unique tag or the axis itself.
        
        Returns:
            (pero.plot.Axis,)
                Child axes.
        """
        
        # get axis
        if not isinstance(axis, Axis):
            axis = self._graphics[axis]
        
        # init buffer
        children = set()
        
        # check series
        for series in self._series:
            
            # skip invisible
            if not series.visible:
                continue
            
            # get series axes
            mappings = self._mapping.get(series.tag, {})
            
            # check if dependent
            if axis.tag not in mappings:
                continue
            
            # get children
            for item_tag in mappings:
                
                # check same axis
                if item_tag == axis.tag:
                    continue
                
                # get axis
                item = self._graphics[item_tag]
                
                # check if child
                if item.level > axis.level:
                    children.add(item)
        
        return list(children)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the plot."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        
        # get size from canvas
        if width is UNDEF:
            width = canvas.viewport.width
        if height is UNDEF:
            height = canvas.viewport.height
        
        # init objects
        self._init_frames(canvas, source, overrides)
        self._init_objects(canvas, source, overrides)
        
        # draw main bgr
        canvas.set_pen_by(self, prefix="bgr", source=source, overrides=overrides)
        canvas.set_brush_by(self, prefix="bgr", source=source, overrides=overrides)
        canvas.draw_rect(x, y, width, height)
        
        # refuse to draw plot if "negative" size
        if self._frame.reversed:
            return
        
        # draw plot bgr
        canvas.line_width = 0
        canvas.set_brush_by(self, prefix="plot", source=source, overrides=overrides)
        canvas.draw_rect(*self._frame.rect)
        
        # get objects
        objects = tuple(self._graphics.values())
        
        out_objects = [o for o in objects if isinstance(o, OutGraphics)]
        out_objects.sort(key=lambda o: o.z_index)
        
        in_objects = [o for o in objects if isinstance(o, InGraphics)]
        in_objects.sort(key=lambda o: o.z_index)
        
        # separate grids and other inside objects
        grids = [o for o in in_objects if o.visible and isinstance(o, Grid)]
        others = [o for o in in_objects if o.visible and not isinstance(o, Grid)]
        grids_z = grids[0].z_index if grids else GRID_Z
        
        # clip plot area
        with canvas.clip(Path().rect(*self._frame.rect)):
            
            # draw inside objects behind grids
            for obj in others:
                if obj.z_index < grids_z:
                    obj.draw(canvas)
            
            # draw grids
            for grid in grids:
                grid.draw_minor(canvas)
            for grid in grids:
                grid.draw_major(canvas)
            
            # draw inside objects above grids
            for obj in others:
                if obj.z_index >= grids_z:
                    obj.draw(canvas)
        
        # draw plot outline
        canvas.fill_style = FILL_STYLE_TRANS
        canvas.set_pen_by(self, prefix="plot", source=source, overrides=overrides)
        canvas.draw_rect(*self._frame.rect)
        
        # draw outside objects
        for obj in out_objects:
            if obj.visible:
                obj.draw(canvas)
        
        # draw debug rectangles
        # self._draw_frames(canvas)
    
    
    def add(self, obj):
        """
        Adds additional graphics to the plot. Depending on the object base class
        it will be used as an inside or outside graphics automatically.
        
        Args:
            obj: pero.plot.InGraphics or pero.plot.OutGraphics
                Object to be added.
        """
        
        # check type
        if not isinstance(obj, (InGraphics, OutGraphics)):
            message = "Object must be of type pero.InGraphics or pero.OutGraphics! -> %s" % type(obj)
            raise TypeError(message)
        
        # check tag
        if not obj.tag or obj.tag in self._graphics or obj.tag == PLOT_TAG:
            message = "Object must have unique tag specified."
            raise ValueError(message)
        
        # check z_index
        if obj.z_index is UNDEF:
            self._init_z_index(obj)
        
        # add object
        self._graphics[obj.tag] = obj
        
        # add to axes
        if isinstance(obj, Axis):
            self._axes.append(obj)
        
        # add to series
        elif isinstance(obj, Series):
            self._series.append(obj)
        
        # add to annotations
        elif isinstance(obj, Annotation):
            self._annots.append(obj)
    
    
    def remove(self, obj):
        """
        Removes object corresponding to given tag. Note that axis cannot be
        removed as long as any other object or series is still linked to it.
        
        Args:
            obj: str or pero.Graphics
                Object's unique tag or the object itself.
        """
        
        # get object tag
        tag = obj.tag if isinstance(obj, Graphics) else obj
        
        # get object
        obj = self._graphics.get(tag, None)
        if obj is None:
            message = "Cannot find object by tag '%s'!" % tag
            raise ValueError(message)
        
        # check axes connections
        if isinstance(obj, Axis):
            axes = [y for x in self._mapping.values() for y in x]
            if tag in axes:
                message = "Axis '%s' is used by another graphics and cannot be removed!" % tag
                raise ValueError(message)
        
        # remove axis
        if obj in self._axes:
            self._axes.remove(obj)
        
        # remove series
        elif obj in self._series:
            self._series.remove(obj)
        
        # remove annotation
        elif obj in self._annots:
            self._annots.remove(obj)
        
        # remove mapping
        if tag in self._mapping:
            del self._mapping[tag]
        
        # remove graphics
        del self._graphics[tag]
    
    
    def map(self, obj, axis, scale=None, limits=None):
        """
        Maps object to specific axis to share and update the scale.
        
        If a custom function is provided for 'limits' the following signature is
        expected: func(x_range:(float, float), y_range:(float, float), exact:bool) -> (float, float)
        
        Args:
            obj: str or pero.Graphics
                Unique tag of the object or the object itself.
            
            axis: str or pero.plot.Axis
                Unique tag of the axis or the axis itself.
            
            scale: str or None
                Scale property name of the object to be synced with the axis.
            
            limits: callable or None
                Function to be used to get specific data range for the axis.
        """
        
        # check axis
        if axis is None:
            return
        
        # get objects
        if not isinstance(obj, Graphics):
            obj = self._graphics[obj]
        
        if not isinstance(axis, Graphics):
            axis = self._graphics[axis]
        
        # check object
        if obj.tag not in self._graphics:
            message = "Cannot find object by tag '%s'!" % obj.tag
            raise ValueError(message)
        
        # check axis
        if axis.tag not in (x.tag for x in self._axes):
            message = "Cannot find axis by tag '%s'!" % axis.tag
            raise ValueError(message)
        
        # check scale property
        if scale is not None:
            
            if not obj.has_property(scale):
                message = "Object doesn't have the property '%s'!" % scale
                raise ValueError(message)
            
            if not axis.has_property('scale'):
                raise ValueError("Axis doesn't have the 'scale' property!")
        
        # get existing mapping
        mapping = self._mapping.get(obj.tag, {})
        
        # add/replace by given axis
        mapping[axis.tag] = {
            'scale': scale,
            'limits': limits}
        
        # store new mapping
        self._mapping[obj.tag] = mapping
    
    
    def annotate(self, annotation, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to add annotations to the plot.
        
        Using the axes, given annotation is connected to particular axis
        scale, so it is automatically scaled to device coordinates.
        
        The order in which the annotations are drawn is not guaranteed so if it
        is important, the z_index property should be set.
        
        Args:
            annotation: pero.plot.Annotation or pero.Glyph
                Annotation to be added.
            
            x_axis: str or pero.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or pero.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the annotation.
        
        Returns:
            pero.plot.Annotation
                Final annotation object.
        """
        
        # create annotation
        if not isinstance(annotation, Annotation):
            annotation = Annotation(glyph=annotation, **overrides)
        
        # set new properties
        elif overrides:
            annotation.set_properties(overrides, True)
        
        # add object
        self.add(annotation)
        
        # map axes
        self.map(annotation, x_axis, scale='x_scale')
        self.map(annotation, y_axis, scale='y_scale')
        
        return annotation
    
    
    def plot(self, series, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to add data series to the plot.
        
        Using the axes tags, given series is connected to particular axes'
        scales, so it is automatically scaled to device coordinates.
        
        The order in which the series are drawn is not guaranteed so if it is
        important, the z_index property should be set.
        
        Args:
            series: pero.plot.Series
                Series data to be added.
            
            x_axis: str or pero.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or pero.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the series.
        """
        
        # check type
        if not isinstance(series, Series):
            message = "Series must be of type pero.plot.Series! -> %s" % type(series)
            raise TypeError(message)
        
        # set new properties
        if overrides:
            series.set_properties(overrides, True)
        
        # set color
        if series.color is UNDEF and self._colors:
            series.color = self._colors.scale(series.tag)
        
        # add object
        self.add(series)
        
        # map axes
        self.map(series, x_axis, scale='x_scale')
        self.map(series, y_axis, scale='y_scale')
    
    
    def zoom(self, axis=None, minimum=None, maximum=None, propagate=True):
        """
        Sets given range to specific axis.
        
        If 'axis' is set to None, given range will be applied to all axes.
        This make only sense if minimum and maximum are both set to None, so all
        the axes will be set to cover full range of connected data series.
        
        If minimum or maximum is set to None, the value will be set by maximum
        or minimum value to cover full range of connected data series.
        
        Args:
            axis: str or pero.plot.Axis or None
                Unique tag of the axis or the axis itself.
            
            minimum: float or None
                Minimum value to be set.
            
            maximum: float or None
                Maximum value to be set.
            
            propagate: bool
                If set to True, dependent axes will be zoomed accordingly.
        """
        
        # get axes
        if axis is None:
            axes = self._axes[:]
        elif isinstance(axis, Axis):
            axes = [axis]
        else:
            axis = self._graphics[axis]
            axes = [axis]
        
        # sort axes by level
        axes.sort(key=lambda a: a.level)
        
        # set axes
        for item in axes:
            
            # set limits
            lo, hi = minimum, maximum
            
            # get limits from series
            if lo is None and hi is None:
                lo, hi = self.get_series_limits(item)
            
            # check limits
            if lo is None:
                lo = item.scale.in_range[0]
            if hi is None:
                hi = item.scale.in_range[1]
            
            # finalize axis
            self.finalize_axis(item, lo, hi)
        
        # propagate main axis change
        if propagate and axis is not None:
            self.finalize_zoom(axis)
    
    
    def finalize_zoom(self, axes):
        """
        For each given axis this method finalizes all child axes according to
        individual settings (e.g. autoscale).
        
        Args:
            axes: (str,) or (pero.plot.Axis,)
                Unique tags of the axes or the axes itself.
        """
        
        # check for single axis
        if isinstance(axes, (str, Axis)):
            axes = (axes,)
        
        # get axes
        axes = list(axes)
        for i, axis in enumerate(axes):
            if not isinstance(axis, Axis):
                axes[i] = self._graphics[axis]
        
        # ensure unique and sort
        axes = list(set(axes))
        axes.sort(key=lambda a: a.level)
        
        # get all related axes
        related = list(set(c for p in axes for c in self.get_child_axes(p)))
        related.sort(key=lambda a: a.level)
        
        # init already changed
        changed = set([a.tag for a in axes])
        
        # autoscale related axes
        for axis in related:
            
            # skip changed or independent
            if axis.tag in changed or axis.static or not axis.autoscale:
                continue
            
            # get parent axes
            parents = self.get_parent_axes(axis)
            if not parents:
                continue
            
            # get crop
            x_range = None
            y_range = None
            
            for parent in parents:
                
                if parent.position in (POS_TOP, POS_BOTTOM):
                    x_range = parent.scale.in_range
                
                elif parent.position in (POS_LEFT, POS_RIGHT):
                    y_range = parent.scale.in_range
            
            # get axis limits
            start, end = self.get_series_limits(axis, x_range, y_range, exact=False)
            if start is None or end is None:
                continue
            
            # finalize axis
            self.finalize_axis(axis, start, end)
    
    
    def finalize_axis(self, axis, start, end):
        """
        Finalizes range for given axis according to its settings. This ensures
        specified limits, margins etc.
        
        Args:
            axis: str or pero.plot.Axis
                Unique tag of the axis or the axis itself.
            
            start: float or None
                Start value to be set.
            
            end: float or None
                End value to be set.
        """
        
        # get axis
        if not isinstance(axis, Axis):
            axis = self._graphics[axis]
        
        # get range
        range_min, range_max = self.get_series_limits(axis.tag)
        
        # use full range if not set
        if start is None or end is None:
            start = range_min
            end = range_max
        
        # check range
        if start is None or end is None:
            start = axis.empty_range[0]
            end = axis.empty_range[1]
        
        # check data limits
        if axis.check_limits and range_min is not None and range_max is not None:
            
            if start < range_min and end > range_max:
                start = range_min
                end = range_max
            
            elif start < range_min:
                shift = range_min - start
                start += shift
                end += shift
            
            elif end > range_max:
                shift = end - range_max
                start -= shift
                end -= shift
        
        # check required values
        if axis.includes:
            
            incl_min = min(axis.includes)
            incl_max = max(axis.includes)
            
            if start > incl_min:
                start = incl_min
            
            if end < incl_max:
                end = incl_max
        
        # check range
        if start == end and start == 0:
            end = 1.
        
        # check symmetry
        if axis.symmetric:
            maximum = max(abs(start), abs(end))
            start, end = -maximum, maximum
        
        # check range
        if start == end:
            start -= 0.1*start
            end += 0.1*end
        
        # apply to axis
        axis.scale.in_range = (start, end)
    
    
    def show(self, title=None, width=None, height=None, backend=None, **options):
        """
        Shows current plot as static image in available viewer app.
        
        Note that is just a convenient scripting shortcut and this method cannot
        be used if the plot is already part of any UI app.
        
        Args:
            title: str or None
                Viewer frame title. If set to None, current plot title is used.
            
            width: float or None
                Image width in device units. If set to None, current plot width
                is used.
            
            height: float or None
                Image height in device units. If set to None, current plot
                height is used.
            
            backend: pero.BACKEND or None
                Specific backend to be used. The value must be an item from the
                pero.BACKEND enum.
            
            options: str:any pairs
                Additional parameters for specific backend.
        """
        
        # get title
        if title is None and self.title:
            title = self.title.text
        
        # get size
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        
        # show plot
        super().show(title, width, height, backend, **options)
    
    
    def export(self, path, width=None, height=None, backend=None, **options):
        """
        Draws current plot into specified file using the format determined
        automatically from the file extension.
        
        Note that is just a convenient scripting shortcut and this method cannot
        be used if the plot is already part of any UI app.
        
        Args:
            path: str
                Full path of a file to save the image into.
            
            width: float or None
                Image width in device units. If set to None, current plot width
                is used.
            
            height: float or None
                Image height in device units. If set to None, current plot
                height is used.
            
            backend: pero.BACKEND or None
                Specific backend to be used. The value must be an item from the
                pero.BACKEND enum.
            
            options: str:any pairs
                Additional parameters for specific backend.
        """
        
        # get size
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        
        # export plot
        super().export(path, width, height, backend, **options)
    
    
    def view(self, title=None, width=None, height=None, backend=None, **options):
        """
        Shows current plot as interactive viewer app.
        
        Note that is just a convenient scripting shortcut and this method cannot
        be used if the plot is already part of any UI app.
        
        Args:
            title: str or None
                Viewer frame title. If set to None, current plot title is used.
            
            width: float or None
                Image width in device units. If set to None, current plot width
                is used.
            
            height: float or None
                Image height in device units. If set to None, current plot
                height is used.
            
            backend: pero.BACKEND or None
                Specific backend to be used. The value must be an item from the
                pero.BACKEND enum.
            
            options: str:any pairs
                Additional parameters for specific backend.
        """
        
        # get title
        if title is None and self.title:
            title = self.title.text
        
        # get size
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        
        # init control
        from .control import PlotControl
        control = PlotControl(graphics=self)
        
        # show viewer
        control.show(title, width, height, backend, **options)
    
    
    def _init_frames(self, canvas, source, overrides):
        """Calculates and sets objects frames."""
        
        # clean frames
        for obj in self._graphics.values():
            obj.frame = Frame(0, 0, 0, 0)
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        padding = self.get_property('padding', source, overrides)
        
        plot_x1 = self.get_property('plot_x1', source, overrides)
        plot_x2 = self.get_property('plot_x2', source, overrides)
        plot_y1 = self.get_property('plot_y1', source, overrides)
        plot_y2 = self.get_property('plot_y2', source, overrides)
        
        # get size from canvas
        if width is UNDEF:
            width = canvas.viewport.width
        if height is UNDEF:
            height = canvas.viewport.height
        
        # get objects
        objects = tuple(self._graphics.values())
        
        out_objects = [o for o in objects if isinstance(o, OutGraphics)]
        out_objects.sort(key=lambda o: o.z_index)
        
        in_objects = [o for o in objects if isinstance(o, InGraphics)]
        in_objects.sort(key=lambda o: o.z_index)
        
        # init buffers
        left_obj = []
        left_extents = []
        left_margins = [0]
        
        right_obj = []
        right_extents = []
        right_margins = [0]
        
        top_obj = []
        top_extents = []
        top_margins = [0]
        
        bottom_obj = []
        bottom_extents = []
        bottom_margins = [0]
        
        # get extents and margins
        for obj in out_objects:
            
            if not obj.visible:
                continue
            
            extent = obj.get_extent(canvas)
            position = obj.position
            margin = obj.margin
            
            if not extent:
                continue
            
            if position == POS_LEFT:
                left_obj.append(obj)
                left_extents.append(extent)
                left_margins[-1] = max(margin[1], left_margins[-1])
                left_margins.append(margin[3])
            
            elif position == POS_RIGHT:
                right_obj.append(obj)
                right_extents.append(extent)
                right_margins[-1] = max(margin[3], right_margins[-1])
                right_margins.append(margin[1])
            
            elif position == POS_TOP:
                top_obj.append(obj)
                top_extents.append(extent)
                top_margins[-1] = max(margin[2], top_margins[-1])
                top_margins.append(margin[0])
            
            elif position == POS_BOTTOM:
                bottom_obj.append(obj)
                bottom_extents.append(extent)
                bottom_margins[-1] = max(margin[0], bottom_margins[-1])
                bottom_margins.append(margin[2])
            
            else:
                message = "Unknown position '%s' for '%s' object." % (position, obj.tag)
                raise ValueError(message)
        
        # init inside frame
        if plot_x1 is UNDEF:
            plot_x1 = x + padding[3] + sum(left_extents) + sum(left_margins[:-1])
        
        if plot_x2 is UNDEF:
            plot_x2 = x - padding[1] + width - sum(right_extents) - sum(right_margins[:-1])
        
        if plot_y1 is UNDEF:
            plot_y1 = y + padding[0] + sum(top_extents) + sum(top_margins[:-1])
        
        if plot_y2 is UNDEF:
            plot_y2 = y - padding[2] + height - sum(bottom_extents) - sum(bottom_margins[:-1])
        
        self._frame = Frame(plot_x1, plot_y1, plot_x2-plot_x1, plot_y2-plot_y1)
        
        # make frame for left objects
        shift = plot_x1 - left_margins[0]
        for i, obj in enumerate(left_obj):
            extent = left_extents[i]
            obj.frame = Frame(shift-extent, plot_y1, extent, plot_y2-plot_y1)
            shift -= extent + left_margins[i+1]
        
        # make frame for right objects
        shift = plot_x2 + right_margins[0]
        for i, obj in enumerate(right_obj):
            extent = right_extents[i]
            obj.frame = Frame(shift, plot_y1, extent, plot_y2-plot_y1)
            shift += extent + right_margins[i+1]
        
        # make frame for top objects
        shift = plot_y1 - top_margins[0]
        for i, obj in enumerate(top_obj):
            extent = top_extents[i]
            obj.frame = Frame(plot_x1, shift-extent, plot_x2-plot_x1, extent)
            shift -= extent + top_margins[i+1]
        
        # make frame for bottom objects
        shift = plot_y2 + bottom_margins[0]
        for i, obj in enumerate(bottom_obj):
            extent = bottom_extents[i]
            obj.frame = Frame(plot_x1, shift, plot_x2-plot_x1, extent)
            shift += extent + bottom_margins[i+1]
        
        # set plot inside frame to inside objects
        for obj in in_objects:
            obj.frame = self._frame
    
    
    def _init_objects(self, canvas, source, overrides):
        """Sets associated scales and initializes all objects."""
        
        # get objects
        objects = tuple(self._graphics.values())
        
        out_objects = [o for o in objects if isinstance(o, OutGraphics)]
        out_objects.sort(key=lambda o: o.z_index)
        
        in_objects = [o for o in objects if isinstance(o, InGraphics)]
        in_objects.sort(key=lambda o: o.z_index)
        
        # set scales by axes
        for obj in objects:
            
            # get associate axes
            axes = self._mapping.get(obj.tag, {})
            for axis_tag in axes:
                
                # set scale to object
                scale_prop = axes[axis_tag]['scale']
                if scale_prop:
                    axis = self._graphics[axis_tag]
                    obj.set_property(scale_prop, axis.scale)
        
        # init outside objects
        for obj in out_objects:
            obj.initialize(canvas, self)
        
        # init inside objects
        for obj in in_objects:
            obj.initialize(canvas, self)
    
    
    def _init_graphics(self):
        """Registers main objects."""
        
        # register objects
        if self.title:
            self.add(self.title)
        
        if self.legend:
            self.add(self.legend)
        
        if self.labels:
            self.add(self.labels)
        
        if self.x_axis:
            self.add(self.x_axis)
        
        if self.y_axis:
            self.add(self.y_axis)
        
        if self.x_grid and self.x_axis:
            self.add(self.x_grid)
            self.map(self.x_grid, self.x_axis, scale='scale')
        
        if self.y_grid and self.y_axis:
            self.add(self.y_grid)
            self.map(self.y_grid, self.y_axis, scale='scale')
        
        if self.x_rangebar and self.x_axis:
            self.add(self.x_rangebar)
            self.map(self.x_rangebar, self.x_axis, scale='scale')
        
        if self.y_rangebar and self.y_axis:
            self.add(self.y_rangebar)
            self.map(self.y_rangebar, self.y_axis, scale='scale')
    
    
    def _init_colors(self):
        """Initializes default color scale."""
        
        # get palette
        palette = self.palette
        if not palette:
            self.palette = colors.Pero
        
        # init color scale
        self._colors = OrdinalScale(
            out_range = self.palette,
            implicit = True,
            recycle = True)
    
    
    def _init_z_index(self, obj):
        """Initializes z-index of given object."""
        
        # series
        if isinstance(obj, Series):
            z_index = [o.z_index for o in self._series if o.z_index]
            obj.z_index = max(SERIES_Z, 1 + max(z_index) if z_index else SERIES_Z)
        
        # annotations
        elif isinstance(obj, Annotation):
            z_index = [o.z_index for o in self._annots if o.z_index]
            obj.z_index = max(ANNOTS_Z, 1 + max(z_index) if z_index else ANNOTS_Z)
        
        # outsides
        elif isinstance(obj, OutGraphics):
            z_index = [o.z_index for o in self._graphics.values() if isinstance(o, OutGraphics) and not isinstance(o, Title)]
            obj.z_index = 1 + max(z_index) if z_index else 0
    
    
    def _draw_frames(self, canvas):
        """Draws all outside objects frames (for debugging)."""
        
        # init color scale
        color_scale = OrdinalScale(
            out_range = colors.Pero,
            implicit = True,
            recycle = True)
        
        # set pen and brush
        canvas.line_width = 1
        canvas.line_style = LINE_STYLE_SOLID
        canvas.fill_style = FILL_STYLE_SOLID
        
        # draw frames
        for tag, obj in self._graphics.items():
            
            # set color
            color = color_scale.scale(tag)
            canvas.line_color = color.opaque(0.5)
            canvas.fill_color = color.opaque(0.25)
            
            # draw frame
            canvas.draw_rect(*obj.frame.rect)
            print(tag, ":", obj.frame)
    
    
    def _on_plot_property_changed(self, evt):
        """Called after any property has changed."""
        
        # color palette changed
        if evt.name == 'palette':
            self._init_colors()
        
        # main objects
        if evt.name in ('title', 'legend', 'labels', 'x_axis', 'y_axis', 'x_grid', 'y_grid', 'x_rangebar', 'y_rangebar'):
            
            # remove old
            if evt.old_value:
                self.remove(evt.old_value.tag)
            
            # register new
            if evt.new_value:
                
                # register new
                self.add(evt.new_value)
                
                # map to axes
                if evt.name == 'x_grid':
                    self.map(evt.new_value, self.x_axis, scale='scale')
                
                elif evt.name == 'y_grid':
                    self.map(evt.new_value, self.y_axis, scale='scale')
                
                elif evt.name == 'x_rangebar':
                    self.map(evt.new_value, self.x_axis, scale='scale')
                
                elif evt.name == 'y_rangebar':
                    self.map(evt.new_value, self.y_axis, scale='scale')
