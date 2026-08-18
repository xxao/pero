#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. enums import *
from .. properties import *
from .. geometry import Path, Frame
from . graphics import Graphics


class Layout(Graphics):
    """
    Layout represents an experimental simple table-like layout manager tool.
    You can define custom layout by specifying rows and columns of fixed or
    relative size. Any pero.Graphics can then be inserted into specific cell.
    
    When the layout is drawn the cells are arranged according to available space
    and specific settings. The exact position of each cell is available via its
    'frame' property.
    
    Each cell graphics is drawn on temporarily modified canvas with specific
    drawing region (view) applied. This allows to use relative coordinates
    within the graphics. The exact position of each cell content is available
    via its 'content' property.
    
    Properties:
        
        x: int or float
            Specifies the x-coordinate of the top-left corner
        
        y: int or float
            Specifies the y-coordinate of the top-left corner
        
        width: int, float or UNDEF
            Specifies the full layout width. If set to UNDEF the full area of
            given canvas is used.
        
        height: int, float or UNDEF
            Specifies the full layout height. If set to UNDEF the full area of
            given canvas is used.
        
        padding: int, float or tuple
            Specifies the inner space of the layout as a single value or values
            for individual sides starting from top.
        
        spacing: int or float
            Specifies the space in-between individual cells.
        
        fill properties:
            Includes pero.FillProperties to specify the background fill.
        
        rows: (pero.Row,) (read-only)
            Gets rows definitions.
        
        cols: (pero.Column,) (read-only)
            Gets columns definitions.
        
        cells: (pero.Cell,) (read-only)
            Gets cells definitions.
    """
    
    x = NumProperty(0)
    y = NumProperty(0)
    width = NumProperty(UNDEF)
    height = NumProperty(UNDEF)
    padding = QuadProperty(0)
    spacing = NumProperty(0)
    
    fill = Include(FillProperties, fill_color="w")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Layout."""
        
        super().__init__(**overrides)
        
        self._rows = []
        self._cols = []
        self._cells = []
        self._grid = []
    
    
    @property
    def rows(self):
        """
        Gets rows definitions.
        
        Returns:
            (pero.Row,)
                Tuple of rows definitions.
        """
        
        return tuple(self._rows)
    
    
    @property
    def cols(self):
        """
        Gets columns definitions.
        
        Returns:
            (pero.Column,)
                Tuple of columns definitions.
        """
        
        return tuple(self._cols)
    
    
    @property
    def cells(self):
        """
        Gets cells definition.
        
        Returns:
            (pero.Cell,)
                Tuple of cells definitions.
        """
        
        return tuple(self._cells)
    
    
    def get_cell(self, row, col):
        """
        Gets the cell at specified layout grid position.
        
        Args:
            row: int
                Row index of requested cell.
            
            col: int
                Column index of requested cell.
        
        Returns:
            pero.Cell or None
                Corresponding cell or None.
        """
        
        return self._grid[row][col]
    
    
    def get_cell_below(self, x, y):
        """
        Gets the cell for which given coordinates fall into its bounding box.
        
        Args:
            x: int or float
                X-coordinate in logical units.
            
            y: int or float
                Y-coordinate in logical units.
        
        Returns:
            pero.Cell or None
                Corresponding cell or None.
        """
        
        for cell in self._cells:
            if cell.frame and cell.frame.contains(x, y):
                return cell
        
        return None
    
    
    def in_cell(self, x, y, row=None, col=None):
        """
        Checks if given coordinates fall into specified cell bounding box.
        
        Args:
            x: int or float
                X-coordinate in logical units.
            
            y: int or float
                Y-coordinate in logical units.
            
            row: int or None
                Row index of the cell to check. If not specified, all rows are
                considered.
            
            col: int or None
                Column index of the cell to check. If not specified, all columns
                are considered.
        
        Returns:
            bool
                True if given coordinates fall into specified bounding box,
                False otherwise.
        """
        
        # get cell
        cell = self.get_cell_below(x, y)
        if cell is None:
            return False
        
        # check row
        if row is not None and cell.row != row:
            return False
        
        # check column
        if col is not None and cell.col != col:
            return False
        
        return True
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw layout cells."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        
        # get size from canvas
        if width is UNDEF:
            width = canvas.viewport.width if canvas else 0
        if height is UNDEF:
            height = canvas.viewport.height if canvas else 0
        
        # arrange cells
        self.arrange(canvas, source, **overrides)
        
        # start drawing group
        canvas.group(tag, "layout")
        
        # set pen and brush
        canvas.line_width = 0
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw background
        canvas.draw_rect(x, y, width, height)
        
        # draw cells
        for cell in sorted(self._cells, key=lambda c: c.z_index):
            cell.draw(canvas)
        
        # end drawing group
        canvas.ungroup()
    
    
    def arrange(self, canvas=None, source=UNDEF, **overrides):
        """Calculates and sets cells frames."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        padding = self.get_property('padding', source, overrides)
        spacing = self.get_property('spacing', source, overrides)
        
        # get size from canvas
        if width is UNDEF:
            width = canvas.viewport.width if canvas else 0
        if height is UNDEF:
            height = canvas.viewport.height if canvas else 0
        
        # apply padding and spacing
        padding = padding or (0, 0, 0, 0)
        x += padding[3]
        y += padding[0]
        width -= spacing * (len(self._cols) - 1) + padding[1] + padding[3]
        height -= spacing * (len(self._rows) - 1) + padding[0] + padding[2]
        
        # arrange rows and cols
        heights = self._arrange_rows(height, spacing)
        widths = self._arrange_cols(width, spacing)
        
        # arrange cells
        for cell in self._cells:
            
            r, rs = cell.row, cell.row_span
            c, cs = cell.col, cell.col_span
            
            cell.frame = Frame(
                x = x + sum(widths[0:c]) + spacing * c,
                y = y + sum(heights[0:r]) + spacing * r,
                width = sum(widths[c:c+cs]) + spacing * (cs-1),
                height = sum(heights[r:r+rs]) + spacing * (rs-1))
            
            cell.arrange(canvas)
    
    
    def add(self, graphics, row, col, **overrides):
        """
        Adds graphics to specified layout cell. Additional rows and columns are
        added if necessary with relative size of 1.
        
        Args:
            graphics: pero.Graphics
                Graphics to be added.
            
            row: int
                Index of the row into which the graphics should be added.
            
            col: int
                Index of the column into which the graphics should be added.
            
            row_span: int
                Number of rows the graphics should span.
            
            col_span: int
                Number of columns the graphics should span.
            
            width: int, float or UNDEF
                Minimum width of the content area. If not specified, the content
                may use whole available width.
            
            height: int, float or UNDEF
                Minimum height of the content area. If not specified, the
                content may use whole available height.
            
            padding: int, float or tuple
                Inner empty space of the cell as a single value or values for
                individual sides starting from top.
            
            h_expand: bool
                If set to True the cell content can use full available width
                even if the 'width' property is set.
            
            v_expand: bool
                If set to True the cell content can use full available height
                even if the 'height' property is set.
            
            h_align: str
                Horizontal alignment of the cell content as any item from the
                pero.POSITION_LRC enum. Note that for this to have any effect
                the 'width' property must be specified.
            
            v_align: str
                Vertical alignment of the cell content as any item from the
                pero.POSITION_TBC enum. Note that for this to have any effect
                the 'height' property must be specified.
            
            line properties:
                All the pero.LineProperties to specify the cell background
                outline.
            
            fill properties:
                All the pero.FillProperties to specify the cell background
                fill.
        """
        
        # check type
        if not isinstance(graphics, Graphics):
            message = "Graphics must be of type pero.Graphics! -> %s" % type(graphics)
            raise TypeError(message)
        
        # init cell
        cell = Cell(
            graphics = graphics,
            row = row,
            col = col,
            **overrides)
        
        # get used rows and columns
        rows = cell.rows
        cols = cell.cols
        
        # add rows and columns if necessary
        while len(self._rows) <= max(rows):
            self.add_row(1, True)
        
        while len(self._cols) <= max(cols):
            self.add_col(1, True)
        
        # check if cells are empty
        for r in rows:
            for c in cols:
                if self._grid[r][c] is not None:
                    message = "Specified cell (%s,%s) is already used!" % (r, c)
                    raise ValueError(message)
        
        # register cell
        self._cells.append(cell)
        
        # add cell to grid
        for r in rows:
            for c in cols:
                self._grid[r][c] = cell
    
    
    def add_row(self, height=1, relative=True):
        """
        Adds additional row at the end of layout with specified absolute or
        relative height.
        
        Args:
            height: int or float
                Absolute or relative height of the row.
            
            relative:
                If set to True, specified height is considered as relative
                portion of total available space after filling all fixed rows.
        """
        
        # init row
        row = Row(
            height = height,
            relative = relative)
        
        # add row
        self._rows.append(row)
        
        # update grid
        self._grid.append([None for c in range(len(self._cols))])
    
    
    def add_col(self, width=1, relative=True):
        """
        Adds additional column at the end of layout with specified absolute or
        relative width.
        
        Args:
            width: int or float
                Absolute or relative width of the column.
            
            relative:
                If set to True, specified width is considered as relative
                portion of total available space after filling all fixed
                columns.
        """
        
        # init column
        col = Column(
            width = width,
            relative = relative)
        
        # add column
        self._cols.append(col)
        
        # update grid
        for row in self._grid:
            row.append(None)
    
    
    def _arrange_rows(self, available, spacing):
        """Calculates final size of each row."""
        
        # get tracks
        tracks = [(row.height, row.relative) for row in self._rows]
        
        # get cell constraints
        constraints = []
        for cell in self._cells:
            if cell.height is not UNDEF:
                padding = cell.padding or (0, 0, 0, 0)
                minimum = cell.height + padding[0] + padding[2] - spacing * (cell.row_span - 1)
                constraints.append((cell.row, cell.row_span, max(0, minimum)))
        
        # arrange rows
        return self._arrange_tracks(available, tracks, constraints)
    
    
    def _arrange_cols(self, available, spacing):
        """Calculates final size of each column."""
        
        # get tracks
        tracks = [(col.width, col.relative) for col in self._cols]
        
        # get cell constraints
        constraints = []
        for cell in self._cells:
            if cell.width is not UNDEF:
                padding = cell.padding or (0, 0, 0, 0)
                minimum = cell.width + padding[1] + padding[3] - spacing * (cell.col_span - 1)
                constraints.append((cell.col, cell.col_span, max(0, minimum)))
        
        # arrange cols
        return self._arrange_tracks(available, tracks, constraints)
    
    
    def _arrange_tracks(self, available, tracks, constraints):
        """Calculates final sizes of fixed and relative tracks."""
        
        # get minima
        minima = [t[0] if not t[1] else 0 for t in tracks]
        constraints = sorted(constraints, key=lambda item: item[1])
        
        # increase relative track minima until all cell constraints are met
        while True:
            sizes = self._allocate_tracks(available, tracks, minima)
            
            for start, span, minimum in constraints:
                current = sum(sizes[start:start+span])
                deficit = minimum - current
                
                if deficit <= 1e-9:
                    continue
                
                indices = [
                    i for i in range(start, start+span)
                    if tracks[i][1]]
                
                # fixed tracks take precedence over cell minima
                if not indices:
                    continue
                
                weights = [max(0, tracks[i][0]) for i in indices]
                weight_sum = sum(weights)
                
                if weight_sum:
                    shares = [weight / weight_sum for weight in weights]
                else:
                    shares = [1 / len(indices)] * len(indices)
                
                for i, share in zip(indices, shares):
                    minima[i] = max(minima[i], sizes[i] + deficit * share)
                
                break
            else:
                return sizes
    
    
    def _allocate_tracks(self, available, tracks, minima):
        """Allocates available space using weights and minimum sizes."""
        
        # init values
        remains = available
        sizes = [0] * len(tracks)
        active = []
        
        # set fixed tracks
        for i, (size, relative) in enumerate(tracks):
            if relative:
                active.append(i)
            else:
                sizes[i] = size
                remains -= size
        
        # distribute relative tracks
        while active:
            
            weight_sum = sum(max(0, tracks[i][0]) for i in active)
            if not weight_sum:
                for i in active:
                    sizes[i] = minima[i]
                break
            
            unit = remains / weight_sum
            forced = next((i for i in active if max(0, unit * max(0, tracks[i][0])) < minima[i]), None)
            if forced is None:
                for i in active:
                    sizes[i] = max(0, unit * max(0, tracks[i][0]))
                break
            
            sizes[forced] = minima[forced]
            remains -= minima[forced]
            active.remove(forced)
        
        return sizes


