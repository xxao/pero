#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
from ...properties import UNDEF


def crop_indices(data, crop, extend):
    """
    Calculates crop indices for given data and range. Optionally the range can
    be extended by adding additional adjacent points to each side. Such
    extension might be useful to display zoomed lines etc. Note that this method
    assumes that given values are sorted ascendantly.
    
    Args:
        data: 1D numpy.ndarray
            Data for which to calculated indices.
        
        crop: (float, float)
            Crop range as (min, max).
        
        extend: bool
            If set to True additional adjacent point is added to each side.
    
    Returns:
        (int, int)
            Left and right cropping index.
    """
    
    # check crop
    if crop is None:
        return 0, len(data)
    
    # ensure numpy array
    if not isinstance(data, numpy.ndarray):
        data = numpy.array(data)
    
    # get indices
    left_idx = numpy.searchsorted(data, crop[0], side='left')
    right_idx = numpy.searchsorted(data, crop[1], side='right')
    
    # extend range by adjacent values
    if extend and left_idx > 0:
        left_idx = numpy.searchsorted(data[:left_idx], data[left_idx-1], side='left')
    
    if extend and right_idx < len(data):
        right_idx += numpy.searchsorted(data[right_idx:], data[right_idx], side='right')
    
    return left_idx, right_idx


def crop_points(data, crops, extend=False):
    """
    Crops given data by applying specified ranges and optionally extends
    data by adding adjacent points. To skip any data item from being used for
    cropping, just provide None for corresponding crop. Note that this method
    changes the order of items but given data arrays are still synchronized.
    
    Args:
        data: (1D numpy.ndarray,)
            Data to crop.
        
        crops: ((float, float),)
            Crop ranges.
        
        extend: bool
            If set to True additional adjacent point is added to each side.
    
    Returns:
        (1D numpy.ndarray,)
            Cropped data.
    """
    
    # break links
    data = list(data[:])
    crops = list(crops[:])
    
    # ensure numpy arrays
    for i, d in enumerate(data):
        if d is not None and not isinstance(d, numpy.ndarray):
            data[i] = numpy.array(d)
    
    # crop data
    for i, crop in enumerate(crops):
        
        # check crop
        if crop is None or data[i] is None:
            continue
        
        # apply sorting
        sorting = data[i].argsort()
        for j, d in enumerate(data):
            if d is not None:
                data[j] = d[sorting]
        
        # apply crop
        i1, i2 = crop_indices(data[i], crop, extend)
        for j, d in enumerate(data):
            if d is not None:
                data[j] = d[i1:i2]
    
    return data


def crop_profile(data, crop, extend=False, master=0):
    """
    Crops data by applying given range to the master data item and cropping
    others accordingly. Optionally the crop can be extended by adding adjacent
    edge points. Note that this method assumes the master data item to be sorted
    ascendantly.
    
    Args:
        data: (1D numpy.ndarray,)
            Data to crop.
        
        crop: (float, float)
            Crop range.
        
        extend: bool
            If set to True additional adjacent point is added to each side.
        
        master: int
            Index of the data array to be used for indices determination.
    
    Returns:
        (1D numpy.ndarray,)
            Cropped data.
    """
    
    # break links
    data = list(data[:])
    
    # check crop
    if crop is None:
        return data
    
    # ensure numpy arrays
    for i, d in enumerate(data):
        if d is not None and not isinstance(d, numpy.ndarray):
            data[i] = numpy.array(d)
    
    # get crop indices from first item
    i1, i2 = crop_indices(data[master], crop, extend)
    
    # apply crop
    for i, d in enumerate(data):
        if d is not None:
            data[i] = d[i1:i2]
    
    return data


def calc_limits(*data):
    """
    Calculates limits for each data set in collection.
    
    Args:
        data: (1D numpy.ndarray,)
            Data to use.
    
    Returns:
        [[float, float],]
            Limits for each data set as series of [min, max].
    """
    
    limits = []
    
    for d in data:
        if d is None or len(d) == 0:
            limits.append(None)
        elif isinstance(d, numpy.ndarray):
            limits.append([d.min(), d.max()])
        else:
            limits.append([min(d), max(d)])
    
    return limits


def combine_limits(*limits):
    """
    Combines given data sets limits to single limits.
    
    Args:
        limits: ([[float,float],],)
            Data sets limits.
    
    Returns:
        [[float,float],] or None
            Combined limits or None if no limits.
    """
    
    limits = [l for l in limits if l is not None]
    if len(limits) == 0:
        return None
    
    size = len(limits[0])
    final = []
    
    for i in range(size):
        values = [v for l in limits if l[i] is not None for v in l[i]]
        final += [[min(values), max(values)]] if values else [None]
    
    if all(l is None for l in final):
        final = None
    
    return final


def calc_points_limits(data, crops, extend=False):
    """
    Crops given data by applying specified ranges and optionally extends
    data by adding adjacent points and finally calculates minimum and
    maximum for each data.
    
    Args:
        data: (1D numpy.ndarray,)
            Data to use.
        
        crops: ((float, float),)
            Crop ranges.
        
        extend: bool
            If set to True additional adjacent point is added to each side.
    
    Returns:
        [[float, float],]
            Data limits as series of [min, max] or None for each dimension.
    """
    
    data = crop_points(data, crops, extend=extend)
    return calc_limits(*data)


