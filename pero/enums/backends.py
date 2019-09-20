#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# load modules
from .enum import Enum

# define backends
BACKEND = Enum(
    JSON = 'json',
    SVG = 'svg',
    QT = 'qt',
    WX = 'wx',
    CAIRO = 'cairo',
    MUPDF = 'mupdf',
    PYTHONISTA = 'pythonista')

# define image formats supported by JSON backend
EXPORT_JSON = {
    '.json'}

# define image formats supported by SVG backend
EXPORT_SVG = {
    '.svg'}

# define image formats supported by QT backend
EXPORT_QT = {
    '.bmp',
    '.gif',
    '.jpg',
    '.jpeg',
    '.pdf',
    '.png'}

# define image formats supported by WX backend
EXPORT_WX = {
    '.bmp',
    '.cur',
    '.ico',
    '.jpg',
    '.jpeg',
    '.pcx',
    '.png',
    '.pnm',
    '.tif',
    '.tiff',
    '.xpm'}

# define formats supported by Cairo backend
EXPORT_CAIRO = {
    '.bmp',
    '.eps',
    '.gif',
    '.jpg',
    '.jpeg',
    '.pdf',
    '.png',
    '.svg',
    '.tif',
    '.tiff'}

# define image formats supported by MuPDF backend
EXPORT_MUPDF = {
    '.pdf'}

# define image formats supported by Pythonista backend
EXPORT_PYTHONISTA = {
    '.png'}

# define available formats
EXPORT_FORMATS = {
    BACKEND.JSON: EXPORT_JSON,
    BACKEND.SVG: EXPORT_SVG,
    BACKEND.QT: EXPORT_QT,
    BACKEND.WX: EXPORT_WX,
    BACKEND.CAIRO: EXPORT_CAIRO,
    BACKEND.MUPDF: EXPORT_MUPDF,
    BACKEND.PYTHONISTA: EXPORT_PYTHONISTA}

# define export backend priorities
EXPORT_PRIORITY = [
    BACKEND.JSON,
    BACKEND.SVG,
    BACKEND.QT,
    BACKEND.WX,
    BACKEND.CAIRO,
    BACKEND.MUPDF,
    BACKEND.PYTHONISTA]

# define viewer backend priorities
VIEWER_PRIORITY = [
    BACKEND.QT,
    BACKEND.WX,
    BACKEND.PYTHONISTA]

# define default export size
EXPORT_WIDTH = 750
EXPORT_HEIGHT = 500

VIEWER_WIDTH = 750
VIEWER_HEIGHT = 500
