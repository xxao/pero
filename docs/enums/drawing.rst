Drawing Enums
=============

pero.ANGLE
----------
Used to specify angle units.

- **pero.DEG**: Angle defined in degrees.
- **pero.RAD**: Angle defined in radians.


pero.LINE_CAP
-------------
Used to specify a shape to be used at line ends.

.. image:: images/line_cap.svg

- **pero.BUTT**: A line cuts directly after endpoint.
- **pero.SQUARE**: A line continues beyond endpoint for half its width.
- **pero.ROUND**: A line continues beyond endpoint by half circle to form round endpoints.


pero.LINE_JOIN
--------------
Used to specify a line join style.

.. image:: images/line_join.svg

- **pero.BEVEL**: A line join is cutout at the distance of half line width.
- **pero.MITER**: Extends a line join to follow the angle of segments.
- **pero.ROUND**: A line join is filled by circle to form round join.


pero.LINE_STYLE
---------------
Used to specify a line style.

.. image:: images/line_style.svg

- **pero.SOLID**: A line is drawn as a solid line.
- **pero.DOTTED**: A line is drawn as a series of dots and spaces.
- **pero.DASHED**: A line is drawn as a series of dashes and spaces.
- **pero.DASHDOTTED**: A line is drawn as a series of dashes, dots and spaces.
- **pero.CUSTOM**: A line is drawn according to definition given by 'line_dash'.


pero.FILL_STYLE
---------------
Used to specify a filling style.

- **pero.SOLID**: Uses current fill color to draw fills.
- **pero.TRANS**: Uses transparent color to draw fills.


pero.FILL_RULE
--------------
Used to specify a path filling rule.

.. image:: images/fill_rule.svg

- **pero.EVENODD**: Fills an area according to inside/outside state.
- **pero.WINDING**: Fills a whole enclosed area.


pero.LINE_STEP
--------------
Used to specify a profile line steps style.

.. image:: images/line_step.svg

- **pero.NONE**: Data points are connected directly by strait line.
- **pero.BEFORE**: A horizontal line starts before data points.
- **pero.AFTER**: A horizontal line starts after data points.
- **pero.MIDDLE**: A horizontal line crosses data points.
