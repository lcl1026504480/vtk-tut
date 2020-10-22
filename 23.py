# import numpy as np
# from mayavi import mlab
#建立数据
#x,y = np.mgrid[-10:10:200j,-10:10:200j]
#z = 100 * np.sin(x * y) / (x * y)
##对数据进行可视化
#mlab.figure(bgcolor=(1,1,1))
#surf = mlab.surf(z,colormap='cool')
#mlab.show()
##访问surf对象的LUT
#用mlab.points3d建立红色和白色小球的集合
#选取事件

import numpy as np
from mayavi import mlab
figure = mlab.gcf()
x1, y1, z1 = np.random.random((3, 10))
red_glyphs = mlab.points3d(x1, y1, z1, color=(1, 0, 0),
                           resolution=100)
x2, y2, z2 = np.random.random((3, 10))
white_glyphs = mlab.points3d(x2, y2, z2, color=(0.9, 0.9, 0.9),
                             resolution=5)
outline = mlab.outline(line_width=3)
outline.outline_mode = 'cornered'
outline.bounds = (x1[0] - 0.1, x1[0] + 0.1,
                  y1[0] - 0.1, y1[0] + 0.1,
                  z1[0] - 0.1, z1[0] + 0.1)
glyph_points = red_glyphs.glyph.glyph_source.glyph_source.output.points.to_array()
def picker_callback(picker):
    if picker.actor in red_glyphs.actor.actors:
        point_id = int(picker.point_id / glyph_points.shape[0])
        if point_id != -1:
            x, y, z = x1[point_id], y1[point_id], z1[point_id]
            outline.bounds = (x - 0.1, x + 0.1,
                              y - 0.1, y + 0.1,
                              z - 0.1, z + 0.1)
picker = figure.on_mouse_pick(picker_callback)
mlab.title('Click on red balls')
mlab.show()