from mayavi import mlab
from mayavi.tools import pipeline
src = mlab.pipeline.scalar_field(s)
mlab.pipeline.iso_surface(src,contours=[s.min()+0.1*s.ptp(),],opacity=0.1)
mlab.pipeline.iso_surface(src,contours=[s.max()-0.1*s.ptp(),])
mlab.pipeline.image_plane_widget(src,
                 plane_orientation="z_axes",
                 slice_index=10,
                )
mlab.show()