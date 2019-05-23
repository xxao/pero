pero.backends
=============

The actual drawing is done by various backends, for which the *pero* library provides consistent API. This is achieved
by specific implementations of the *pero.Canvas* base class, which translates the API into methods and logic of
particular backend. As of now, the *pero* library supports `wxPython <https://pypi.org/project/wxPython/>`_,
`PyCairo <https://pypi.org/project/pycairo/>`_, `PyMuPDF <https://pypi.org/project/PyMuPDF/>`_,
`Pythonista <http://omz-software.com/pythonista/>`_ app and its own implementation of SVG canvas.

Under construction...