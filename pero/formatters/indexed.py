#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from .. properties import *
from . formatter import Formatter


class IndexFormatter(Formatter):
    """
    This formatter tool returns appropriate label by its index within the
    predefined set of 'labels'. A number is expected as an input of the 'format'
    method and it is automatically rounded to the nearest integer to look-up
    predefined label. If labels are not defined or the index is outside current
    range the 'default' property value is returned.
    
    Properties:
        
        labels: (str,), None or UNDEF
            Specifies the sequence of predefined labels.
        
        default: str
            Specifies the default value to be used if no appropriate label can
            be found.
    """
    
    labels = TupleProperty(UNDEF, intypes=(str,), dynamic=False, nullable=True)
    default = StringProperty("", dynamic=False, nullable=True)
    
    
    def format(self, value, *args, **kwargs):
        """
        Returns a predefined label for given index.
        
        Args:
            value: int or float
                Index value for which to look up a label.
        
        Returns:
            str
                Corresponding label.
        """
        
        # get index
        i = int(round(value))
        
        # check labels
        if not self.labels or i < 0 or i >= len(self.labels):
            return self.default
        
        # return label
        return self.labels[i]
