import pytest
from CentreOfMass import Geometry, Shape, ShapePlotter
import numpy as np

# Testing Geometry calculations
def test_calculate_center_of_mass():
    vertices = [(0, 0), (4, 0), (4, 4), (0, 4)]
    com, area = Geometry.calculate_center_of_mass(vertices)
    assert com == (2.0, 2.0)
    assert area == 16.0

def test_rotate_point():
    origin = (1, 1)
    point = (2, 2)
    angle = np.pi / 2  # 90 degrees
    rotated_point = Geometry.rotate_point(point, angle, origin)
    np.testing.assert_almost_equal(rotated_point, (0, 2))

# Testing Shape functionalities
def test_add_vertex():
    shape = Shape()
    shape.add_vertex((1, 2))
    assert shape.vertices == [(1, 2)]

def test_close_shape():
    shape = Shape()
    shape.add_vertex((0, 0))
    shape.add_vertex((4, 0))
    shape.add_vertex((4, 4))
    shape.add_vertex((0, 4))
    shape.close_shape()
    assert shape.center_of_mass == (2.0, 2.0)
    assert shape.area == 16.0

def test_rotate_shape():
    shape = Shape()
    shape.add_vertex((0, 0))
    shape.add_vertex((4, 0))
    shape.add_vertex((4, 4))
    shape.add_vertex((0, 4))
    shape.close_shape()
    pin_point = (2, 2)  # Center of the shape
    degrees = shape.rotate_shape(pin_point)
    # Acceptable results could be 0 or -180 degrees since both represent the shape's alignment with itself
    assert degrees in [0, -180.0], "Rotation should result in no visual change."

# Optionally, test the plotting behavior
# Note: Testing matplotlib plots can be challenging and may require
#       integration testing rather than unit testing.

# Run tests
if __name__ == "__main__":
    pytest.main()