# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 21:56:36 2020

@author: lenovouser
"""

import numpy as np
from mayavi import mlab
def f(x,y):
    return np.sin(x - y) + np.cos(x + y)
x, y = np.mgrid[-7.:7.05:0.1,-5.:5.05:0.05]
s = mlab.contour_surf(x,y,f)
mlab.show()