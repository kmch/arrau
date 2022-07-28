"""
Dimension-independent abstract arrays
and auxiliary objects.
"""
from abc import ABC, abstractmethod
import numpy as np

from arrau.modify import modify_array

class Arr(ABC):
  """
  Abstract 1-3d array.
  
  """
  def __init__(self, array, **kwargs):
    """
    Parameters
    ----------
    array : arrauay
        1d, 2d or 3d.
    axes : list
        List of ArrAxis elements.
    extent : list
        List of pairs [vmin, vmax], by default None.
    """
    self.shape = array.shape
    self.nd = len(self.shape)
    self.axes = self._set_axes(**kwargs)
    self._set_axes_labels()
    self.arr = array
    self._set_slice_class()
    self._init_slices()
  def extract(self, extent):
    """
    Extract a subarray from the array.

    Parameters
    ----------
    extent : list
        [[x1, x2], ...] in metres.
    """
    array = self.arr
    indices = []
    for axis, (m1, m2) in enumerate(extent):
      assert m1 >= self.axes[axis].extent[0]
      assert m2 <= self.axes[axis].extent[1]
      i1 = self._get_slice_index(m1, 'm', axis)
      i2 = self._get_slice_index(m2, 'm', axis)
      indices.append([i1, i2])
    # print('indices', indices)
    for axis, (i1,i2) in enumerate(indices):
      array = np.take(array, np.arange(i1, i2+1), axis=axis)
    return self.__class__(array, extent=extent) 
  def info(self):
    """
    Print some useful info about the erray.
    """
    print('grid shape: {} [nodes]'.format(self.shape))
    print('grid cell-size (dx): {} [m]'.format(self.dx))    
    print('grid extent: {} [m]'.format(self.extent))
    print('value min: {}, max: {}'.format(np.min(self.arr), np.max(self.arr)))
  def modify(self, **kwargs):
    self.arr = modify_array(self.arr, **kwargs)
  def normalise(self, norm='max'):
    self.arr = modify_array(self.arr, norm=norm)  
  def read(self, overwrite=True, **kwargs):
    """
  
    Notes
    -----
    Overwrite=True by default because otherwise plots are not 
    updated even though they are supposed to. 
    They will be correct (updated) only
    if you delete self.array variable, e.g. by restarting the 
    notebook kernel.
    Disable overwrite only for PERFORMANCE (e.g. interactive plot)
    when the array remains unchanged unlike other (e.g. plotting)
    parameters.
    
    """
    # from fullwavepy.ndat.arrays import Arr3d
    
    # if (not hasattr(self, 'array')) or overwrite:
    #   self.__log.debug('{}.array does not exist and will be read.'.format(type(self)))
    #   self.array = Arr3d(self.fname, **kwargs)
    
    # return self.array 
    pass 
  def slice(self, value, unit='index', axis=0, **kwargs):
    """
    Slice the array at a single value
    along a given axis.

    Parameters
    ----------
    value : float
        Value of coordinate to slice at, in units
        defined by 'unit'.
    unit : str, optional
        Unit of coordinate value, by default 'index'
        (that stands for array index). 
        Other options: 'metre', 'node'. 
        The only difference between 'node' and 'index' is that
        the former starts at 1, and the latter at 0.     
    axis : int, optional
        Axis along which to slice, by default 0 (first).
    
    Returns
    -------
    array : type defined by _set_slice_class()
        Sliced array.
    """
    # prep the slicing
    index = self._get_slice_index(value, unit, axis)
    self._check_slice_index(index, axis)
    # do the slicing
    axes = self._slice_axes(axis)
    array = self._slice_array(index, axis)
    array = self.SliceClass(array, axes=axes)
    # add the slice to the list
    self.slices.add(value, axis, array)
    return array
  # -----------------------------------------------------------------------------
  def _check_slice_index(self, index, axis):
    if (index < 0) or (index >= self.shape[axis]):
      raise IndexError('Incorrect array index: %s' % index)
  def _get_slice_index(self, value, unit, axis):
    """
    Calculate array index to slice at
    based on the provided coordinate
    in specified units.

    Parameters
    ----------
    See slice().

    Returns
    -------
    int
        Index at which the array
        will be sliced.
    """
    ax = self.axes[axis]
    if unit == 'index' or unit == 'i':
      index = value
    elif unit == 'node' or unit == 'n':
      index = CoordTransform().node2index(value)
    elif unit == 'metre' or unit == 'm':
      origin = ax.extent[0]
      dx = ax.dx
      index = CoordTransform().metre2index(value, origin, dx)
    elif unit == 'kilometre' or unit == 'km':
      origin = ax.extent[0]
      dx = ax.dx
      # use metre2index as nothing changes (origin and dx are in km)
      index = CoordTransform().metre2index(value, origin, dx)    
    else:
      raise ValueError('Unknown unit: %s.' % unit)    
    return index      
  def _set_axes_labels(self):
    for ax in self.axes:
      ax.label = None
  def _slice_array(self, index, axis):
    """
    Slice the array at a single index
    along a given axis.

    Parameters
    ----------
    index : int
        Index to slice at.
    axis : int
        Axis to slice along.

    Returns
    -------
    arrauay
        Sliced array.
    """
    return np.take(self.arr, indices=index, axis=axis)
  def _slice_axes(self, axis):
    """
    Slice array axes.

    Parameters
    ----------
    axis : int
        Axis of slicing.

    Returns
    -------
    list
        Sliced axes.

    """    
    axes = [ax for i, ax in enumerate(self.axes) if i != axis]
    return axes
  # -----------------------------------------------------------------------------
  @abstractmethod
  def _init_slices(self):
    pass
  @abstractmethod
  def _set_axes(self, **kwargs):
    """
    Set axes of a ND array.

    Parameters
    ----------
    extent : list, optional
        By default [None] * ND. If axes are provided,
        the custom extent will have no effect.
    axes : list, optional
        See child classes for defaults.

    Returns
    -------
    list
        ND-element list of  axes.
    """
    return axes  
  @abstractmethod
  def _set_slice_class(self, **kwargs):
    self.SliceClass = None
