# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 22:01:02 2020

@author: lenovouser
"""

import numpy
from mayavi import mlab
x,y,z = numpy.mgrid[-5:5:64j,-5:5:64j,-5:5:64j]
scalars = x * x + y * y + z * z
x,y,z=np.mgrid[-2:3,-2:3,-2:3]
#obj = mlab.contour3d(scalars, contours=8,transparent=True)
r = np.sqrt(x ** 2 + y ** 2 + z ** 4)
u = y * np.sin(r) / (r + 0.001)
v = -x * np.sin(r)/ (r + 0.001)
w = np.zeros_like(z)
obj = mlab.quiver3d(x,y,z,u,v,w,line_width=3,scale_factor=1)