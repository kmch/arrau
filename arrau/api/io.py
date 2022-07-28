"""
I/O API.

Handling input/output efficiently
and conveniently.
"""
from abc import ABC, abstractmethod
from autologging import logged, traced
import numpy as np

def extent2str(extent):
  """
  Convert `extent` to string which 
  can be used e.g. to create a descriptive
  name for a file storing an array.

  Paramaters
  ----------
  extent : list / array
      List of the form:
        [[x1,x2], [y1,y2], ...]
      Should work in 1-3d.
  """
  if len(extent) == 3:
    [[x1, x2], [y1, y2], [z1, z2]] = extent 
    x1, x2, y1, y2, z1, z2 = [int(i) for i in [x1, x2, y1, y2, z1, z2]]
    s = 'x{x1}_{x2}_y{y1}_{y2}_z{z1}_{z2}'.format(x1=x1,x2=x2,y1=y1,y2=y2,z1=z1,z2=z2)
  elif len(extent) == 2:
    [[x1, x2], [y1, y2]] = extent 
    x1, x2, y1, y2 = [int(i) for i in [x1, x2, y1, y2]]
    s = 'x{x1}_{x2}_y{y1}_{y2}'.format(x1=x1,x2=x2,y1=y1,y2=y2)
  elif len(extent) == 1:
    [[x1, x2]] = extent 
    x1, x2 = [int(i) for i in [x1, x2]]
    s = 'x{x1}_{x2}'.format(x1=x1,x2=x2)    
  return s
def shape2str(shape):
  """
  See `extent2str`, now it converts 
  `shape` instead of `extent`.
  """
  if len(shape) == 3:
    s = '%sx%sx%s' % shape
  elif len(shape) == 2:
    s = '%sx%s' % shape
  elif len(shape) == 1:
    s = '%s' % shape
  s = 'shape%s' % s
  return s  
@logged
class File(ABC):
  def __init__(self, name, path, **kwargs):
    if path[-1] != '/':
      path += '/'
    self.name = name
    self.path = path
    self.fname = path + name
class FileReader(ABC):
  def read_any(fname, overwrite_mmp=False, **kwargs):
    """
    Read file of any format, possibly as a 
    memory-mapped file if both the file is 
    present on disk and the shape of the array 
    is provided. FILE MUST CONTAIN AN ARRAY.
    
    shape : tuple
      Shape of the array stored in fname.
      (this is necessary to read .mmp).
    
    """
    from .memmap import read_mmp, save_mmp
    
    if overwrite_mmp:
      read_any._log.info('Set overwrite_mmp=False for faster i/o!')
    else:
      read_any._log.info('If the array looks corrupted try overwrite_mmp=True.')

    shape = kw('shape', None, kwargs)
    
    fname_mmp = strip(fname) + '.mmp'
    
    if not exists(fname_mmp) or overwrite_mmp:
      read_any._log.debug(fname_mmp+' does not exist. Reading ' + 
                        fname + ' instead...')
      A = read_any_format(fname, **kwargs)
      read_any._log.info('Saving ' + fname_mmp + '...')
      save_mmp(A, fname_mmp)

    elif shape is None:
      read_any._log.debug('File ' + fname_mmp + ' exists, but you' +
                        ' need to provide its shape to read it. Reading ' + 
                        fname + ' instead...')
      A = read_any_format(fname, **kwargs) 
      
    else:
      read_any._log.debug(fname_mmp+' exists and its shape is provided: ' +
                        str(shape))
      A = read_mmp(fname_mmp, **kwargs)    
    
    return A
def read_any_format(fname, **kwargs):
  """
  Read an array from a file of
  any format.
  
  """
  from fullwavepy.ioapi.fw3d import read_vtr, read_ttr
  from fullwavepy.ioapi.segy import read_sgy
  from fullwavepy.ioapi.memmap import read_mmp
  
  read_any_format._log.debug('Reading ' + fname + '...')
  ext = exten(fname, **kwargs)
  
  ext = ext.lower() # convert to lower case

  if ext == 'vtr':
    A = read_vtr(fname, **kwargs)
  elif ext == 'ttr':
    A = read_ttr(fname, **kwargs)    
  elif ext == 'sgy' or ext == 'segy':
    A = read_sgy(fname, **kwargs)
  elif ext == 'mmp':
    A = read_mmp(fname, **kwargs)
  elif ext == 'txt':
    c = read_txt(fname, **kwargs)
    A = np.zeros((1,1,len(c)))
    A[0,0,:] = [float(i[0]) for i in c]    
  else:
    raise ValueError('Unknown extension: ' + ext)
  
  return A    

