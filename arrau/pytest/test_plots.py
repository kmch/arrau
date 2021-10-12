"""
Unit tests of plotting functions 
using pytest's mpl plugin.

Notes
-----
pytest can run virtually all unittest-tests out of the box.

It can be slow.
"""
import matplotlib.pyplot as plt
import pytest
from unittest import TestCase
# from ndar.a3d import Arr3d

# funtion to test
def foo(a, b):
  return a + b

# pytest-style test
def test_foo():
  assert foo(2,2) == 4

# unittest-style test (Python standard-library) understood by pytest
class Test(TestCase):
  def test_foo(self):
    assert foo(2,2) == 4

# pytest-mpl test comparing similarity of figures

# It needs an X server running. 
# (it works with Xming as of 4 Oct 2021)

# First run as:
# >>> pytest test_plots.py --mpl-generate-path=baseline
# to save good figures in ./baseline directory

# Then, after codebase modifications, run as:
# >>> pytest test_plots.py --mpl
# It should take a few sec to complete.
  @pytest.mark.mpl_image_compare
  def test_succeeds():
      fig = plt.figure()
      ax = fig.add_subplot(1,1,1)
      ax.plot([1,2,3])
      return fig

# class TestPlottingArrSlices(TestCase):
#   # @pytest.mark.mpl_image_compare
#   def test_plot(self):
#     fname = '../notebooks/downloaded/p14-StartVp_shape341x361x81.mmp'
#     a = np.memmap(fname, dtype=np.float32, shape=(341,361,81))
#     a = Arr3d(a, extent=[[8e3,25e3],[-3e3,15e3],[0,4e3]])
#     a.slice(13.25e3, axis=0, unit='m')
#     a.slice(8.75e3, axis=1, unit='m')
#     a.slice(2e3, axis=2, unit='m')
#     fig = plt.figure(figsize=(15,6))
#     a.slices.list[-1].plot(mode='shade', cmap='magma')
#     a.slices.list[-1].plot(mode='contour', xlabel='x, m', ylabel='y, m')
#     a.slices.list[-1].plot_slice_lines()
#     return fig
