# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 21:10:05 2020

@author: lenovouser
"""

from tvtk.api import tvtk
from tvtkfunc import ivtk_scene,event_loop
plot3d = tvtk.MultiBlockPLOT3DReader(
        xyz_file_name = "combxyz.bin.sha512",
             q_file_name = "combq.bin.sha512",
             scalar_function_number = 100,vector_function_number = 200)
plot3d.update()
grid = plot3d.output.get_block(0)
mask = tvtk.MaskPoints(random_mode=True,on_ratio=50)
mask.set_input_data(grid)
glyph_source = tvtk.ConeSource()
glyph = tvtk.Glyph3D(input_connection=mask.output_port,scale_factor=4)
glyph.set_source_connection(glyph_source.output_port)
m = tvtk.PolyDataMapper(scalar_range=grid.point_data.scalars.range,input_connection=glyph.output_port)
a = tvtk.Actor(mapper = m)
win = ivtk_scene(a)
win.scene.isometric_view()
event_loop()