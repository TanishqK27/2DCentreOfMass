# README for ShapePlotter

## Overview

The `ShapePlotter` class is designed for interactive plotting and manipulation of 2D shapes in a matplotlib plot. Users can create shapes by specifying vertices and then select a vertex to "pin" the shape, simulating how it would hang if suspended from that point. The class calculates the center of mass for the shape, rotates the shape to align the center of mass directly below the pinning point, and provides visual feedback throughout the process.
Note that this is only for simple polygons. 

## How to Use

1. **Initialization**: Instantiate a `ShapePlotter` object by specifying the input mode (`'click'` or `'manual'`) and the axis size as a tuple (width, height).

2. **Shape Creation**: Depending on the input mode, create the shape by clicking on the plot or entering coordinates manually.

3. **Pinning Point Selection**: After the shape is created, select a vertex to act as the pinning point. The shape will rotate so that its center of mass aligns vertically below this point.

4. **Visualization**: The plot displays the shape, its center of mass, and the pinning point, updating in real time as the shape is manipulated.

## Functions and Their Roles

### `__init__(self, input_mode, axis_size)`
Initializes the `ShapePlotter` instance. Sets up the plot and connects event handlers if the input mode is `'click'`.

- `input_mode`: Determines how the user inputs the shape (`'click'` or `'manual'`).
- `axis_size`: Defines the size of the plotting area.

### `add_vertex(self, point)`
Adds a vertex to the shape and updates the plot.

- Prints the coordinates of the added point.
- Closes the shape if the added point completes it.

### `close_shape(self)`
Closes the shape by connecting the last and first vertices and calculates the center of mass.

- Invokes the center of mass calculation.
- Displays the center of mass on the plot.

### `update_polygon(self)`
Updates the plot with the current vertices of the shape.

- Redraws the shape with any new vertices added.

### `calculate_center_of_mass(self)`
Calculates and displays the center of mass for the shape using the polygon's vertex coordinates.

- Utilizes the formula for the centroid of a polygon based on its vertices.
- Prints and plots the center of mass.

### `select_pinning_point(self, point)`
Selects the closest vertex to a given point as the pinning point and initiates rotation.

- Determines the closest vertex to the user-selected point.
- Prints the coordinates of the chosen pinning point.

### `rotate_shape(self)`
Rotates the shape so that the center of mass is vertically aligned below the pinning point.

- Calculates the necessary rotation angle.
- Applies the rotation to all vertices and the center of mass.
- Updates the plot with the rotated shape.

### `rotate_point(self, point, angle, origin)`
Rotates a point around a given origin by a specified angle.

- Used to rotate each vertex and the center of mass during the shape rotation.

## Mathematical Concepts

- **Center of Mass**: Calculated using the formula for the centroid of a polygon, which involves the coordinates of the vertices.
- **Rotation**: Achieved by applying a rotation matrix to each vertex and the center of mass, ensuring the shape rotates as a rigid body.
- **Pinning Point Selection**: Involves determining the closest vertex to a user-selected point, which becomes the point of suspension.

## Usage Example

```python
plotter = ShapePlotter(input_mode='click', axis_size=(10, 10))
plotter.show()