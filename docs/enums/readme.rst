pero.enums
==========

Drawing Enums
-------------

pero.ANGLE
~~~~~~~~~~
Used to specify angle units.

- **pero.DEG**: Angle defined in degrees.
- **pero.RAD**: Angle defined in radians.


pero.LINE_CAP
~~~~~~~~~~~~~
Used to specify a shape to be used at line ends.

.. image:: images/line_cap.svg

- **pero.BUTT**: A line cuts directly after endpoint.
- **pero.SQUARE**: A line continues beyond endpoint for half its width.
- **pero.ROUND**: A line continues beyond endpoint by half circle to form round endpoints.


pero.LINE_JOIN
~~~~~~~~~~~~~~
Used to specify a line join style.

.. image:: images/line_join.svg

- **pero.BEVEL**: A line join is cutout at the distance of half line width.
- **pero.MITER**: Extends a line join to follow the angle of segments.
- **pero.ROUND**: A line join is filled by circle to form round join.


pero.LINE_STYLE
~~~~~~~~~~~~~~~
Used to specify a line style.

.. image:: images/line_style.svg

- **pero.SOLID**: A line is drawn as a solid line.
- **pero.DOTTED**: A line is drawn as a series of dots and spaces.
- **pero.DASHED**: A line is drawn as a series of dashes and spaces.
- **pero.DASHDOTTED**: A line is drawn as a series of dashes, dots and spaces.
- **pero.CUSTOM**: A line is drawn according to definition given by 'line_dash'.


pero.FILL_STYLE
~~~~~~~~~~~~~~~
Used to specify a filling style.

- **pero.SOLID**: Uses current fill color to draw fills.
- **pero.TRANS**: Uses transparent color to draw fills.


pero.FILL_RULE
~~~~~~~~~~~~~~
Used to specify a path filling rule.

.. image:: images/fill_rule.svg

- **pero.EVENODD**: Fills an area according to inside/outside state.
- **pero.WINDING**: Fills a whole enclosed area.


pero.LINE_STEP
~~~~~~~~~~~~~~
Used to specify a profile line steps style.

.. image:: images/line_step.svg

- **pero.NONE**: Data points are connected directly by strait line.
- **pero.BEFORE**: A horizontal line starts before data points.
- **pero.AFTER**: A horizontal line starts after data points.
- **pero.MIDDLE**: A horizontal line crosses data points.


Text Enums
----------

pero.FONT_FAMILY
~~~~~~~~~~~~~~~~
Used to specify a font family, rather then exact font to use.

.. image:: images/font_family.svg

- **pero.SERIF**: Default serif font will be used (e.g. Times).
- **pero.SANS**: Default sans-serif font will be used (e.g. Arial or Helvetica).
- **pero.MONO**: Default monospaced font will be used (e.g. Courier).


pero.FONT_STYLE
~~~~~~~~~~~~~~~
Used to specify a font style to use.

.. image:: images/font_style.svg

- **pero.NORMAL**: Normal font style variant will be used.
- **pero.ITALIC**: Italic font style variant will be used.


pero.FONT_WEIGHT
~~~~~~~~~~~~~~~~
Used to specify a font weight to use. Note that not all values are supported by all backends and the closest value might
be used instead (e.g. pero.HEAVY falls to pero.BOLD).

.. image:: images/font_weight.svg

- **pero.NORMAL**: Normal font weight variant will be used.
- **pero.LIGHT**: Light font weight variant will be used.
- **pero.BOLD**: Bold font weight variant will be used.
- **pero.BLACK**: Black font weight variant will be used.
- **pero.HEAVY**: Heavy font weight variant will be used.
- **pero.SEMIBOLD**: Semi-bold font weight variant will be used.
- **pero.MEDIUM**: Medium font weight variant will be used.
- **pero.ULTRALIGHT**: Ultra-light font weight variant will be used.
- **pero.THIN**: Thin font weight variant will be used.


pero.TEXT_ALIGN
~~~~~~~~~~~~~~~
Used to specify a text horizontal alignment.

.. image:: images/text_align.svg

- **pero.LEFT**: Uses the text left side as anchor.
- **pero.CENTER**: Uses the text center as anchor.
- **pero.RIGHT**: Uses the text right side as anchor.


pero.TEXT_BASELINE
~~~~~~~~~~~~~~~~~~
Used to specify a text vertical alignment.

.. image:: images/text_base.svg

- **pero.TOP**: Uses the text top side as anchor.
- **pero.MIDDLE**: Uses the text center as anchor.
- **pero.BOTTOM**: Uses the text bottom side as anchor.


pero.TEXT_ROTATION
~~~~~~~~~~~~~~~~~~
Used to define a way to align text labels around a circle according to their angle.

.. image:: images/text_rotation.svg

