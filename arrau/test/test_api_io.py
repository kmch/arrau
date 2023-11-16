import numpy as np
from unittest import TestCase
from arrau.io import extent2str, shape2str

class TestFunctions(TestCase):
  def test_extent2str(self):
    assert extent2str([[-1,-2],[3,4],[5,6]]) == 'x-1_-2_y3_4_z5_6'
    assert extent2str([[-1,-2],[3,4]]) == 'x-1_-2_y3_4'
    assert extent2str([[-1,-2]]) == 'x-1_-2'
  def test_shape2str(self):
    assert shape2str((1,2,3)) == 'shape1x2x3'
    assert shape2str((1,2)) == 'shape1x2'
    assert shape2str((1,)) == 'shape1'