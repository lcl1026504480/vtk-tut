import pyvista as pv
import numpy as np
## 生成一组点云的坐标，然后构建点云的mesh
points = np.random.rand(30000, 3)
point_cloud = pv.PolyData(points)
print (np.allclose(points, point_cloud.points))
#检测是否一致
# 画点云
point_cloud.plot(eye_dome_lighting=True)