"""
I/O API.

Handling input/output efficiently
and conveniently.
"""
from abc import ABC, abstractmethod
from autologging import logged, traced
import numpy as np


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

