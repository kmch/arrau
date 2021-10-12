import numpy as np
from unittest import TestCase, skip
from arrau.a1d import Arr1d

class TestArr1d(TestCase):
  def test_extent_custom(self):
    a = Arr1d(np.zeros(5), extent=[[-1,1]])
    assert np.all(a.axes[0].extent == [-1,1])  
  def test_extent_default(self):
    a = Arr1d(np.zeros(5))
    assert np.all(a.axes[0].extent == [0,4])
  def test_init_axes(self):
    a = Arr1d(np.zeros(5))
    assert len(a.axes) == 1
    assert a.axes[0].param == 'x'
    assert a.axes[0].unit == 'm' 
  @skip
  def test_info(self):
    a = Arr1d(np.zeros(5))
    a.info()
