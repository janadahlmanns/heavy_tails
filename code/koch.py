from manim import *
import numpy as np

class Koch(Scene):
    def construct(self):
        side_length = 10
        max_depth = 5
        linewidth = 3

        snowflakes = []
        colored_snowflakes = []
        for depth in range(max_depth + 1):
            triangle = self.initial_triangle(side_length)
            points = self.koch_recursive(triangle, depth)
            shape = VMobject(stroke_color="#AFCBCF", stroke_width=linewidth)
            colored_shape = VMobject(stroke_color="#E79E16", stroke_width=linewidth)
            shape.set_points_as_corners(points + [points[0]])
            colored_shape.set_points_as_corners(points + [points[0]])
            snowflakes.append(shape)
            colored_snowflakes.append(colored_shape)


        # Start with colored trianlge
        current = colored_snowflakes[0]
        self.play(Create(current))
        self.wait(0.5)

        for i in range(len(snowflakes)):
            white = snowflakes[i]
            # Fade from colored (A) to white (B)
            self.play(FadeOut(current), FadeIn(white))
            current = white
            self.wait(0.5)

            # A: Overlay current white with next colored
            if i + 1 < len(snowflakes):
                colored = colored_snowflakes[i + 1]
                overlaid = VGroup(colored, current.copy())
                self.play(Transform(current, overlaid))
                self.wait(0.2)

        self.wait(2)


    def initial_triangle(self, side_length):
        height = side_length * np.sqrt(3) / 2
        p1 = np.array([-side_length / 2, -height / 3, 0])
        p2 = np.array([ side_length / 2, -height / 3, 0])
        p3 = np.array([0, 2 * height / 3, 0])
        return [p1, p2, p3]

    def koch_recursive(self, points, depth):
        if depth == 0:
            return points
        new_points = []
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            new_points += self.add_bump(p1, p2)
        return self.koch_recursive(new_points, depth - 1)

    def add_bump(self, p1, p2):
        v = p2 - p1
        a = p1 + v / 3
        b = p1 + 2 * v / 3
        m = (a + b) / 2

        dir = b - a
        dir /= np.linalg.norm(dir)
        normal = -np.array([-dir[1], dir[0], 0])

        s = np.linalg.norm(b - a)
        height = s * np.sqrt(3) / 2
        peak = m + normal * height

        return [p1, a, peak, b]
