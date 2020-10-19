#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero

# create venn
venn = pero.venn.Venn(
    10, 8, 22, 6, 9, 4, 2,
    palette = pero.colors.Set2,
    mode = pero.venn.SEMI)

# show diagram
venn.show("Venn Diagram", width=400, height=400)
