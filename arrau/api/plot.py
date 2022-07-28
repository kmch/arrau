"""
Plotting API. Currently the only 'backend' is 
the `plotea` package.
"""
# import matplotlib.pyplot as plt # for interlace only
import numpy as np
from plotea.ipyvolume import Ipv
from plotea.mpl2d import Contour, Contourf, Imshow, Shade, Wiggle,\
  PltPlot, figax

class Arr1dPlot:
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
class Arr2dPlot:
  """
  Mix-in.
  """
  # def plot_interlaced(self, arr, **kwargs):
  #   # extent will be default, even better for setting grid lines 

  #   self.plot(**kwargs) # Dat will use Dat.plot etc. ?
  #   xticks = np.arange(len(self.arr))[::chunk_size] - .5     
  #   ax = plt.gca()
  #   # ax.set_title('Interlaced traces.')
  #   ax.set_xticks(xticks)
  #   ax.grid(axis='x', c='k', linestyle='-.', linewidth=1)  
  #   empty_string_labels = ['']*len(xticks)
  #   _ = ax.set_xticklabels(empty_string_labels) 
  #   return ax 
  def plot(self, mode='imshow', **kwargs):
    """
    Parameters
    ----------
    mode : str
        'imshow' / 'contour' / 'contourf' / 'im+cr' / 'shade'
        Default: 'imshow'.
    """
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
    elif mode == 'wiggle':
      self._wiggle(**kwargs)
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
  def _wiggle(self, **kwargs):
    Wiggle().plot(self.arr, **kwargs) 
class Arr2dSlicePlot:
  def plot(self, **kwargs):
    self.arr.plot(**kwargs)
class Arr3dPlot:
  def volshow(self, **kwargs):
    return Ipv.volshow(self.arr, **kwargs)
  def plot_interface(self, **kwargs):
    """
    Framework plotter.
    
    Notes
    -----
    This is a preferred function to call rather than
    plot_3slices directly. This is because plot 
    formatting is set in subclasses by overwriting
    plot method. This could be avoided by defining
    _format_plot() method or similar.
    """
    x = kwargs.get('x', None)
    y = kwargs.get('y', None)
    z = kwargs.get('z', None)

    # choose the slices based on kwargs
    if not ('x' in kwargs or 'y' in kwargs or 'z' in kwargs):
      nslices = 1 # actually make it 3 slices through centre
      raise ValueError('Slicing type not implemented')
    elif 'x' in kwargs and 'y' in kwargs and 'z' in kwargs:
      self.plot_3slices(x, y, z, **kwargs)
    elif 'x' in kwargs and not ('y' in kwargs or 'z' in kwargs):
      nslices = 1
      kwargs['axis'] = 0
      kwargs['value'] = kwargs['x'] 
    elif 'y' in kwargs and not ('x' in kwargs or 'z' in kwargs):
      nslices = 1
      kwargs['axis'] = 1
      kwargs['value'] = kwargs['y'] 
    elif 'z' in kwargs and not ('x' in kwargs or 'y' in kwargs):
      nslices = 1
      kwargs['axis'] = 2
      kwargs['value'] = kwargs['z']   
    else:
      raise ValueError('Slicing arguments not understood.')
    # choose the plotting function
    if nslices == 1:
      self.plot_slice(**kwargs)
    elif nslices == 3:
      self.plot_3slices(**kwargs)
    else:
      raise ValueError('Wrong value of nslices: %s' %str(nslices))
    return plt.gca()
  def plot(self, *args, **kwargs):
    self.slice(*args, **kwargs)
    self.slices.list[-1].plot(**kwargs)
  def plot_3slices(self, x, y, z, unit='m', **kwargs):
    self.slice(x, axis=0, unit=unit)
    self.slice(y, axis=1, unit=unit)
    self.slice(z, axis=2, unit=unit)
    linecolor = kwargs.get('linecolor', 'k')
    for sl in self.slices.list:
      fig, ax = figax()
      sl.plot(**kwargs)
      sl.plot_slice_lines(color=linecolor)
class Arr3dSlicePlot:
  def plot(self, **kwargs):
    # Allow to overwrite the default to prevent multiple flipping
    # when plotting multi-layer data
    kwargs['vertical_axis_up'] = kwargs.get('vertical_axis_up', \
      self.vertical_axis_up)
    self.arr.plot(**kwargs)
  def plot_slice_lines(self, color='k', linestyle='--', lw=1):
    vlines = self._get_slice_lines(is_vertical=True)
    hlines = self._get_slice_lines(is_vertical=False)
    for line in vlines + hlines:
      PltPlot().plot(line.ordinates, xaxis=line.abscissas,\
        color=color, linestyle=linestyle, lw=lw)
