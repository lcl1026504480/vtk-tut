# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 21:13:18 2020

@author: lenovouser
"""

from tvtk.api import tvtk
from tvtkfunc import ivtk_scene,event_loop
s = tvtk.OBJReader(file_name = 'arm.obj')
m = tvtk.PolyDataMapper(input_connection = s.output_port)
a = tvtk.Actor(mapper=m)
win = ivtk_scene(a)
win.scene.isometric_view()
event_loop()