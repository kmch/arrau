from arrau.generic import Arr, ArrAxis
from plotea.mpl2d import plot_array_1d

class Arr1d(Arr):
  def plot(self, *args, **kwargs):
    plot_array_1d(self.arr, *args, **kwargs)
  # -----------------------------------------------------------------------------  
  def _init_slices(self):
    self.slices = None  
  def _set_axes(self, extent=[None], **kwargs):
    self.axes = kwargs.get('axes', [\
      ArrAxis(param='x', shape=self.shape[0], unit='m', extent=extent[0])
    ])
    return self.axes
  def _set_slice_class(self, **kwargs):
    self.SliceClass = None
class TimeSeries(Arr1d):
  pass
