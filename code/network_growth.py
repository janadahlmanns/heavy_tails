from manim import *
import numpy as np
import csv

class NetworkGrowth(MovingCameraScene):
    def construct(self):
        # --- CAMERA SETTINGS ---
        # 16:9 landscape aspect ratio
        self.camera.frame.set_width(16)
        self.camera.frame.set_height(9)
        self.camera.frame.move_to([8, 4.5, 0])
        self.camera.background_color = "#cc1515"
        
        # Create horizontal white lines at various y values with width 2
        y_values = [0, 2, 4, 6, 8]
        lines = []
        labels = []
        
        for y in y_values:
            line = Line(start=np.array([0, y, 0]), end=np.array([16, y, 0]), stroke_color=WHITE, stroke_width=2)
            lines.append(line)
            
            # Create label at middle of line, slightly above
            label = Text(f"y={y}", font_size=24, color=WHITE)
            label.move_to([8, y + 0.4, 0])
            labels.append(label)
        
        # Create vertical white lines at various x values with width 2
        x_values = [0, 2, 4, 6, 8, 10, 12, 14, 16]
        
        for x in x_values:
            line = Line(start=np.array([x, 0, 0]), end=np.array([x, 8, 0]), stroke_color=WHITE, stroke_width=2)
            lines.append(line)
            
            # Create label at 1/3 the length, slightly to the right
            label = Text(f"x={x}", font_size=24, color=WHITE)
            label.move_to([x + 0.4, 10/3, 0])
            labels.append(label)
        
        # Display all lines and labels
        self.add(*lines, *labels)
        

        # --- COORDINATE SYSTEM ---
        origin = np.array([1, 1, 0])
        
        # X-axis
        x_axis = Line(start=np.array([1, 0.5, 0]), end=np.array([9, 0.5, 0]), stroke_color=WHITE, stroke_width=2)
        
        # Y-axis
        y_axis = Line(start=np.array([1, 0.5, 0]), end=np.array([1, 8.5, 0]), stroke_color=WHITE, stroke_width=2)
        
        # X-axis ticks and labels (0 to 2)
        x_positions = np.linspace(1, 9, 5)  # 5 ticks for 0, 0.5, 1.0, 1.5, 2.0
        x_values_labels = [0, 0.5, 1.0, 1.5, 2.0]
        
        x_ticks = []
        x_labels = []
        
        for pos, val in zip(x_positions, x_values_labels):
            tick = Line(start=np.array([pos, 0.5, 0]), end=np.array([pos, 0.3, 0]), stroke_color=WHITE, stroke_width=1.5)
            x_ticks.append(tick)
            
            label = Text(f"{val}", font_size=28, color=WHITE, font="sans-serif")
            label.move_to([pos, 0.05, 0])
            x_labels.append(label)
        
        # Y-axis ticks and labels (0 to 2)
        y_positions = np.linspace(0.5, 8.5, 5)  # 5 ticks for 0, 0.5, 1.0, 1.5, 2.0
        y_values_labels = [0, 0.5, 1.0, 1.5, 2.0]
        
        y_ticks = []
        y_labels = []
        
        for pos, val in zip(y_positions, y_values_labels):
            tick = Line(start=np.array([1, pos, 0]), end=np.array([0.8, pos, 0]), stroke_color=WHITE, stroke_width=1.5)
            y_ticks.append(tick)
            
            label = Text(f"{val}", font_size=28, color=WHITE, font="sans-serif")
            label.move_to([0.3, pos, 0])
            y_labels.append(label)
        
        # Add coordinate system on top
        self.add(x_axis, y_axis)
        self.add(*x_ticks, *x_labels)
        self.add(*y_ticks, *y_labels)
        
        # Add border lines
        right_line = Line(start=np.array([9, 0.5, 0]), end=np.array([9, 8.5, 0]), stroke_color=WHITE, stroke_width=4)
        top_line = Line(start=np.array([1, 8.5, 0]), end=np.array([9, 8.5, 0]), stroke_color=WHITE, stroke_width=4)
        self.add(right_line, top_line)
        
        # --- LOAD NETWORK DATA ---
        network_data = []
        with open('network_data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                network_data.append(row)
        
        # --- PLOT NETWORK NODES ---
        # Create circles for all nodes
        dots = []
        for node_data in network_data:
            x_orig = float(node_data['x'])
            y_orig = float(node_data['y'])
            
            # Normalize from original range [-5, 5] for x and [-3, 3] for y to [0, 2]
            x_normalized = ((x_orig + 5) / 10) * 2  # [-5, 5] -> [0, 1] -> [0, 2]
            y_normalized = ((y_orig + 3) / 6) * 2   # [-3, 3] -> [0, 1] -> [0, 2]
            
            # Scale to Manim coordinates [1, 9] for x and [0.5, 8.5] for y
            x_manim = 1 + x_normalized * 4
            y_manim = 0.5 + y_normalized * 4
            
            # Create white filled circle
            dot = Circle(radius=0.05, color=WHITE, fill_color=WHITE, fill_opacity=1)
            dot.move_to([x_manim, y_manim, 0])
            dots.append(dot)
        
        # Add all dots to scene
        self.add(*dots)
        
        # --- HISTOGRAM COORDINATE SYSTEM (Right Pane) ---
        # X-axis (width)
        hist_x_axis = Line(start=np.array([10, 0.5, 0]), end=np.array([15, 0.5, 0]), stroke_color=WHITE, stroke_width=2)
        
        # Y-axis (height - degree range 0 to 25)
        hist_y_axis = Line(start=np.array([10, 0.5, 0]), end=np.array([10, 8.5, 0]), stroke_color=WHITE, stroke_width=2)
        
        # Y-axis ticks and labels (0 to 25 degrees)
        hist_y_positions = np.linspace(0.5, 8.5, 6)  # 6 ticks for 0, 5, 10, 15, 20, 25
        hist_y_values_labels = [0, 5, 10, 15, 20, 25]
        
        hist_y_ticks = []
        hist_y_labels = []
        
        for pos, val in zip(hist_y_positions, hist_y_values_labels):
            tick = Line(start=np.array([10, pos, 0]), end=np.array([9.8, pos, 0]), stroke_color=WHITE, stroke_width=1.5)
            hist_y_ticks.append(tick)
            
            label = Text(f"{val}", font_size=28, color=WHITE, font="sans-serif")
            label.move_to([9.3, pos, 0])
            hist_y_labels.append(label)
        
        # X-axis ticks and labels (for degree values 0-25)
        hist_x_positions = np.linspace(10, 15, 6)  # 6 ticks
        hist_x_values_labels = [0, 5, 10, 15, 20, 25]  # Degree values
        
        hist_x_ticks = []
        hist_x_labels = []
        
        for pos, val in zip(hist_x_positions, hist_x_values_labels):
            tick = Line(start=np.array([pos, 0.5, 0]), end=np.array([pos, 0.3, 0]), stroke_color=WHITE, stroke_width=1.5)
            hist_x_ticks.append(tick)
            
            label = Text(f"{val}", font_size=28, color=WHITE, font="sans-serif")
            label.move_to([pos, 0.05, 0])
            hist_x_labels.append(label)
        
        # Add histogram coordinate system
        self.add(hist_x_axis, hist_y_axis)
        self.add(*hist_y_ticks, *hist_y_labels)
        self.add(*hist_x_ticks, *hist_x_labels)
        self.wait(2)
