# 2DCentreOfMass README

2DCentreOfMass is an interactive tool designed for visualizing and manipulating geometric shapes based on user input. It calculates properties such as the center of mass and area, and allows for rotation based on a specified pinning point.

## Tutorial

### Getting Started

To begin using 2DCentreOfMass, ensure that you have Python installed, along with the necessary libraries: `matplotlib` and `numpy`.

1. **Launch the program**: Run ShapePlotter from your command line:

    ```bash
    python CentreOfMass.py
    ```

2. **Input mode selection**: Choose between 'click' or 'manual' input modes.
   - **Click mode**: Use your mouse to click on the plot area to define the vertices of your shape. Right-click to close the shape and left-click to select the pinning point.
   - **Manual mode**: Enter coordinates of vertices directly through the console. Type 'done' to close the shape.

### Creating a Shape

- **Add vertices**: Depending on the chosen input mode, add vertices by clicking on the plot area or entering coordinates in the format `x,y`.
- **Close the shape**: Right-click on the plot or type 'done' to finish the shape definition.
- **Select a pinning point**: Click on a vertex to set it as the pinning point for rotation.

## How To

### Setting Up the Environment

1. **Install Python**: Download and install Python from [python.org](https://www.python.org/).
2. **Install required libraries**: Use pip to install Matplotlib and NumPy.

    ```bash
    pip install matplotlib numpy
    ```

### Running the Library

Navigate to the directory containing `shapeplotter.py` and run:

```bash
python CentreOfMass.py
```
## Examples

### Creating a Triangle

- Use either **Click Mode** or **Manual Mode** in order to create a triangle.
- Click around any vertex to choose a **pinning point**. 
- You will see the shape rotate as it would under gravity. 

### Creating a Rectangle

- Follow similar steps as for the triangle, but with four points.

### Functions and Their Parameters

- `add_vertex(vertex)`: Adds a vertex to the current shape. `vertex` should be a tuple `(x, y)`.
- `close_shape()`: Closes the shape by connecting the last vertex to the first and calculates geometric properties.
- `calculate_center_of_mass()`: Calculates the center of mass for the defined shape.
- `select_pinning_point(point)`: Selects a pinning point for rotation. `point` is a tuple `(x, y)`.
- `rotate_shape()`: Rotates the shape around the selected pinning point to align the center of mass beneath it.
- `rotate_point(point, angle, origin)`: Rotates a point around the given origin by the specified angle.

## Explanation

### Underlying Mathematics and Algorithms

- **Center of Mass**: The center of mass is computed using the formula for polygons, which involves summing over the vertices and dividing by the total area.
- **Area Calculation**: The area of the polygon is calculated using the shoelace formula (Gauss's area formula), which is efficient for computing the area of a polygon given its vertices.
- **Rotation**: Rotation is handled through transformation matrices that rotate points around a given pin by a calculated angle based on the position of the center of mass relative to the pinning point.

The algorithms are designed to handle general polygons and perform calculations in real-time to update the visualizations dynamically.

If you would like to read more about the underlying mathematics, look at the paper written, in the directory as 
```bash
main.pdf
```