"""
Array modifiers
"""
import numpy as np
from autologging import logged

@logged
def modify_array(A, *args, **kwargs):
  """
  Modify each trace (last dimension) 
  of a 1D/2D/3D array using a list 
  of functions.
  
  Parameters
  ----------
  A : array 
   1D/2D/3D array.
   
  **kwargs : keyword arguments (optional)
    Current capabilities:
    modifiers : list
      List of functions to apply subsequently 
      on each trace. The order is following:
      [func1, func2, ...] 
      first func1 will be applied and 
      followed by func2, etc. 
      Note that it is different from
      the composite function's notation:
      ...(func2(func1(trace))  
      Modifiers are set up in a separate function 
      for cleanliness.
      Modifiers are allowed to have *args and **kwargs
      so lambda functions are not recommended as 
      modifiers.
  
  Returns
  -------
  Modified A.

  Notes
  -----
  Always modify trace-wise where trace 
  is the last dimension of the array.
  
  """
  array_modifiers = _set_array_modifiers(**kwargs)
  tracewise_modifiers = _set_tracewise_modifiers(**kwargs)

  A = np.array(A)

  for func in array_modifiers:
    A = func(A, *args, **kwargs)

  for func in tracewise_modifiers:
    A = np.apply_along_axis(func, -1, A, *args, **kwargs)
  
  return A
@logged
def _set_array_modifiers(**kwargs):
  """
  Notes
  -----
  norm_bulk acts on the whole array,
  and norm acts trace-wise, but they both
  call the same function. FIXME: common interface
  """
  #from ..dsp.su import su_process
  from fullwavepy.numeric.generic import norm_bulk_max
  modifiers = kwargs.get('array_modifiers', [])  
  
  clip = kwargs.get('clip', None)
  clip_min = kwargs.get('clip_min', None)  
  clip_max = kwargs.get('clip_max', None)
  norm_bulk = kwargs.get('norm_bulk', None)  
  func = kwargs.get('func', None)

  # bulk-normalization (must be BEFORE clipping)
  if norm_bulk is not None:
    modifiers.append(norm_bulk_max) 

  if clip is not None or clip_min is not None or clip_max is not None:
    modifiers.append(clip_array)
    
  #if func is not None:
    #modifiers.append(su_process)
  
  return modifiers
@logged
def _set_tracewise_modifiers(**kwargs):
  """
  Set a list of functions to modify 
  a trace / an array of traces.
  
  Parameters
  ----------
  **kwargs : keyword arguments (optional)
    Current capabilities:
    modifiers : list
      List of functions to apply subsequently 
      on each trace. The order is following:
      [func1, func2, ...] 
      first func1 will be applied and so on.
      Note that order of the elements is 
      opposite to the composite function's 
      notation:
      ...(func2(func1(trace))
  
  Returns
  -------
  modifiers : list 
    List of modifiers.
  
  Notes
  -----
  The order matters, they don't commute in general.
  
  We could use lambda functions, but we want to 
  pass **kwargs to modifiers, and it is bad to 
  define lambda functions with *args, **kwargs.
  
  Clipping is done before normalization.
  
  """
  from fullwavepy.numeric.generic import normalize
  from fullwavepy.numeric.operators import derivative
  from fullwavepy.numeric.fourier import dft
  
  modifiers = kwargs.get('tracewise_modifiers', [])
  norm = kwargs.get('norm', None)
  spect = kwargs.get('spect', None)
  deriv = kwargs.get('deriv', None)
  
  # DERIVATIVE 
  if deriv is not None:
    modifiers.append(derivative)   
  
  # DISCRETE FOURIER TRANSFORM
  if spect is not None:
    modifiers.append(dft)
  
  # NORMALIZATION
  if norm is not None:
    modifiers.append(normalize)
  
  return modifiers
@logged
def clip_array(A, clip=None, clip_min=None, clip_max=None):
  """
  clip : float 
    Convenience to define both bounds 
    at once as [-clip, clip]
  """
  if clip is not None:
    clip_min = -clip
    clip_max = clip

  return np.clip(A, clip_min, clip_max)
