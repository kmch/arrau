from arrau.a1d import Arr1d
from arrau.plot import Arr2dPlot, Arr2dSlicePlot
from arrau.generic import Arr, ArrAxis, ArrSlices
from arrau.modify import interlace_arrays


class Arr2d(Arr,Arr2dPlot):
  """
  2d array.
  """
  def interlace(self, other_arr2d, chunk_size=10, **kwargs):
    arr = Arr2d(interlace_arrays(self.arr, other_arr2d.arr, chunk_size))
    return arr
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
class Arr2dSlice(Arr2dSlicePlot):
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
class A2d(Arr2d):
  def _metre_2_nearest_index(self, m, axis, **kwargs):
    origin = self.extent[axis][0]
    i = (m - origin) / self.dx[axis]
    if not i.is_integer():
      print('Warning. Non-integer index. Taking its floor')
      i = np.floor(i)
    return int(i)        
  def plot_slice(self, coord, unit='n', axis='y', **kwargs):
    kwargs['slice_at'] = axis
    axis_id = dict(x=0, y=1, z=2)[axis]
    if unit == 'n':
      kwargs['node'] = coord
    elif unit == 'm':
      i = self._metre_2_nearest_index(coord, axis_id)
      if (i < 0) or (i >= self.shape[axis_id]):
        raise IndexError('Incorrect array index: %s' %i)
      kwargs['title'] = '%s=%s m' % (axis, coord) 
      kwargs['node'] = i 
    else:
      NIErr()
    return super().plot_slice(**kwargs)
