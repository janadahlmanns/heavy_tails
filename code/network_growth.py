from manim import *
import numpy as np
import csv

class NetworkGrowth(MovingCameraScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.network_data = []
        self.dots = []  # Keep track of all dots added
    
    def load_network_data(self):
        """Load network data from CSV file"""
        with open('network_data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.network_data.append(row)
    
    def add_node(self, node_index):
        """Create, add to scene, and return a dot for the given node index"""
        node_data = self.network_data[node_index]
        x_orig = float(node_data['x'])
        y_orig = float(node_data['y'])
        
        # Normalize from original range [-5, 5] for x and [-3, 3] for y to [0, 2]
        x_normalized = ((x_orig + 5) / 10) * 2  # [-5, 5] -> [0, 1] -> [0, 2]
        y_normalized = ((y_orig + 3) / 6) * 2   # [-3, 3] -> [0, 1] -> [0, 2]
        
        # Scale to Manim coordinates [0.25, 8.25] for x and [0.5, 8.5] for y
        x_manim = 0.25 + x_normalized * 4
        y_manim = 0.5 + y_normalized * 4
        
        # Create white-outlined circle with black fill
        dot = Circle(radius=0.1, stroke_color=WHITE, stroke_width=1.5, fill_color=BLACK, fill_opacity=1)
        dot.move_to([x_manim, y_manim, 0])
        
        # Retrieve and draw connections to target nodes
        connections = []
        for i in range(20):  # Max 20 targets per node
            target_x_key = f'target_{i}_x'
            target_y_key = f'target_{i}_y'
            
            if target_x_key not in node_data:
                break  # No more targets
            
            target_x_str = node_data[target_x_key]
            target_y_str = node_data[target_y_key]
            
            # Skip empty or None values
            if not target_x_str or target_x_str == 'None':
                break
            
            try:
                target_x_orig = float(target_x_str)
                target_y_orig = float(target_y_str)
                
                # Normalize target coordinates
                target_x_normalized = ((target_x_orig + 5) / 10) * 2
                target_y_normalized = ((target_y_orig + 3) / 6) * 2
                
                # Scale to Manim coordinates
                target_x_manim = 0.25 + target_x_normalized * 4
                target_y_manim = 0.5 + target_y_normalized * 4
                
                # Create line from current node to target
                line = Line(start=np.array([x_manim, y_manim, 0]),
                           end=np.array([target_x_manim, target_y_manim, 0]),
                           stroke_color=WHITE, stroke_width=1)
                connections.append(line)
            except (ValueError, KeyError):
                break
        
        # Fade in the dot first
        self.play(FadeIn(dot, run_time=15/15))
        
        # Store dot and bring to front
        self.dots.append(dot)
        self.bring_to_front(dot)
        
        # Draw connection lines growing from the new node simultaneously
        if connections:
            # Set z-index before animating
            for conn in connections:
                conn.set_z_index(-1)
            create_animations = [Create(conn, run_time=15/15) for conn in connections]
            self.play(*create_animations)
        
        return dot
    
    def construct(self):
        # --- CAMERA SETTINGS ---
        # 16:9 landscape aspect ratio
        self.camera.frame.set_width(16)
        self.camera.frame.set_height(9)
        self.camera.frame.move_to([8, 4.5, 0])
        self.camera.background_color = "#000000"
        
        # --- COORDINATE SYSTEM ---
        origin = np.array([1, 1, 0])
        
        # X-axis
        x_axis = Line(start=np.array([0.25, 0.5, 0]), end=np.array([8.25, 0.5, 0]), stroke_color=WHITE, stroke_width=2)
        
        # Y-axis
        y_axis = Line(start=np.array([0.25, 0.5, 0]), end=np.array([0.25, 8.5, 0]), stroke_color=WHITE, stroke_width=2)
        
        # X-axis ticks and labels (0 to 2)
        x_positions = np.linspace(0.25, 8.25, 5)  # 5 ticks for 0, 0.5, 1.0, 1.5, 2.0
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
            tick = Line(start=np.array([0.25, pos, 0]), end=np.array([0.05, pos, 0]), stroke_color=WHITE, stroke_width=1.5)
            y_ticks.append(tick)
            
            label = Text(f"{val}", font_size=28, color=WHITE, font="sans-serif")
            label.move_to([-0.45, pos, 0])
            y_labels.append(label)
        
        # Add coordinate system on top
        self.add(x_axis, y_axis)
        self.add(*x_ticks, *x_labels)
        self.add(*y_ticks, *y_labels)
        

        # --- LOAD NETWORK DATA ---
        self.load_network_data()
        
      
        # --- HISTOGRAM COORDINATE SYSTEM (Right Pane) ---
        # X-axis (width)
        hist_x_axis = Line(start=np.array([10.25, 0.5, 0]), end=np.array([15.25, 0.5, 0]), stroke_color=WHITE, stroke_width=2)
        
        # Y-axis (height - degree range 0 to 25)
        hist_y_axis = Line(start=np.array([10.25, 0.5, 0]), end=np.array([10.25, 8.5, 0]), stroke_color=WHITE, stroke_width=2)
        
        # Y-axis ticks and labels (0 to 25 degrees)
        hist_y_positions = np.linspace(0.5, 8.5, 6)  # 6 ticks for 0, 5, 10, 15, 20, 25
        hist_y_values_labels = [0, 5, 10, 15, 20, 25]
        
        hist_y_ticks = []
        hist_y_labels = []
        
        for pos, val in zip(hist_y_positions, hist_y_values_labels):
            tick = Line(start=np.array([10.25, pos, 0]), end=np.array([10.05, pos, 0]), stroke_color=WHITE, stroke_width=1.5)
            hist_y_ticks.append(tick)
            
            label = Text(f"{val}", font_size=28, color=WHITE, font="sans-serif")
            label.move_to([9.55, pos, 0])
            hist_y_labels.append(label)
        
        # X-axis ticks and labels (for degree values 0-25)
        hist_x_positions = np.linspace(10.25, 15.25, 6)  # 6 ticks
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

        # --- PLOT NETWORK NODES ---
        #for node_index in range(60):
        for node_index in range(10):
            self.add_node(node_index)

        self.wait(2)
