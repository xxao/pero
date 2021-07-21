#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import decimal
from .. enums import *
from .. properties import *
from . utils import *
from . formatter import Formatter


class TimeFormatter(Formatter):
    """
    This formatter tool formats given time in seconds into reasonable time
    representation. The formatting can be fully automatic based on current
    'domain' and 'precision' or it can be controlled by defining the 'template'
    property.
    
    The 'template' should be specified by the parts or granularity to use,
    optionally with additional formatting (e.g. '{h}:{m:.02.0f}:{s:.02.0f}').
    The available parts, which can be used are defined by the pero.TIME
    enum. If there is no specific formatting of a part defined directly by the
    template, a default formatting or a custom sub-template is used. The parts
    sub-templates are definable by corresponding properties (e.g. 'h_template'
    for hours or 's_template' for seconds, s_template='{:.0f}s').
    
    For different purposes, different style of rounding might be necessary. For
    example the normal half-rounding should be used for axis labels, however, in
    case of time counters the value should always be rounded down. This behavior
    can be specified by the 'rounding' property as any item from the
    pero.ROUNDING enum.
    
    Properties:
        
        template: str, None or UNDEF
            Specifies the main template to be used instead of automatic
            formatting.
        
        d_template: str, None or UNDEF
            Specifies the template to be used for days formatting.
        
        h_template: str, None or UNDEF
            Specifies the template to be used for hours formatting.
        
        m_template: str, None or UNDEF
            Specifies the template to be used for minutes formatting.
        
        s_template: str, None or UNDEF
            Specifies the template to be used for seconds formatting.
        
        ms_template: str, None or UNDEF
            Specifies the template to be used for milliseconds formatting.
        
        us_template: str, None or UNDEF
            Specifies the template to be used for microseconds formatting.
        
        ns_template: str, None or UNDEF
            Specifies the template to be used for nanoseconds formatting.
        
        rounding: str
            Specifies the rounding style as any item from the pero.ROUNDING
            enum.
        
        separator: str or UNDEF
            Specifies the separator to be used between individual parts.
        
        add_units: bool
            Specifies whether the units should be added to individual parts.
    """
    
    template = StringProperty(UNDEF, dynamic=False, nullable=True)
    d_template = StringProperty(UNDEF, dynamic=False, nullable=True)
    h_template = StringProperty(UNDEF, dynamic=False, nullable=True)
    m_template = StringProperty(UNDEF, dynamic=False, nullable=True)
    s_template = StringProperty(UNDEF, dynamic=False, nullable=True)
    ms_template = StringProperty(UNDEF, dynamic=False, nullable=True)
    us_template = StringProperty(UNDEF, dynamic=False, nullable=True)
    ns_template = StringProperty(UNDEF, dynamic=False, nullable=True)
    
    rounding = EnumProperty(ROUNDING.HALFUP, enum=ROUNDING, dynamic=False)
    separator = StringProperty(UNDEF, dynamic=False)
    add_units = BoolProperty(False, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of TimeFormatter."""
        
        super().__init__(**overrides)
        
        # init buffers
        self._template = None
        self._templates_multi = None
        self._templates_single = None
        
        self._is_dirty = True
        
        # get available parts (units, factor)
        self._parts = sorted(TIME_FACTORS.items(), key=lambda d: d[1], reverse=True)
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_time_formatter_property_changed)
    
    
    def format(self, value, *args, **kwargs):
        """
        Formats a given value using time formatting.
        
        Args:
            value: float
                Time in seconds.
        
        Returns:
            str
                Formatted label.
        """
        
        # init formatting
        if self._is_dirty:
            self._init_formatting()
        
        # get template
        template = self._template
        if not template:
            template = self._make_template(value)
        
        # init parts
        parts = {x[0]:0 for x in self._parts}
        
        # split time
        last = None
        for units, f in self._parts:
            
            key = "{%s:" % units
            if key in template:
                
                # get part value
                val = value / float(f)
                value -= int(val) * f
                parts[units] = decimal.Decimal(val)
                
                # remove fractions from higher part
                if last:
                    parts[last] = int(parts[last])
                
                last = units
        
        # init context
        context = decimal.Context()
        
        if self.rounding == ROUNDING.FLOOR:
            context.rounding = decimal.ROUND_DOWN
        elif self.rounding == ROUNDING.CEIL:
            context.rounding = decimal.ROUND_UP
        
        # format with correct rounding
        with decimal.localcontext(context):
            return template.format(**parts)
    
    
    def _init_formatting(self):
        """Initializes formatting based on current settings."""
        
        # reset
        self._template = None
        self._is_dirty = False
        
        # init templates
        self._init_templates()
        
        # use custom template
        if self.template:
            self._template = self._expand_template(self.template, False)
            return
        
        # check domain
        if not self.domain:
            return
        
        # make template
        self._template = self._make_template(abs(self.domain))
    
    
    def _init_templates(self):
        """Initializes templates."""
        
        # init default parts templates
        self._templates_multi = {
            DAYS: "{%s:.0f}" % DAYS,
            HOURS: "{%s:.0f}" % HOURS,
            MINUTES: "{%s:02.0f}" % MINUTES,
            SECONDS: "{%s:02.0f}" % SECONDS,
            MSECONDS: "{%s:03.0f}" % MSECONDS,
            USECONDS: "{%s:03.0f}" % USECONDS,
            NSECONDS: "{%s:03.0f}" % NSECONDS}
        
        # init default singles templates
        self._templates_single = {x[0]: ("{%s:.2f}" % x[0]) for x in self._parts}
        
        # get user-defined templates
        for units, f in self._parts:
            
            # get part template
            template = self.get_property(units+"_template")
            if not template:
                continue
            
            # ensure part name is present
            template = template.replace("{:", "{%s:" % units)
            
            # store template
            self._templates_multi[units] = template
            self._templates_single[units] = template
    
    
    def _make_template(self, domain):
        """Creates template to cover expected range."""
        
        # check current precision
        precision = domain
        if self.precision and self.precision < domain:
            precision = self.precision
        
        # get required parts
        template = []
        for units, f in self._parts:
            
            if domain >= f:
                template.append(units)
            
            if precision >= f:
                break
        
        # get separator
        separator = self.separator
        if separator is UNDEF:
            separator = " " if self.add_units else ":"
        
        # init template
        template = separator.join("{%s}" % x for x in template)
        
        # expand parts
        return self._expand_template(template, self.add_units)
    
    
    def _expand_template(self, template, add_units):
        """Expands template parts."""
        
        # replace parts in template
        for key, tmpl in self._templates_multi.items():
            
            # make full key
            tag = "{%s}" % key
            
            # add units
            if add_units:
                tmpl = tmpl + " %s" % key
            
            # check for singles
            if template == tag:
                units = " %s" % key if add_units else ""
                tmpl = self._templates_single[key] + units
                return template.replace(tag, tmpl)
            
            # replace in template
            template = template.replace(tag, tmpl)
        
        return template
    
    
    def _on_time_formatter_property_changed(self, evt=None):
        """Called after a property has changed."""
        
        self._is_dirty = True
