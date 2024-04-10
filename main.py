
import matplotlib

matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import sympy as sp



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
        if input_mode == 'click':
            self.fig.canvas.mpl_connect('button_press_event', self.on_click)
            self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def on_click(self, event):
        if not self.shape_drawn and event.button == 1:
            self.add_vertex((event.xdata, event.ydata))

    def on_release(self, event):
        if not self.shape_drawn and event.button == 3:  # Close shape with right-click
            self.close_shape()
        elif self.shape_drawn and not self.pinning_point_selected and event.button == 1:  # Select pinning point with left-click
            self.select_pinning_point((event.xdata, event.ydata))
            self.pinning_point_selected = True

    def add_vertex(self, point):
        self.vertices.append(point)
        print(f"Point added: ({point[0]:.2f}, {point[1]:.2f})")  # Print the added point with two decimal places
        if len(self.vertices) > 1:
            self.update_polygon()
        if len(self.vertices) > 2 and self.vertices[-1] == self.vertices[0]:
            self.close_shape()

    def close_shape(self):
        self.shape_drawn = True
        self.update_polygon(closed=True)
        self.calculate_center_of_mass()

    def update_polygon(self, closed=False):
        self.ax.clear()
        self.ax.add_patch(plt.Polygon(self.vertices, fill=False, closed=closed))
        self.ax.plot(*zip(*self.vertices), marker='o', color='r')
        self.ax.set_xlim(0, self.axis_size[0])
        self.ax.set_ylim(0, self.axis_size[1])
        plt.draw()

    def calculate_center_of_mass(self):
        vertices = self.vertices + [self.vertices[0]]  # Close the loop
        A = 0.5 * sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(vertices[:-1], vertices[1:]))
        C_x = (1 / (6 * A)) * sum((x0 + x1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(vertices[:-1], vertices[1:]))
        C_y = (1 / (6 * A)) * sum((y0 + y1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(vertices[:-1], vertices[1:]))
        self.center_of_mass = (C_x, C_y)
        print(f"Center of Mass: ({C_x:.2f}, {C_y:.2f})")  # Print the center of mass coordinates with two decimal places
        print(f"Total Area of the Shape: {abs(A):.2f}")  # Print the total area of the shape with two decimal places
        self.ax.plot(C_x, C_y, 'bo')  # Plot center of mass
        plt.draw()

    def select_pinning_point(self, point):
        closest_vertex = min(self.vertices[:-1], key=lambda v: np.linalg.norm(np.array(v) - np.array(point)))
        self.pin_point = closest_vertex
        print(f"Pinning point selected: ({self.pin_point[0]:.2f}, {self.pin_point[1]:.2f})")  # Print the pinning point with two decimal places
        self.rotate_shape()

    def rotate_shape(self):
        # Calculate the angle for rotation.
        dx = self.center_of_mass[0] - self.pin_point[0]
        dy = self.center_of_mass[1] - self.pin_point[1]
        angle_to_vertical = np.arctan2(dy, dx)
        angle_of_rotation = np.pi / 2 - angle_to_vertical

        # Apply rotation to vertices and center of mass to align vertically.
        rotated_vertices = [self.rotate_point(vertex, angle_of_rotation, self.pin_point) for vertex in self.vertices]
        rotated_center_of_mass = self.rotate_point(self.center_of_mass, angle_of_rotation, self.pin_point)

        # Perform an additional 180-degree rotation to move the center of mass below the pinning point.
        final_vertices = [self.rotate_point(vertex, np.pi, self.pin_point) for vertex in rotated_vertices]
        final_center_of_mass = self.rotate_point(rotated_center_of_mass, np.pi, self.pin_point)

        # Update the plot with the final rotated shape and new center of mass position
        self.ax.clear()
        self.ax.add_patch(plt.Polygon(final_vertices, fill=False, closed=True))
        self.ax.plot(*zip(*final_vertices), marker='o', color='r')
        self.ax.plot(*self.pin_point, 'go')  # Pinning point
        self.ax.plot(*final_center_of_mass, 'bo')  # Center of mass after rotation
        self.ax.set_xlim(0, self.axis_size[0])
        self.ax.set_ylim(0, self.axis_size[1])
        plt.draw()

        # Update the center of mass to the new final position
        self.center_of_mass = final_center_of_mass

        # Update the center of mass to the new rotated position
        self.center_of_mass = rotated_center_of_mass

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
        while True:
            vertex_input = input("Enter vertex as 'x,y' or type 'done' when finished: ")
            if vertex_input.lower() == 'done':
                if len(plotter.vertices) > 2:
                    plotter.close_shape()
                break
            else:
                try:
                    vertex = tuple(map(float, vertex_input.split(',')))
                    plotter.add_vertex(vertex)
                    if len(plotter.vertices) > 1:
                        plotter.update_polygon()
                except ValueError:
                    print("Invalid input. Please enter coordinates as 'x,y'.")

    plotter.show()