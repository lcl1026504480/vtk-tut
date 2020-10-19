# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 20:41:56 2020

@author: lenovouser
"""
x=[[-1,1,1,-1,-1]]*2
y=[[-1]*5,[1]*5]
z=[[1,1,-1,-1,1],[1,1,-1,-1,1]]
from mayavi import mlab
mlab.mesh(x,y,z)
