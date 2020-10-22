# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 21:48:03 2020

@author: lenovouser
"""

import numpy as np
from mayavi import mlab
import cv2

n_mer, n_long = 6, 11
dphi = np.pi / 1000.0
phi = np.arange(0.0, 2 * np.pi + 0.5 * dphi, dphi)
mu = phi * n_mer
x = np.cos(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
y = np.sin(mu) * (1 + np.cos(n_long * mu / n_mer) * 0.5)
z = np.sin(n_long * mu / n_mer) * 0.5
l = mlab.plot3d(x, y, z, np.sin(mu), tube_radius=0.025, colormap="Spectral")
