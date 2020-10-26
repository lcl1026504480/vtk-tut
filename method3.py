import numpy as np
from mayavi import mlab
from tvtk.api import tvtk

# 宽150.8619：875
# 高33.1265：656
# 间隔0.4


def isosurfacing(data):
    """data should be a 3d array with channel last."""
    # Heuristic for finding the threshold for the brain

    # Exctract the percentile 20 and 80 (without using
    # scipy.stats.scoreatpercentile)
    # sorted_data = np.sort(data.ravel())
    # l = len(sorted_data)
    # lower_thr = sorted_data[int(0.2 * l)]
    # upper_thr = sorted_data[int(0.8 * l)]

    # The white matter boundary: find the densest part of the upper half
    # of histogram, and take a value 10% higher, to cut _in_ the white matter
    # hist, bins = np.histogram(data[data > np.mean(data)], bins=50)
    # brain_thr_idx = np.argmax(hist)
    # brain_thr = bins[brain_thr_idx + 4]

    # del hist, bins, brain_thr_idx

    # Display the data #############################################################

    fig = mlab.figure(bgcolor=(0, 0, 0), size=(400, 500))
    # to speed things up
    fig.scene.disable_render = True

    src = mlab.pipeline.scalar_field(data)
    # Our data is not equally spaced in all directions:
    src.spacing = [1, 1, 20]
    src.update_image_data = True

    #----------------------------------------------------------------------
    # Brain extraction pipeline

    # In the following, we create a Mayavi pipeline that strongly
    # relies on VTK filters. For this, we make heavy use of the
    # mlab.pipeline.user_defined function, to include VTK filters in
    # the Mayavi pipeline.

    # Apply image-based filters to clean up noise
    # thresh_filter = tvtk.ImageThreshold()
    # thresh_filter.threshold_between(lower_thr, upper_thr)
    # thresh = mlab.pipeline.user_defined(src, filter=thresh_filter)

    median_filter = tvtk.ImageMedian3D()

    median_filter.kernel_size = [3, 3, 3]
    median = mlab.pipeline.user_defined(src, filter=median_filter)

    diffuse_filter = tvtk.ImageAnisotropicDiffusion3D(
        diffusion_factor=1.0,
        diffusion_threshold=100.0,
        number_of_iterations=5, )

    diffuse = mlab.pipeline.user_defined(median, filter=diffuse_filter)

    # Extract brain surface
    contour = mlab.pipeline.contour(diffuse, )
    contour.filter.contours = [0.5, ]

    # Apply mesh filter to clean up the mesh (decimation and smoothing)
    dec = mlab.pipeline.decimate_pro(mlab.pipeline.triangle_filter(contour))
    dec.filter.feature_angle = 60.
    dec.filter.target_reduction = 0.5

    smooth_ = tvtk.SmoothPolyDataFilter(
        number_of_iterations=10,
        relaxation_factor=0.1,
        feature_angle=60,
        feature_edge_smoothing=False,
        boundary_smoothing=False,
        convergence=0.,
    )

    smooth = mlab.pipeline.user_defined(dec, filter=smooth_)

    # Get the largest connected region
    connect_ = tvtk.PolyDataConnectivityFilter(extraction_mode=4)
    connect = mlab.pipeline.user_defined(smooth, filter=connect_)

    # Compute normals for shading the surface
    compute_normals = mlab.pipeline.poly_data_normals(connect)
    compute_normals.filter.feature_angle = 80

    surf = mlab.pipeline.surface(compute_normals,
                                 color=(1, 1, 1))

    #----------------------------------------------------------------------
    # Display a cut plane of the raw data
    ipw = mlab.pipeline.image_plane_widget(src, colormap='bone',
                                           plane_orientation='z_axes',
                                           slice_index=55)

    # mlab.view(-165, 32, 350, [143, 133, 73])
    # mlab.roll(180)

    fig.scene.disable_render = False

    #----------------------------------------------------------------------
    # To make the link between the Mayavi pipeline and the much more
    # complex VTK pipeline, we display both:
    mlab.show_pipeline(rich_view=False)
    from tvtk.pipeline.browser import PipelineBrowser
    browser = PipelineBrowser(fig.scene)
    browser.show()

    mlab.show()


import cv2 as cv
import glob
images = []
d = len(glob.glob("process/*"))
path = ["process/%d.png" % i for i in range(1, d, 5)]
for fn in path:
    print(fn)
    images.append(cv.resize(cv.imread(fn, 0), (1500, 330)) / 255)

images = np.array(images)
images = np.swapaxes(images, 0, -1)
isosurfacing(images)