def calc_profile_limits(data, crop, extend=False, interpolate=False):
    """
    Crops given data by applying specified range to first data and
    optionally extends data by adding adjacent points and finally calculates
    minimum and maximum for each data. Note that this method assumes the first
    data item to be sorted ascendantly.
    
    Args:
        data: (1D numpy.ndarray,)
            Data to use.
        
        crop: (float, float)
            Crop range.
        
        extend: bool
            If set to True additional adjacent point is added to each side.
        
        interpolate: bool
            If set to True range extension is done by edge points
            interpolation to provide exact crop.
    
    Returns:
        [[float, float],]
            Data limits as series of [min, max] or None.
    """
    
    # check crop
    if crop is None:
        return calc_limits(*data)
    
    # no interpolation necessary
    if extend or not interpolate:
        data = crop_profile(data, crop, extend=extend)
        return calc_limits(*data)
    
    # get interpolation data
    x_data = data[0]
    y_data = data[1] if len(data) > 1 else None
    
    # get cropped limits
    data = crop_profile(data, crop, extend=False)
    limits = calc_limits(*data)
    
    # get indices
    i1, i2 = crop_indices(x_data, crop, extend=False)
    ei1, ei2 = crop_indices(x_data, crop, extend=True)
    
    # no interpolation necessary
    if (i1 == ei1 and i2 == ei2) or (i1 == i2 and (i1 == ei1 or i2 == ei2)):
        return limits
    
    # init limit
    if limits[0] is None:
        limits[0] = [crop[0], crop[1]]
    
    # interpolate left
    if i1 != ei1:
        
        limits[0][0] = crop[0]
        if y_data is not None:
            
            x1 = x_data[ei1]
            x2 = x_data[i1]
            y1 = y_data[ei1]
            y2 = y_data[i1]
            
            a = (y2 - y1) / (x2 - x1)
            b = y1 - a * x1
            y = a*crop[0] + b
            
            if limits[1] is None:
                limits[1] = [y, y]
            elif limits[1][0] > y:
                limits[1][0] = y
            elif limits[1][1] < y:
                limits[1][1] = y
    
    # interpolate right
    if i2 != ei2:
        
        limits[0][1] = crop[1]
        if y_data is not None:
            
            x1 = x_data[i2-1]
            x2 = x_data[ei2-1]
            y1 = y_data[i2-1]
            y2 = y_data[ei2-1]
            
            a = (y2 - y1) / (x2 - x1)
            b = y1 - a * x1
            y = a*crop[1] + b
            
            if limits[1] is None:
                limits[1] = [y, y]
            elif limits[1][0] > y:
                limits[1][0] = y
            elif limits[1][1] < y:
                limits[1][1] = y
    
    return limits


def is_sorted(data):
    """
    Checks if given data are sorted ascendantly.
    
    Args:
        data: (float,)
            Data to check.
    
    Returns:
        bool
            True if sorted, False otherwise.
    """
    
    for i in range(data.size-1):
        if data[i+1] < data[i]:
            return False
    
    return True


def extract_data_size(series, *names):
    """
    Determines series data size from the first available property, which
    provides direct values as list, tuple or NumPy array.
    
    Args:
        series: pero.plot.Series
            Series from which to extract data size.
        
        names: (str,)
            Sequence of property names to check.
    
    Returns:
        int or None
            Determined data size.
    """
    
    # get size
    for name in names:
        
        # check property
        if not series.has_property(name):
            continue
        
        # get property
        prop = series.get_property(name, native=True)
        
        # get size
        if isinstance(prop, (list, tuple, numpy.ndarray)):
            return len(prop)
    
    # no data
    return None


def extract_data(series, name, source=UNDEF, size=None, mapper=None, dtype=numpy.float64):
    """
    Extracts specified data coordinates into NumPy array of floats. If data are
    provided as a single value, an array of specified 'size' filled by the value
    is created. If data are provided as a list, tuple or array, new array is
    created. If data are provided as a selector, values are extracted from the
    'source'. Finally, raw data are recalculated by given 'mapper' and cast
    to specified type.
    
    Args:
        series: pero.plot.Series
            Series from which to extract data.
        
        name: str
            Data property name.
        
        source: (any,) or UNDEF
            Collection of data used by data selector.
        
        size: int or None
            Specific size to create data array from a single value.
        
        mapper: pero.Scale or None
            Scale to map raw values into final coordinates.
        
        dtype: numpy type
            Final data type for values.
    
    Returns:
        (numpy.ndarray, numpy.ndarray)
            Two 1D arrays of final values and raw data.
    """
    
    # init buffers
    raw = numpy.array([], dtype=numpy.float64)
    data = numpy.array([], dtype=numpy.float64)
    
    # check property
    if not series.has_property(name):
        return data, raw
    
    # get property
    prop = series.get_property(name, native=True)
    
    # extract raw data
    if isinstance(prop, (int, float)) and size:
        raw = numpy.full(size, prop)
    
    elif isinstance(prop, (list, tuple, numpy.ndarray)):
        raw = numpy.array(prop)
    
    elif prop != UNDEF and source is not UNDEF:
        raw = numpy.array([prop(p) for p in source])
    
    # apply mapper
    data = numpy.array(mapper.scale(raw)) if mapper else raw
    
    # ensure floats
    if data.dtype != dtype:
        data = data.astype(dtype, copy=False)
    
    # check data
    if size and len(data) != size:
        message = "Inconsistent data length for '%s' property!" % name
        raise ValueError(message)
    
    return data, raw