class ArrAxis:
  def __init__(self, param, shape, unit='m', extent=None, label=None):
    """
    Initialise the axis.

    Parameters
    ----------
    param : str
        ID of a physical parameter (e.g. a coordinate)
        associated with the axis.
    shape : int
        Number of points of the axis.
    unit : str, optional
        Unit of the param, by default 'm'
    extent : list, optional
        Range of values [vmin, vmax] corresponding to 
        the first and the last point of the axis, by default None,
        which invokes the _extent_default method.
    """
    self.param = param
    self.shape = shape
    self.unit = unit
    self.label = label
    self.set_extent(extent)
  def set_extent(self, extent):
    """
    Set the extent of the axis in metres.

    Returns
    -------
    extent: array
      FIXME, obsolete description:
      For a 1d array it is np.array([[xmin, xmax]]).
      For a 2d array it is np.array([[xmin, xmax], [ymin, ymax]])
      For a 3d array it is np.array([[xmin, xmax], [ymin, ymax], [zmin, zmax]])
    
    Notes
    -----
    Every time new extent is set, dx is also set accordingly.
    """
    self.extent = self._extent_default() if extent is None else extent
    self._check_extent(self.extent)
    self._set_dx()
    return self.extent    
  # -----------------------------------------------------------------------------
  def _check_extent(self, extent):
    """
    Check if the extent has a correct 
    form.

    Parameters
    ----------
    extent : array
      Its correct form is checked by this function.    
    """
    assert len(extent) == 2  
  def _extent_default(self):
    """
    Returns
    -------
    list
        Default extent in units.
    """
    extent = [0, self.shape-1]
    return extent
  def _set_dx(self):
    """
    Set the cell size in metres,
    based on the extent and shape.

    Returns
    -------
    dx : float 
      In metres.
      
    """
    # dx = []
    # self.__log.debug('self.shape %s' % str(self.shape))
    # self.__log.debug('self.extent %s' % str(self.extent))
    # for nx, (x1, x2) in zip(self.shape, self.extent):
      # self.__log.debug('nx=%s, x1=%s, x2=%s' % (nx, x1, x2))
      # dx_1D = (x2 - x1) / (nx-1) if nx > 1 else None
      # self.__log.debug('dx_1D=%s' % dx_1D)
      # dx.append(dx_1D)
    # return np.array(dx)
    nx = self.shape
    x1, x2 = self.extent
    dx = (x2 - x1) / (nx-1) if nx > 1 else None
    self.dx = dx
    return self.dx
