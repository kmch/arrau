import numpy as np
from unittest import TestCase, skip
from arrau.a2d import Arr2d, Arr2dSlice

class TestArr2d(TestCase):
  def test_extract(self):
    a = Arr2d(np.zeros((4,4)), extent=[[1,4],[1,4]])
    a = a.extract([[1,4],[1,2]])
    assert isinstance(a, Arr2d) 
    assert np.all(a.shape == (4,2)) 
  def test_plot(self):
    a = Arr2d(np.array([[0,1],[2,3]]))
    a.plot()
  def test_slice_axes(self):
    a = Arr2d(np.array([[0,1],[2,3]]))
    assert len(a.slice(value=0, unit='i', axis=0).axes) == 1
  def test_slice_extent(self):
    a = Arr2d(np.array([[0,1],[2,3]]), extent=[[0,100],[0,200]])
    assert np.all(a.slice(0, axis=0).axes[0].extent == np.array([[0,200]]))
    assert np.all(a.slice(1, axis=1).axes[0].extent == np.array([[0,100]])) 
  def test_slice_index(self):
    a = Arr2d(np.array([[0,1],[2,3]]))
    assert np.all(a.slice(value=0, unit='i', axis=0).arr == [0,1])
  def test_slice_metre(self):
    a = Arr2d(np.array([[0,1],[2,3]]), extent=[[0,100],[0,100]])
    assert np.all(a.slice(value=80, unit='m', axis=0).arr == [2,3])
  def test_slices_add(self):
    a = Arr2d(np.zeros((2,2)))
    a.slice(0, axis=0)
    assert len(a.slices.list) == 1
    assert isinstance(a.slices.list[0], Arr2dSlice)
