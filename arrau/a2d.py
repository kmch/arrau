from arrau.a1d import Arr1d
from arrau.generic import Arr, ArrAxis, ArrSlices
from plotea.mpl2d import Contour, Contourf, Imshow, Shade

class Arr2dPlotter:
  """
  Mix-in.
  """
  def plot(self, mode='imshow', **kwargs):
    kwargs = self._get_formatting_for_plot(**kwargs)
    # framework
    if mode == 'imshow' or mode == 'im':
      self._imshow(**kwargs)
    elif mode == 'contour' or mode == 'cr':
      self._contour(**kwargs)
    elif mode == 'contourf' or mode == 'cf':
      self._contourf(**kwargs)      
    elif mode == 'im+cr':
      self._imshow_plus_contour(**kwargs)
    elif mode == 'shade':
      self._shade(**kwargs)
    else:
      raise ValueError('Wrong mode: %s' % mode)
  # -----------------------------------------------------------------------------  
  def _contour(self, **kwargs):
    kwargs['extent'] = self._get_extent_for_contour()
    Contour().plot(self.arr, **kwargs)
  def _contourf(self, **kwargs):
    kwargs['extent'] = self._get_extent_for_contour()
    Contourf().plot(self.arr, **kwargs)    
  def _get_axis_labels(self, **kwargs):
    kwargs['xlabel'] = kwargs.get('xlabel', self.axes[0].label)
    kwargs['ylabel'] = kwargs.get('ylabel', self.axes[1].label)
    return kwargs    
  def _get_extent_for_contour(self):
    """
    Set formatting of the extent
    compatible with plotters such as
    plt.contour.

    Returns
    -------
    list
        Extent of format accepted by
        plt.contour.
    
    Notes
    -----
    Different from imshow!
    """
    x1, x2 = self.axes[0].extent
    y1, y2 = self.axes[1].extent
    extent = [x1, x2, y1, y2]
    return extent  
  def _get_extent_for_imshow(self):
    """
    Set formatting of the extent
    compatible with plotters such as
    plt.imshow.

    Returns
    -------
    list
        Extent of format accepted by
        plt.imshow.
    """
    x1, x2 = self.axes[0].extent
    y1, y2 = self.axes[1].extent
    extent = [x1, x2, y2, y1] # NOTE y1, y2 are swapped
    return extent  
  def _get_formatting_for_plot(self, **kwargs):
    kwargs = self._get_axis_labels(**kwargs)
    return kwargs  
  def _imshow(self, **kwargs):
    kwargs['extent'] = self._get_extent_for_imshow()
    Imshow().plot(self.arr, **kwargs)
  def _imshow_plus_contour(self, **kwargs):
    self._imshow(**kwargs)
    kwargs['invert_vertical_axis'] = False
    self._contour(**kwargs)
  def _shade(self, **kwargs):
    kwargs['extent'] = self._get_extent_for_imshow()
    Shade().plot(self.arr, **kwargs)    
class Arr2d(Arr,Arr2dPlotter):
  """
  2d array.
  """
  def _init_slices(self):
    self.slices = Arr2dSlices()  
  def _set_axes(self, extent=[None]*2, **kwargs):
    self.axes = kwargs.get('axes', [\
      ArrAxis(param='x', shape=self.shape[0], unit='m', extent=extent[0]),
      ArrAxis(param='y', shape=self.shape[1], unit='m', extent=extent[1])
    ])
    return self.axes
  def _set_slice_class(self, **kwargs):
    self.SliceClass = Arr1d
class Arr2dSlices(ArrSlices):
  def _add_slice(self, value, axis, array):
    SliceClass = {0: Arr2dSliceX, 1: Arr2dSliceY}
    new_slice = SliceClass[axis](value, axis, array, self)
    self.list.append(new_slice)  
  def _init_values(self):
      xvalues = []
      yvalues = []
      self.values = [xvalues, yvalues]
class Arr2dSlice:
  def __init__(self, value, axis, arr, all_slices):
    """
    Parameters
    ----------
    value : see Arr.slice
    axis : see Arr.slice
    arr : Arr
    all_slices : ArrSlices
    """
    self.all_slices = all_slices
    self.arr = arr
    self.axis = axis
    self.value = value
    # self._pick_slice_values()
    # self._set_axes_labels()
    # self._set_axes_order()
    # self._set_vertical_axis_up()
class Arr2dSliceX(Arr2dSlice):
  def _set_axes_labels(self):
    self.arr.axes[0].label = 'y, m'
  def _set_vertical_axis_up(self):
    self.vertical_axis_up = False  
  def _pick_slice_values(self):
    self.vals = self.all_slices.values[1]
class Arr2dSliceY(Arr2dSlice):
  def _set_axes_labels(self):
    self.arr.axes[0].label = 'x, m'
  def _set_vertical_axis_up(self):
    self.vertical_axis_up = False  
  def _pick_slice_values(self):
    self.vvals = self.all_slices.values[0]
class Surf(Arr2d):
  def _set_axes_labels(self):
    self.axes[0].label = 'x, m'
    self.axes[1].label = 'y, m'