class ArrSlices(ABC):
  def __init__(self):
    if hasattr(self, 'list'):
      # self.__log.debug('Already has "list" attribute.')
      pass
    else:
      self.list = []
      self._init_values()
  def add(self, value, axis, array):
    """
    Add a slice to array-slices.

    Parameters
    ----------
    value : See Arr.slice
    axis : See Arr.slice
    array : See Arr.slice
        Array returned by Arr.slice.
    """
    # check
    if self._on_the_list(value, axis):
      # self.__log.debug('This slice is already on the list.')
      return
    # add
    self._add_slice(value, axis, array)
    self._add_slice_value(value, axis)
  def plot(self, slice_no, **kwargs):
    self.list[slice_no].plot(**kwargs)
  # -----------------------------------------------------------------------------
  def _add_slice_value(self, value, axis):
    self.values[axis].append(value)     
  def _on_the_list(self, value, axis):
    is_in = False
    for sli in self.list:
      if sli.value == value and sli.axis == axis:
        is_in = True
        break
    return is_in
  # -----------------------------------------------------------------------------  
  @abstractmethod
  def _add_slice(self, value, axis, array):
    pass  
  @abstractmethod
  def _init_values(self):
    pass    

class CoordTransform(ABC):
  """
  Collection of transformations between various coordinate
  systems useful for array manipulations.
  """
  def node2index(self, node):
    assert node >= 1
    return node - 1
  # -----------------------------------------------------------------------------
  def index2node(self, index):
    return index + 1
  # -----------------------------------------------------------------------------  
  # def kilometre2index(self, m, origin, dx, **kwargs):
  #   # this 
  #   return self.metre2index(m, origin, dx, **kwargs)
  def metre2index(self, m, origin, dx, **kwargs):
    """
    Convert metres to array index. If the result
    is not an integer, the nearest integer is used.

    Parameters
    ----------
    m : float
        Value in metres.
    origin : float
        Origin of coordinate axis.
    dx : float
        Grid interval along the axis.
    
    Returns
    -------
    int
        Nearest index.
    """
    # origin = self.extent[axis][0]
    i = (m - origin) / dx #self.dx[axis]
    if not i.is_integer():
      # self.__log.debug('Non-integer index. Taking its floor')
      i = round(i)
    return int(i) 
  # -----------------------------------------------------------------------------  
  def index2metre(self, i, origin, axis, **kwargs):
    # origin = self.extent[axis][0]
    # m = i * self.dx[axis] + origin
    # return m
    raise NotImplementedError()
  # -----------------------------------------------------------------------------  
  def metre2node(self, *args, **kwargs):
    # not tested
    return self.index2node(self.metre2index(*args, **kwargs))
  # -----------------------------------------------------------------------------
  def node2metre(self, node, axis, **kwargs):
    # not tested
    return self.index2metre(self.node2index(node), axis, **kwargs)      
  # -----------------------------------------------------------------------------
  def box2inds(self, box, **kwargs):
    """
    Convert box into slicing-indices using extent.
    Not tested.
    """
    box = np.array(box)
    extent = np.array(self.extent)
    assert len(box.shape) == 1
    assert len(box) == len(extent.flatten())
    box = box.reshape(extent.shape)
    inds = np.zeros(box.shape)
    for axis, _ in enumerate(box):
      b0, b1 = box[axis]
      if b0 == b1: # FOR 2D (DOUBLE-CHECK)
        # self.__log.warn('Skipping b0=b1=%s' % b0)
        continue
      inds[axis][0] = self._metre2index(b0, axis)
      inds[axis][1] = self._metre2index(b1, axis) + 1 # NOTE: FOR np.arange(b1, b2) etc.
      # self.__log.debug('axis %s: i1=%s, i2=%s' % (axis, inds[axis][0], inds[axis][1]))    
    return inds.astype(int)
  # -----------------------------------------------------------------------------