@logged
def interlace_arrays(A1, A2, chunk_size=10):
  """ 
  Create an array composed of interlaced 
  chunks of A1 and A2. Each chunk counts `chunk_size` 
  traces. First chunk is composed of A1 traces.
  
  Parameters
  ----------
  A1, A2 : 2d arrays
  chunk_size : int 
      No. of columns of 1st array
      followed by the same no. of
      columns of the 2nd array. 
    
  Returns
  -------
  Z : array
    2D array.
  
  """
  assert len(A1.shape) == 2
  if A1.shape != A2.shape:
    raise ValueError('Arrays must have same shapes.')
  
  A = np.array(A1)
  ncols = A.shape[0]
  
  if ncols < 2 * chunk_size:
    interlace_arrays._log.warning('No. of columns=' + str(ncols) + 
           ' < 2 * chunk_size! Outputting empty array')
    return []
  
  nchunks = ncols // chunk_size // 2
  for i, Ai in enumerate([A1, A2]):
    i_start = i * chunk_size
    for j in range(nchunks):
      i1 = i_start + j * 2 * chunk_size
      i2 = i_start + j * 2 * chunk_size + (chunk_size) # IT USED TO BE WRONG (-1)
      A[i1 : i2] = Ai[i1 : i2]

  return np.array(A)


# alternative
class ArrModifier:
  """
  Mix-in with array-processing methods.
  Should work for any no. of dimensions.
  """
  def clip(self, clip=None, clip_min=None, clip_max=None):
    """
    clip : float 
      Convenience to define both bounds 
      at once as [-clip, clip]
    """
    if clip is not None:
      clip_min = -clip
      clip_max = clip

    return np.clip(self.arr, clip_min, clip_max)  
  def modify(self, *args, **kwargs):
    """
    Modify each trace (last dimension) 
    of a 1D/2D/3D array using a list 
    of functions.
    
    Parameters
    ----------
    A : array 
    1D/2D/3D array.
    
    **kwargs : keyword arguments (optional)
      Current capabilities:
      modifiers : list
        List of functions to apply subsequently 
        on each trace. The order is following:
        [func1, func2, ...] 
        first func1 will be applied and 
        followed by func2, etc. 
        Note that it is different from
        the composite function's notation:
        ...(func2(func1(trace))  
        Modifiers are set up in a separate function 
        for cleanliness.
        Modifiers are allowed to have *args and **kwargs
        so lambda functions are not recommended as 
        modifiers.
    
    Returns
    -------
    Modified A.

    Notes
    -----
    Always modify trace-wise where trace 
    is the last dimension of the array.
    
    """
    array_modifiers = _set_array_modifiers(**kwargs)
    tracewise_modifiers = _set_tracewise_modifiers(**kwargs)

    A = np.array(self.arr)

    for func in array_modifiers:
      A = func(A, *args, **kwargs)

    for func in tracewise_modifiers:
      A = np.apply_along_axis(func, -1, A, *args, **kwargs)
    
    return A
  def _set_array_modifiers(**kwargs):
    """
    Notes
    -----
    norm_bulk acts on the whole array,
    and norm acts trace-wise, but they both
    call the same function. FIXME: common interface
    """
    
    modifiers = kwargs.get('array_modifiers', [])  
    
    clip = kwargs.get('clip', None)
    clip_min = kwargs.get('clip_min', None)  
    clip_max = kwargs.get('clip_max', None)
    norm_bulk = kwargs.get('norm_bulk', None)  
    func = kwargs.get('func', None)

    # bulk-normalization (must be BEFORE clipping)
    if norm_bulk is not None:
      modifiers.append(norm_bulk_max) 

    if clip is not None or clip_min is not None or clip_max is not None:
      modifiers.append(self.clip)
      
    #if func is not None:
      #modifiers.append(su_process)
    
    return modifiers
  def _set_tracewise_modifiers(**kwargs):
    """
    Set a list of functions to modify 
    a trace / an array of traces.
    
    Parameters
    ----------
    **kwargs : keyword arguments (optional)
      Current capabilities:
      modifiers : list
        List of functions to apply subsequently 
        on each trace. The order is following:
        [func1, func2, ...] 
        first func1 will be applied and so on.
        Note that order of the elements is 
        opposite to the composite function's 
        notation:
        ...(func2(func1(trace))
    
    Returns
    -------
    modifiers : list 
      List of modifiers.
    
    Notes
    -----
    The order matters, they don't commute in general.
    
    We could use lambda functions, but we want to 
    pass **kwargs to modifiers, and it is bad to 
    define lambda functions with *args, **kwargs.
    
    Clipping is done before normalization.
    
    """
    from fullwavepy.numeric.generic import normalize
    from fullwavepy.numeric.operators import derivative
    from fullwavepy.numeric.fourier import dft
    
    modifiers = kwargs.get('tracewise_modifiers', [])
    norm = kwargs.get('norm', None)
    spect = kwargs.get('spect', None)
    deriv = kwargs.get('deriv', None)
    
    # DERIVATIVE 
    if deriv is not None:
      modifiers.append(derivative)   
    
    # DISCRETE FOURIER TRANSFORM
    if spect is not None:
      modifiers.append(dft)
    
    # NORMALIZATION
    if norm is not None:
      modifiers.append(normalize)
    
    return modifiers
