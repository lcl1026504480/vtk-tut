# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 21:54:55 2020

@author: lenovouser
"""


import numpy
from mayavi import mlab
s = numpy.random.random((10,10))
img = mlab.imshow(s,colormap='gist_earth')
mlab.show()