class Row(PropertySet):
    """
    Layout row definition. This is typically created automatically by layout
    manager but the properties can be later changed if needed.
    
    Properties:
        
        height: int or float
            Specifies absolute or relative height of the row.
        
        relative: bool
            Specifies whether the row height is considered as relative portion
            of total available space after filling all fixed rows.
    """
    
    height = NumProperty(UNDEF, dynamic=False)
    relative = BoolProperty(False, dynamic=False)


class Column(PropertySet):
    """
    Layout column definition. This is typically created automatically by layout
    manager but the properties can be later changed if needed.
    
    Properties:
        
        width: int or float
            Specifies absolute or relative width of the column.
        
        relative: bool
            Specifies whether the column width is considered as relative portion
            of total available space after filling all fixed columns.
    """
    
    width = NumProperty(UNDEF, dynamic=False)
    relative = BoolProperty(False, dynamic=False)


class Cell(Graphics):
    """
    Layout cell definition. This is typically created automatically by layout
    manager but some of the properties can be later changed if needed.
    
    Properties:
        
        graphics: pero.Graphics
            Specifies the graphics to draw.
        
        row: int
            Specifies the index of the row in which the cell sits. This value
            cannot be changed once set.
        
        col: int
            Specifies the index of the column in which the cell sits. This value
            cannot be changed once set.
        
        row_span: int
            Specifies the number of rows the cell spans. This value cannot be
            changed once set.
        
        col_span: int
            Specifies the number of columns the cell spans. This value cannot be
            changed once set.
        
        clip: bool
            Specifies whether the content overflow should be clipped.
        
        width: int, float or UNDEF
            Specifies the minimum width of the content area. If not specified,
            the content may use whole available width.
        
        height: int, float or UNDEF
            Specifies the minimum height of the content area. If not specified,
            the content may use whole available height.
        
        padding: int, float or tuple
            Specifies the inner empty space of the cell as a single value or
            values for individual sides starting from top.
        
        h_expand: bool
            Specifies whether the cell content can use full available width even
            if the 'width' property is set.
        
        v_expand: bool
            Specifies whether the cell content can use full available height
            even if the 'height' property is set.
        
        h_align: str
            Specifies the horizontal alignment of the cell content as any item
            from the pero.POSITION_LRC enum. Note the for this to have any
            effect the 'width' property must be specified and 'h_expand' must be
            disabled.
        
        v_align: str
            Specifies vertical alignment of the cell content as any item from
            the pero.POSITION_TBC enum. Note the for this to have any effect
            the 'height' property must be specified and 'v_expand' must be
            disabled.
        
        line properties:
            Includes pero.LineProperties to specify the cell background
            outline.
        
        fill properties:
            Includes pero.FillProperties to specify the cell background fill.
        
        frame: pero.Frame
            Specifies the cell frame. This value is typically calculated and set
            automatically by the layout manager.
        
        content: pero.Frame
            Specifies the cell content frame. This value is typically calculated
            and set automatically by the layout manager.
    """
    
    graphics = Property(UNDEF, types=(Graphics,), dynamic=False)
    
    row = IntProperty(UNDEF, dynamic=False)
    col = IntProperty(UNDEF, dynamic=False)
    row_span = IntProperty(1, dynamic=False)
    col_span = IntProperty(1, dynamic=False)
    
    width = NumProperty(UNDEF, dynamic=False)
    height = NumProperty(UNDEF, dynamic=False)
    padding = QuadProperty(0, dynamic=False)
    clip = BoolProperty(True)
    
    h_expand = BoolProperty(True)
    v_expand = BoolProperty(True)
    
    h_align = EnumProperty(POS_CENTER, enum=POSITION_LRC, dynamic=False)
    v_align = EnumProperty(POS_CENTER, enum=POSITION_TBC, dynamic=False)
    
    outline = Include(LineProperties, line_color=None)
    fill = Include(FillProperties, fill_color=None)
    
    frame = FrameProperty(UNDEF, dynamic=False)
    content = FrameProperty(UNDEF, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of layout Cell."""
        
        super().__init__(**overrides)
        
        self._content_origin = (0, 0)
        
        # lock properties
        self.lock_property('row')
        self.lock_property('col')
        self.lock_property('row_span')
        self.lock_property('col_span')
    
    
    @property
    def rows(self):
        """
        Gets indices of all the rows this cell spans.
        
        Returns:
            (int,)
                Tuple of rows indices.
        """
        
        return tuple(self.row+s for s in range(self.row_span))
    
    
    @property
    def cols(self):
        """
        Gets indices of all the columns this cell spans.
        
        Returns:
            (int,)
                Tuple of columns indices.
        """
        
        return tuple(self.col+s for s in range(self.col_span))
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw cell graphics."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        graphics = self.get_property('graphics', source, overrides)
        frame = self.get_property('frame', source, overrides)
        content = self.get_property('content', source, overrides)
        clip = self.get_property('clip', source, overrides)
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # start drawing group
        canvas.group(tag, "layout_cell")
        
        # draw background
        canvas.draw_rect(*frame.rect)
        
        # set clipping
        if clip:
            canvas.clip(Path().rect(*content.rect))
        
        # draw graphics
        if graphics:
            with canvas.view(*content.rect, relative=True):
                graphics.draw(canvas)
        
        # revert clipping
        if clip:
            canvas.unclip()
        
        # end drawing group
        canvas.ungroup()
    
    
    def arrange(self, canvas=None, source=UNDEF, **overrides):
        """Calculates and sets content frame."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        padding = self.get_property('padding', source, overrides)
        h_expand = self.get_property('h_expand', source, overrides)
        v_expand = self.get_property('v_expand', source, overrides)
        h_align = self.get_property('h_align', source, overrides)
        v_align = self.get_property('v_align', source, overrides)
        clip = self.get_property('clip', source, overrides)
        
        # calculate available area inside padding
        inner_x = frame.x + padding[3]
        inner_y = frame.y + padding[0]
        inner_width = max(0, frame.width - padding[1] - padding[3])
        inner_height = max(0, frame.height - padding[0] - padding[2])
        
        # calculate content size
        width = width or 0
        height = height or 0
        
        if not width or h_expand:
            width = max(width, inner_width)
        if not height or v_expand:
            height = max(height, inner_height)
        
        # constrain content before alignment
        if clip:
            width = min(width, inner_width)
            height = min(height, inner_height)
        
        # align horizontally
        if h_align == POS_CENTER:
            x = inner_x + .5 * (inner_width - width)
        elif h_align == POS_RIGHT:
            x = inner_x + inner_width - width
        else:
            x = inner_x
        
        # align vertically
        if v_align == POS_CENTER:
            y = inner_y + .5 * (inner_height - height)
        elif v_align == POS_BOTTOM:
            y = inner_y + inner_height - height
        else:
            y = inner_y
        
        self.content = Frame(x, y, max(0, width), max(0, height))
    
    
    def to_content(self, x, y):
        """
        Recalculates given position from the layout coordinate system into the
        cell content system.
        
        Args:
            x: float
                X-coordinate to convert.
            
            y: float
                Y-coordinate to convert.
        
        Returns:
            (float, float)
                X and y coordinates within cell content coordinate system.
        """
        
        return x - self.content.x, y - self.content.y
    
    
    def to_layout(self, x, y):
        """
        Recalculates given position from the cell content coordinate system into
        the layout system.
        
        Args:
            x: float
                X-coordinate to convert.
            
            y: float
                Y-coordinate to convert.
        
        Returns:
            (float, float)
                X and y coordinates within layout coordinate system.
        """
        
        return x + self.content.x, y + self.content.y
