#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

# init image
img = pero.Image()

# load json
with open('image.json') as dump:
    img.draw_json(dump.read())

# show image
img.show()
