#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

# JSON dump
dump = """{"commands": [
    ["set_property", {"name": "height", "value": 400}],
    ["set_property", {"name": "width", "value": 400}],
    ["set_property", {"name": "line_cap", "value": "round"}],
    ["set_property", {"name": "line_join", "value": "round"}],
    ["set_property", {"name": "fill_color", "value": "#ffffffff"}],
    ["fill", {}],
    
    ["set_property", {"name": "line_width", "value": 3}],
    ["set_property", {"name": "line_color", "value": "#e69500ff"}],
    ["set_property", {"name": "fill_color", "value": "#ffa500ff"}],
    ["draw_circle", {"x": 200, "y": 200, "radius": 150}],
    
    ["set_property", {"name": "line_color", "value": null}],
    ["set_property", {"name": "fill_color", "value": "#e6e6e6ff"}],
    ["draw_ellipse", {"x": 200, "y": 370, "width": 100, "height": 20}],
    
    ["set_property", {"name": "fill_color", "value": "#000000ff"}],
    ["draw_circle", {"x": 140, "y": 170, "radius": 30}],
    ["draw_circle", {"x": 260, "y": 170, "radius": 30}],
    
    ["set_property", {"name": "line_color", "value": "#000000ff"}],
    ["set_property", {"name": "fill_color", "value": null}],
    ["set_property", {"name": "line_width", "value": 7}],
    ["draw_arc", {"x": 140, "y": 170, "radius": 45, "start_angle": -1.7453292519943295, "end_angle": -0.3490658503988659, "clockwise": true}],
    ["draw_arc", {"x": 260, "y": 170, "radius": 45, "start_angle": 3.490658503988659, "end_angle": 4.886921905584122, "clockwise": true}],
    
    ["set_property", {"name": "line_width", "value": 10}],
    ["draw_arc", {"x": 200, "y": 200, "radius": 100, "start_angle": 0.6981317007977318, "end_angle": 1.3962634015954636, "clockwise": true}],
    
    ["set_property", {"name": "line_color", "value": "#ffc04dff"}],
    ["draw_arc", {"x": 200, "y": 200, "radius": 135, "start_angle": 3.839724354387525, "end_angle": 4.537856055185257, "clockwise": true}],
    
    ["set_property", {"name": "line_color", "value": null}],
    ["set_property", {"name": "fill_color", "value": "#000000ff"}],
    ["draw_path", {"path": {"fill_rule": "winding", "commands": [
        ["M", 253.01312221547863, 54.34764377818418],
        ["C", 273.77223837502214, 61.90334414993255, 289.06955070659535, 72.23559667918414, 287.18062561365826, 77.42537571907002],
        ["C", 285.2917005207212, 82.6151547589559, 266.93183550850875, 80.6971965656507, 246.17271934896524, 73.14149619390236],
        ["C", 225.41360318942174, 65.58579582215398, 210.11629085784853, 55.25354329290239, 212.0052159507856, 50.063764253016515],
        ["C", 213.8941410437227, 44.87398521313064, 232.25400605593512, 46.79194340643582, 253.01312221547863, 54.34764377818418],
        ["Z"],
        ["M", 259.853525081992, 35.553791362466],
        ["C", 272.82797268170674, 40.276104094808744, 281.81456426132013, 48.31144211358094, 279.92563916838304, 53.501221153466815],
        ["C", 278.03671407544596, 58.69100019335269, 265.98756981519335, 59.06995651052691, 253.01312221547863, 54.34764377818418],
        ["C", 240.03867461576397, 49.62533104584146, 231.05208303615052, 41.589993027069255, 232.9410081290876, 36.40021398718338],
        ["C", 234.8299332220247, 31.2104349472975, 246.87907748227735, 30.831478630123286, 259.853525081992, 35.553791362466],
        ["Z"],
        ["M", 232.9410081290876, 36.40021398718338],
        ["L", 279.92563916838304, 53.501221153466815],
        ["L", 273.08523630186966, 72.29507356918498],
        ["L", 226.10060526257422, 55.19406640290154],
        ["Z"]]}}]]
}"""

# draw image
img = pero.Image()
img.draw_json(dump)
img.show()
