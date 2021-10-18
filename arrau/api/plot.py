"""
Plot API.
"""
import numpy as np
from plotea.mpl2d import PltPlot

class PlotArr1d:
  def plot(self, mode='plt', **kwargs):
    self._set_xaxis()
    if mode == 'plt':
      self._plt_plot(**kwargs)
    else:
      raise ValueError('Unknown mode:', mode)
  # -----------------------------------------------------------------------------    
  def _plt_plot(self, **kwargs):
    kwargs['xaxis'] = kwargs.get('xaxis', self.xaxis)
    PltPlot().plot(self.arr, **kwargs)
  def _set_xaxis(self):
    axis = self.axes[0]
    x1, x2 = axis.extent
    nsampl = len(self.arr)
    self.xaxis = np.linspace(x1, x2, nsampl)
class PlotArr3d:
  def plot(self, xyz, unit='m'):
    x, y, z = xyz
    self.slice(x, axis=0, unit=unit)
    self.slice(y, axis=1, unit=unit)
    self.slice(z, axis=2, unit=unit)
    for sl in self.slices.list:
      sl.plot()
      sl.plot_slice_lines()
class PlotArr3dSlice:
  def plot(self, **kwargs):
    # Allow to overwrite the default to prevent multiple flipping
    # when plotting multi-layer data
    kwargs['vertical_axis_up'] = kwargs.get('vertical_axis_up', \
      self.vertical_axis_up)
    self.arr.plot(**kwargs)
  def plot_slice_lines(self):
    vlines = self._get_slice_lines(is_vertical=True)
    hlines = self._get_slice_lines(is_vertical=False)
    for line in vlines + hlines:
      PltPlot().plot(line.ordinates, xaxis=line.abscissas,\
        color='k', linestyle='--')
      # plt.plot(line.abscissas, line.ordinates,  'k--')