- **pero.NONE**: Labels are drawn horizontally, aligned to the circle.
- **pero.FOLLOW**: Labels are drawn the way their left or right side follows the circle.
- **pero.NATURAL**: Labels are drawn the way their top or bottom side follows the circle.
- **pero.FACEOUT**: Labels are drawn the way their bottom side follows the circle.
- **pero.FACEIN**: Labels are drawn the way their top side follows the circle.


Glyphs Enums
------------

pero.MARKER
~~~~~~~~~~~
Used to specify a marker glyph type shortcut for pero.MarkerProperty.

.. image:: images/markers.svg

- Use the "*" character for pero.Asterisk marker.
- Use the "o" character for pero.Circle marker.
- Use the "x" character for pero.Cross marker.
- Use the "+" character for pero.Plus marker.
- Use the "t" character for pero.Triangle marker.
- Use the "s" character for pero.Square marker.
- Use the "d" character for pero.Diamond marker.
- Use the "p" character for pero.Pentagon marker.
- Use the "h" character for pero.Hexagon marker.


pero.ARROWS
~~~~~~~~~~~
Used to specify an arrow type shortcut to create pero.Arrow.

.. image:: images/arrows.svg

- Use the "c" character for pero.ArcArrow arrow.
- Use the ")" character for pero.BowArrow arrow.
- Use the "~" character for pero.CurveArrow arrow.
- Use the "-" character for pero.LineArrow arrow.
- Use the "/" character for pero.RayArrow arrow.
- Use the "z" character for line pero.ConnectorArrow arrow.
- Use the "s" character for curve pero.ConnectorArrow arrow.


pero.HEADS
~~~~~~~~~~
Used to specify an arrow head type shortcut for pero.HeadProperty.

.. image:: images/heads.svg

- Use the "o" character for pero.CircleHead arrow head.
- Use the "\|" character for pero.LineHead arrow head.
- Use the "\|>" characters for pero.NormalHead arrow head.
- Use the "<\|" characters for pero.NormalHead arrow head.
- Use the ">" characters for pero.OpenHead arrow head.
- Use the "<" characters for pero.OpenHead arrow head.
- Use the ">>" characters for pero.VeeHead arrow head.
- Use the "<<" characters for pero.VeeHead arrow head.


Position Enums
--------------

pero.ORIENTATION
~~~~~~~~~~~~~~~~
Used to specify an object orientation.

- **pero.HORIZONTAL**
- **pero.VERTICAL**


pero.POSITION_LR
~~~~~~~~~~~~~~~~
Used to specify an object horizontal position.

- **pero.LEFT**
- **pero.RIGHT**


pero.POSITION_LRC
~~~~~~~~~~~~~~~~~
Used to specify an object horizontal position.

- **pero.LEFT**
- **pero.RIGHT**
- **pero.CENTER**


pero.POSITION_TB
~~~~~~~~~~~~~~~~
Used to specify an object vertical position.

- **pero.TOP**
- **pero.BOTTOM**


pero.POSITION_TBC
~~~~~~~~~~~~~~~~~
Used to specify an object vertical position.

- **pero.TOP**
- **pero.BOTTOM**
- **pero.CENTER**


pero.POSITION_LRTB
~~~~~~~~~~~~~~~~~~
Used to specify an object cross position.

- **pero.LEFT**
- **pero.RIGHT**
- **pero.TOP**
- **pero.BOTTOM**


pero.POSITION_LRTBC
~~~~~~~~~~~~~~~~~~~
Used to specify an object cross position.

- **pero.LEFT**
- **pero.RIGHT**
- **pero.TOP**
- **pero.BOTTOM**
- **pero.CENTER**


pero.POSITION_IOC
~~~~~~~~~~~~~~~~~
Used to specify an object relative position.

- **pero.INSIDE**
- **pero.OUTSIDE**
- **pero.CENTER**


pero.POSITION_SEM
~~~~~~~~~~~~~~~~~
Used to specify an object relative position.

- **pero.START**
- **pero.END**
- **pero.MIDDLE**


pero.POSITION_TL
~~~~~~~~~~~~~~~~
Used to specify an object corner position.

- **pero.TOP**
- **pero.LEFT**


pero.POSITION_TR
~~~~~~~~~~~~~~~~
Used to specify an object corner position.

- **pero.TOP**
- **pero.RIGHT**


pero.POSITION_BL
~~~~~~~~~~~~~~~~
Used to specify an object corner position.

- **pero.BOTTOM**
- **pero.LEFT**


pero.POSITION_BR
~~~~~~~~~~~~~~~~
Used to specify an object corner position.

- **pero.BOTTOM**
- **pero.RIGHT**


pero.POSITION_COMPASS
~~~~~~~~~~~~~~~~~~~~~
Used to specify an object compass-like position.

- **pero.N**
- **pero.NW**
- **pero.NE**
- **pero.S**
- **pero.SW**
- **pero.SE**
- **pero.W**
- **pero.E**
