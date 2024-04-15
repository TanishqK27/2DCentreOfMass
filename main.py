
import matplotlib

matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sympy as sp


import matplotlib.pyplot as plt
import numpy as np

class ShapePlotter:
    def __init__(self, input_mode, axis_size):
        self.fig, self.ax = plt.subplots()
        self.axis_size = axis_size
        self.ax.set_xlim(0, axis_size[0])
        self.ax.set_ylim(0, axis_size[1])
        self.vertices = []
        self.shape_drawn = False
        self.center_of_mass = None
        self.pinning_point_selected = False
        self.pin_point = None
        self.input_mode = input_mode
        self.setup_input_mode()

    def setup_input_mode(self):
        if self.input_mode == 'click':
            self.fig.canvas.mpl_connect('button_press_event', self.on_click)
            self.fig.canvas.mpl_connect('button_release_event', self.on_release)
            print("Click on the plot to add vertices. Right-click to close the shape and left-click to select a pinning point.")

    def on_click(self, event):
        if not self.shape_drawn and event.button == 1:
            self.add_vertex((event.xdata, event.ydata))

    def on_release(self, event):
        if not self.shape_drawn and event.button == 3:
            self.close_shape()
        elif self.shape_drawn and not self.pinning_point_selected and event.button == 1:
            self.select_pinning_point((event.xdata, event.ydata))
            self.pinning_point_selected = True
            self.rotate_shape()

    def add_vertex(self, point):
        if None not in point:
            self.vertices.append(point)
            print(f"Vertex added: ({point[0]:.2f}, {point[1]:.2f})")
            self.update_polygon()

    def close_shape(self):
        if len(self.vertices) > 2:
            self.shape_drawn = True
            self.update_polygon(closed=True)
            self.calculate_center_of_mass()
            print("Shape closed. Select a pinning point by clicking on the plot.")

    def update_polygon(self, closed=False):
        self.ax.clear()
        self.ax.add_patch(plt.Polygon(self.vertices, fill=False, closed=closed))
        self.ax.plot(*zip(*self.vertices), marker='o', color='r')
        self.ax.set_xlim(0, self.axis_size[0])
        self.ax.set_ylim(0, self.axis_size[1])
        plt.draw()

    def calculate_center_of_mass(self):
        vertices = self.vertices + [self.vertices[0]]
        A = 0.5 * sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(vertices[:-1], vertices[1:]))
        C_x = (1 / (6 * A)) * sum((x0 + x1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(vertices[:-1], vertices[1:]))
        C_y = (1 / (6 * A)) * sum((y0 + y1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(vertices[:-1], vertices[1:]))
        self.center_of_mass = (C_x, C_y)
        print(f"Center of Mass: ({C_x:.2f}, {C_y:.2f}) located. Total area: {abs(A):.2f}")

    def select_pinning_point(self, point):
        closest_vertex = min(self.vertices[:-1], key=lambda v: np.linalg.norm(np.array(v) - np.array(point)))
        self.pin_point = closest_vertex
        print(f"Pinning point selected at: ({self.pin_point[0]:.2f}, {self.pin_point[1]:.2f}). Calculating rotation...")

    def rotate_shape(self):
        if self.center_of_mass and self.pin_point:
            dx = self.center_of_mass[0] - self.pin_point[0]
            dy = self.center_of_mass[1] - self.pin_point[1]
            phi = np.arctan2(-dx, -dy)
            degrees = np.degrees(phi)
            rotated_vertices = [self.rotate_point(vertex, phi, self.pin_point) for vertex in self.vertices]
            rotated_center_of_mass = self.rotate_point(self.center_of_mass, phi, self.pin_point)

            self.ax.clear()
            self.ax.add_patch(plt.Polygon(rotated_vertices, fill=False, closed=True))
            self.ax.plot(*zip(*rotated_vertices), marker='o', color='r')
            self.ax.plot(rotated_center_of_mass[0], rotated_center_of_mass[1], 'bo')
            self.ax.plot(self.pin_point[0], self.pin_point[1], 'go')
            self.ax.set_xlim(0, self.axis_size[0])
            self.ax.set_ylim(0, self.axis_size[1])
            plt.draw()

            print(f"Shape rotated by {degrees:.2f} degrees to align the center of mass directly below the pinning point.")

    def rotate_point(self, point, angle, origin):
        ox, oy = origin
        px, py = point
        qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
        qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
        return (qx, qy)

    def show(self):
        plt.show()

if __name__ == "__main__":
    input_mode = input("Choose input mode ('click' or 'manual'): ")
    axis_size = list(map(float, input("Enter axis size as 'x,y': ").split(',')))

    plotter = ShapePlotter(input_mode, axis_size)

    if input_mode == 'manual':
        print("Enter vertices as 'x,y'. Type 'done' to close the shape and proceed.")
        while True:
            vertex_input = input("Enter vertex or 'done': ")
            if vertex_input.lower() == 'done':
                if len(plotter.vertices) > 2:
                    plotter.close_shape()
                else:
                    print("A minimum of three vertices is required to form a shape.")
                break
            else:
                try:
                    vertex = tuple(map(float, vertex_input.split(',')))
                    plotter.add_vertex(vertex)
                except ValueError:
                    print("Invalid input. Please enter coordinates as 'x,y'.")

    plotter.show()