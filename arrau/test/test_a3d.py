import numpy as np
from unittest import TestCase
from arrau.a3d import Arr3d

class TestArr3d(TestCase):
  """
  Even though Arr is abstract, we 
  can test some of its functions.

  """
  def test_extent_custom(self):
    a = Arr3d(np.zeros((2,2,2)), extent=[[0,1],[0,2],[0,3]])
    assert np.all(a.axes[2].extent == [0,3])    
  def test_extract(self):
    a = Arr3d(np.zeros((4,4,4)), extent=[[1,4],[1,4],[1,4]])
    a = a.extract([[1,4],[1,2],[1,2]])
    assert isinstance(a, Arr3d)
    assert np.all(a.shape == (4,2,2))
  def test_slice_index(self):
    a = Arr3d(np.array([[[0, 1],[2, 3]],[[4, 5],[6, 7]]]))
    assert np.all(a.slice(value=0, unit='i', axis=0).arr == [[0, 1],[2, 3]])
  def test_slice_metre(self):
    a = Arr3d(np.array([[[0, 1],[2, 3]],[[4, 5],[6, 7]]]), \
      extent=[[0,100],[0,100],[0,100]])
    assert np.all(a.slice(value=80, unit='m', axis=0).arr == [[4, 5],[6, 7]])
  def test_slice_extent(self):
    a = Arr3d(np.array([[[0, 1],[2, 3]],[[4, 5],[6, 7]]]), extent=[[0,1],[0,2],[0,3]])
    assert np.all(a.slice(0, axis=0).axes[0].extent == [0,2])
    assert np.all(a.slice(0, axis=0).axes[1].extent == [0,3])
    assert np.all(a.slice(0, axis=2).axes[0].extent == [0,1])
