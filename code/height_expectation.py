from manim import *
import numpy as np

def cm_to_imperial(cm):
    """Convert cm to feet and inches"""
    inches = cm / 2.54
    feet = int(inches // 12)
    remaining_inches = int(round(inches % 12))
    return f"{feet}'{remaining_inches}\""

class HeightExpectation(MovingCameraScene):
    def construct(self):
        # --- CAMERA SETTINGS ---
        self.camera.frame.set_width(14)
        self.camera.frame.move_to([6, 6, 0])
        self.camera.background_color = "#1a1a1a"
        
        # Create horizontal white lines at various y values with width 2
        y_values = [0, 2, 4, 6, 8, 10, 12]
        lines = []
        
        for y in y_values:
            line = Line(start=np.array([0, y, 0]), end=np.array([12, y, 0]), stroke_color=WHITE, stroke_width=2)
            lines.append(line)
        
        # Create vertical white lines at various x values with width 2
        x_values = [0, 2, 4, 6, 8, 10, 12]
        
        for x in x_values:
            line = Line(start=np.array([x, 0, 0]), end=np.array([x, 12, 0]), stroke_color=WHITE, stroke_width=2)
            lines.append(line)
        
        # Display all lines instantly
        self.add(*lines)
        
        # --- COORDINATE SYSTEM (on top) ---
        origin = np.array([1, 1, 0])
        
        # X-axis
        x_axis = Line(start=origin, end=np.array([12, 1, 0]), stroke_color=WHITE, stroke_width=2)
        
        # Y-axis
        y_axis = Line(start=origin, end=np.array([1, 8, 0]), stroke_color=WHITE, stroke_width=2)
        
        # X-axis ticks and labels (145-200cm)
        x_cm_values = [145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200]
        x_positions = np.linspace(1, 12, len(x_cm_values))
        
        x_ticks = []
        x_labels = []
        
        for pos, cm_val in zip(x_positions, x_cm_values):
            tick = Line(start=np.array([pos, 1, 0]), end=np.array([pos, 0.85, 0]), stroke_color=WHITE, stroke_width=1.5)
            x_ticks.append(tick)
            
            metric_label = Text(f"{cm_val}", font_size=36, color=WHITE, font="sans-serif")
            metric_label.move_to([pos, 0.3, 0])
            x_labels.append(metric_label)
            
            imperial = cm_to_imperial(cm_val)
            imperial_label = Text(imperial, font_size=34, color="#AFCBCF", font="sans-serif")
            imperial_label.move_to([pos, -0.15, 0])
            x_labels.append(imperial_label)
        
        x_title = Text("height", font_size=40, color=WHITE, font="sans-serif")
        x_title.move_to([6.5, -0.3, 0])
        
        # Y-axis ticks and labels (0-10)
        y_values = list(range(0, 11))
        y_positions = np.linspace(1, 8, len(y_values))
        
        y_ticks = []
        y_labels = []
        
        for pos, y_val in zip(y_positions, y_values):
            tick = Line(start=np.array([1, pos, 0]), end=np.array([0.85, pos, 0]), stroke_color=WHITE, stroke_width=1.5)
            y_ticks.append(tick)
            
            label = Text(f"{y_val}", font_size=36, color=WHITE, font="sans-serif")
            label.move_to([0.55, pos, 0])
            y_labels.append(label)
        
        y_title = Text("number of people", font_size=40, color=WHITE, font="sans-serif")
        y_title.rotate(PI / 2)
        y_title.move_to([-0.5, 4.5, 0])
        
        # Add coordinate system on top
        self.add(x_axis, y_axis)
        self.add(*x_ticks, *x_labels, x_title)
        self.add(*y_ticks, *y_labels, y_title)
        
        self.wait(2)
        self.add(*x_ticks, *x_labels, x_title)
        self.add(*y_ticks, *y_labels, y_title)

