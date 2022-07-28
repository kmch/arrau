import numpy as np

from arrau.a2d import Arr2d
from arrau.api.plot import Arr3dPlot, Arr3dSlicePlot
from arrau.generic import Arr, ArrAxis, ArrSlices

class Arr3d(Arr,Arr3dPlot):
  """
  3d array.
  """
  def _init_slices(self):
    self.slices = Arr3dSlices()  
  def _set_axes(self, extent=[None]*3, **kwargs):
    self.axes = kwargs.get('axes', [\
      ArrAxis(param='x', shape=self.shape[0], unit='m', extent=extent[0]),
      ArrAxis(param='y', shape=self.shape[1], unit='m', extent=extent[1]),
      ArrAxis(param='z', shape=self.shape[2], unit='m', extent=extent[2])
    ])
    return self.axes
  def _set_slice_class(self, **kwargs):
    self.SliceClass = Arr2d
class Arr3dSlices(ArrSlices):
  def _add_slice(self, value, axis, array):
    SliceClass = {0: Arr3dSliceX, 1: Arr3dSliceY, 2: Arr3dSliceZ}
    new_slice = SliceClass[axis](value, axis, array, self)
    self.list.append(new_slice)    
  def _init_values(self):
      xvalues = []
      yvalues = []
      zvalues = []
      self.values = [xvalues, yvalues, zvalues]
class Arr3dSlice(Arr3dSlicePlot):
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
    self._pick_slice_values()
    self._set_axes_labels()
    self._set_axes_order()
    self._set_vertical_axis_up()
  # -----------------------------------------------------------------------------    
  def _get_slice_lines(self, is_vertical):
    if is_vertical:
      axis = self.vaxis
      vals = self.vvals
    else:
      axis = self.haxis
      vals = self.hvals

    v1, v2 = self.arr.axes[axis].extent
    n = self.arr.shape[axis]
    
    lines = []
    for v in vals:
      abscissas = np.linspace(v1, v2, n)
      ordinates = np.full(n, v)
      if is_vertical: # swap
        abscissas, ordinates = ordinates, abscissas
      lines.append(Arr3dSliceLine(abscissas, ordinates))
    return lines
  def _set_axes_order(self):
    self.haxis = 0 
    self.vaxis = 1
class Arr3dSliceX(Arr3dSlice):
  """
  YZ plane.
  """
  def _set_axes_labels(self):
    self.arr.axes[0].label = 'Y (m)'
    self.arr.axes[1].label = 'Z (m)'   
  def _set_vertical_axis_up(self):
    self.vertical_axis_up = False  
  def _pick_slice_values(self):
    self.vvals = self.all_slices.values[1]
    self.hvals = self.all_slices.values[2]
class Arr3dSliceY(Arr3dSlice):
  """
  XZ
  """
  def _set_axes_labels(self):
    self.arr.axes[0].label = 'X (m)'
    self.arr.axes[1].label = 'Z (m)'  
  def _set_vertical_axis_up(self):
    self.vertical_axis_up = False  
  def _pick_slice_values(self):
    self.vvals = self.all_slices.values[0]
    self.hvals = self.all_slices.values[2]
class Arr3dSliceZ(Arr3dSlice):
  """
  XY plane
  """
  def _set_axes_labels(self):
    self.arr.axes[0].label = 'X (m)'
    self.arr.axes[1].label = 'Y (m)'
  def _set_vertical_axis_up(self):
    self.vertical_axis_up = True
  def _pick_slice_values(self):
    self.vvals = self.all_slices.values[0]
    self.hvals = self.all_slices.values[1]
class Arr3dSliceLine:
  def __init__(self, abscissas, ordinates):
    self.abscissas = abscissas
    self.ordinates = ordinates
