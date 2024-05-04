
import matplotlib
matplotlib.use('Qt5Agg')
import logging
import matplotlib.pyplot as plt
import numpy as np

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Geometry:
    """
    Handles geometric calculations for shapes.
    """

    @staticmethod
    def calculate_center_of_mass(vertices):
        """
        Calculate the center of mass and area of a polygon given its vertices.

        Arguments required:
        vertices (list of tuples): List of (x, y) coordinates for the vertices of the polygon.

        Returns:
        tuple: ((C_x, C_y), Area) where (C_x, C_y) are coordinates of the center of mass, and Area is the area of the polygon.
        """
        vertices_loop = vertices + [vertices[0]]  # Close the loop for calculation
        A = 0.5 * sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(vertices_loop[:-1], vertices_loop[1:]))
        C_x = (1 / (6 * A)) * sum(
            (x0 + x1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(vertices_loop[:-1], vertices_loop[1:]))
        C_y = (1 / (6 * A)) * sum(
            (y0 + y1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(vertices_loop[:-1], vertices_loop[1:]))
        return (C_x, C_y), abs(A)

    @staticmethod
    def rotate_point(point, angle, origin):
        """
        Rotate a point around a given origin by an angle.

        Arguments:
        point (tuple): The point to rotate (x, y).
        angle (float): The angle in radians to rotate.
        origin (tuple): The origin point to rotate around (x, y).

        Returns:
        tuple: The rotated point (x, y).
        """
        ox, oy = origin
        px, py = point
        qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
        qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
        return qx, qy


class Shape:
    """
    Manages the vertices of the shape and performs calculations using Geometry.
    """

    def __init__(self):
        self.vertices = []
        self.center_of_mass = None
        self.area = None

    def add_vertex(self, vertex):
        """
        Add a vertex to the shape.

        Args:
        vertex (tuple): The vertex to add (x, y).
        """
        self.vertices.append(vertex)

    def close_shape(self):
        """
        Close the shape by calculating its center of mass and area.
        """
        self.center_of_mass, self.area = Geometry.calculate_center_of_mass(self.vertices)

    def rotate_shape(self, pin_point):
        """
        Rotate the shape around a specified pin point so the center of mass is directly underneath it.

        Args:
        pin_point (tuple): The pin point around which to rotate (x, y).

        Returns:
        float: The angle of rotation in degrees.
        """
        dx, dy = self.center_of_mass[0] - pin_point[0], self.center_of_mass[1] - pin_point[1]
        phi = np.arctan2(-dx, -dy)
        self.vertices = [Geometry.rotate_point(v, phi, pin_point) for v in self.vertices]
        self.center_of_mass = Geometry.rotate_point(self.center_of_mass, phi, pin_point)
        return np.degrees(phi)


class ShapePlotter:
    """
    Manages user interaction and plotting of the Shape using Matplotlib.
    """

    def __init__(self, input_mode, axis_size):
        """
        Initialize the ShapePlotter with a given input mode and plot dimensions.

        Args:
        input_mode (str): 'click' for mouse input or 'manual' for console input.
        axis_size (tuple): The dimensions of the plotting area (width, height).
        """
        self.shape = Shape()
        self.fig, self.ax = plt.subplots()
        self.axis_size = axis_size
        self.ax.set_xlim(0, axis_size[0])
        self.ax.set_ylim(0, axis_size[1])
        self.input_mode = input_mode
        self.setup_input_mode()

    def setup_input_mode(self):
        """
        Setup event handlers for mouse interaction based on the input mode.
        """
        if self.input_mode == 'click':
            self.fig.canvas.mpl_connect('button_press_event', self.on_click)
            self.fig.canvas.mpl_connect('button_release_event', self.on_release)
            logging.info("Click to add vertices. Right-click to close shape, left-click to select pinning point.")

    def on_click(self, event):
        """
        Handle click events for adding vertices and selecting pinning points.
        """
        if event.button == 1 and not self.shape.center_of_mass:
            self.shape.add_vertex((event.xdata, event.ydata))
            self.update_polygon()

    def on_release(self, event):
        """
        Handle release events for closing shapes and initiating rotations.
        """
        if event.button == 3 and not self.shape.center_of_mass:
            self.shape.close_shape()
            self.update_polygon(closed=True)
            logging.info(f"Shape closed. Center of mass at {self.shape.center_of_mass}, Area: {self.shape.area}")
        elif event.button == 1 and self.shape.center_of_mass:
            degrees = self.shape.rotate_shape((event.xdata, event.ydata))
            self.update_polygon(closed=True)
            logging.info(
                f"Shape rotated by {degrees:.2f} degrees to align the center of mass directly below the pinning point.")

    def update_polygon(self, closed=False):
        """
        Redraw the polygon to reflect any changes in vertices or rotation.
        """
        self.ax.clear()
        vertices = self.shape.vertices
        self.ax.add_patch(plt.Polygon(vertices, closed=closed, fill=False, edgecolor='r'))
        self.ax.plot(*zip(*vertices), marker='o', color='r')
        if self.shape.center_of_mass:
            self.ax.plot(*self.shape.center_of_mass, marker='o', color='b', label='Center of Mass')
        self.ax.set_xlim(0, self.axis_size[0])
        self.ax.set_ylim(0, self.axis_size[1])
        plt.draw()

    def show(self):
        """
        Display the plot window.
        """
        plt.show()


if __name__ == "__main__":
    input_mode = input("Choose input mode ('click' or 'manual'): ")
    axis_size = list(map(float, input("Enter axis size as 'x,y': ").split(',')))
    plotter = ShapePlotter(input_mode, axis_size)
    if input_mode == 'manual':
        logging.info("Enter vertices as 'x,y'. Type 'done' to close the shape and proceed.")
        while True:
            vertex_input = input("Enter vertex or 'done': ")
            if vertex_input.lower() == 'done':
                if len(plotter.shape.vertices) > 2:
                    plotter.shape.close_shape()
                    plotter.update_polygon(closed=True)
                    logging.info("Shape closed. Select a pinning point by clicking on the plot.")
                    break
                else:
                    logging.warning("A minimum of three vertices is required to form a shape.")
            else:
                try:
                    vertex = tuple(map(float, vertex_input.split(',')))
                    plotter.shape.add_vertex(vertex)
                except ValueError:
                    logging.error("Invalid input. Please enter coordinates as 'x,y'.")

    plotter.show()