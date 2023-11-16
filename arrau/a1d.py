import numpy as np
from arrau.plot import Arr1dPlot
from arrau.generic import Arr, ArrAxis


class Arr1d(Arr,Arr1dPlot):
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
