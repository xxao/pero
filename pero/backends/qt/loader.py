#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import PyQt5
try:
    from PyQt5.QtCore import Qt, QPoint, QLineF, QSizeF, QEvent
    from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPainterPath
    from PyQt5.QtGui import QPainter, QImage, QPicture, QPixmap, QFontMetrics
    from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout
    from PyQt5.QtPrintSupport import QPrinter

# import PySlide2
except ImportError:
    
    from PySide2.QtCore import Qt, QPoint, QLineF, QSizeF, QEvent
    from PySide2.QtGui import QFont, QColor, QPen, QBrush, QPainterPath
    from PySide2.QtGui import QPainter, QImage, QPicture, QPixmap, QFontMetrics
    from PySide2.QtWidgets import QApplication, QWidget, QDesktopWidget, QHBoxLayout
    from PySide2.QtPrintSupport import QPrinter
