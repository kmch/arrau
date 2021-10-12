import numpy as np
from unittest import TestCase
from arrau.generic import ArrAxis, CoordTransform

class TestArrAxis(TestCase):
  def test_dx(self):
    ax = ArrAxis('x', shape=10)
    assert ax.dx == 1
    ax = ArrAxis('x', shape=11, extent=[0,1])
    assert ax.dx == 0.1
  def test_extent_custom(self):
    ax = ArrAxis('x', shape=11, extent=[0,1])
    assert np.all(ax.extent == [0,1])
  def test_extent_default(self):
    ax = ArrAxis('x', shape=10)
    assert np.all(ax.extent == [0,9])
class TestCoordTransform(TestCase):
  def test_metre2index(self):
    origin = 0
    dx = 50
    i = CoordTransform().metre2index(24, origin, dx)
    assert i == 0
    i = CoordTransform().metre2index(26, origin, dx)
    assert i == 1
