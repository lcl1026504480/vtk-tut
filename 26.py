# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:06:44 2020

@author: lenovouser
"""

#coding=gbk
from mayavi import mlab
import numpy as np
from tvtk.api import tvtk
from tvtk.common import configure_input
from tvtkfunc import ivtk_scene, event_loop

pi = np.pi
cos = np.cos
sin = np.sin
mgrid = np.mgrid

r,theta = pi/250,pi/250
[r,theta] = np.mgrid[0:1:10j,0:2*pi:10j]

x = r * cos(theta)
y = r * sin(theta)
z = r * r
s = x * y * z
s = scalars
s = mlab.mesh(scalars,x,y,z)

plot3d = tvtk.MultiBlockPLOT3DReader(
        xyz_file_name="s",
        q_file_name="s",
        scalar_function_number=100, vector_function_number=200
    )#读入Plot3D数据
plot3d.update()#让plot3D计算其输出数据
grid = plot3d.output.get_block(0)#获取读入的数据集对象
outline = tvtk.StructuredGridOutlineFilter()#计算表示外边框的PolyData对象
configure_input(outline, grid)#调用tvtk.common.configure_input()
m = tvtk.PolyDataMapper(input_connection=outline.output_port)
a = tvtk.Actor(mapper=m)
a.property.color = 0.3, 0.3, 0.3

#窗口绘制
win = ivtk_scene(a)
win.scene.isometric_view()
event_loop()

mlab.show()