from manim import *
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

def cm_to_imperial(cm):
    """Convert cm to feet and inches"""
    inches = cm / 2.54
    feet = int(inches // 12)
    remaining_inches = int(round(inches % 12))
    return f"{feet}'{remaining_inches}\""

def height_to_x(h):
    """Map height (110-230cm) to x-position (1-12)"""
    return 1 + (h - 110) / (230 - 110) * (12 - 1)

def create_distribution_curve(heights):
    """
    Create a smoothed histogram curve from heights data.
    Returns a VMobject curve.
    """
    if len(heights) == 0:
        # Return empty line if no data
        return Line(start=np.array([1, 1, 0]), end=np.array([12, 1, 0]), stroke_color=WHITE, stroke_width=2)
    
    # Create histogram with 2cm bins (across full 110-230cm range)
    bins = np.arange(110, 232, 2)
    hist_counts, bin_edges = np.histogram(heights, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Create smooth interpolation of histogram
    if len(bin_centers) > 1:
        smooth_func = interp1d(bin_centers, hist_counts, kind='cubic', fill_value='extrapolate')
        
        # Sample smooth function across full range
        x_range = np.linspace(110, 230, 300)
        smooth_counts = np.clip(smooth_func(x_range), 0, None)  # Ensure non-negative
    else:
        smooth_counts = np.zeros(300)
        x_range = np.linspace(110, 230, 300)
    
    # Convert to world coordinates (map counts to y-axis 2-9 range, representing 0-20 people)
    curve_points = []
    for h, count in zip(x_range, smooth_counts):
        x_pos = height_to_x(h)
        y_pos = 2 + (count / 20) * (8 - 1)  # Scale count (0-20) to y-position (2-9)
        curve_points.append([x_pos, y_pos, 0])
    
    # Create curve
    curve = VMobject(stroke_color="#E79E16", stroke_width=6)
    curve.set_points_as_corners(np.array(curve_points))
    
    return curve

class HeightExpectation(MovingCameraScene):
    def drop_dot(self, idx, duration, hold_duration=0):
        """
        Drop a single dot with specified duration.
        Updates distribution curve after the dot drops.
        
        Args:
            idx: Index in heights array
            duration: Time for this dot to drop
            hold_duration: Time to hold dot at top before dropping (default 0)
        """
        fade_duration = duration * 0.2  # 20% of dot time
        dot_duration = duration - fade_duration
        
        height = self.heights[idx]
        x_pos = height_to_x(height)
        
        # Create dot
        dot = Circle(radius=0.15, color=WHITE, fill_opacity=1)
        dot.move_to([x_pos, 10, 0])
        
        # Create metric label
        metric_label = Text(f"{int(height)}cm", font_size=36, color=WHITE, font="sans-serif")
        metric_label.move_to([x_pos + 1, 10.7, 0])
        
        # Create imperial label
        imperial = cm_to_imperial(height)
        imperial_label = Text(imperial, font_size=34, color=WHITE, font="sans-serif")
        imperial_label.move_to([x_pos + 1, 9.9, 0])
        
        # Add and animate dot dropping
        self.add(dot, metric_label, imperial_label)
        
        # Hold dot at top if hold_duration > 0
        if hold_duration > 0:
            self.wait(hold_duration)
        
        self.play(
            dot.animate.move_to([x_pos, 2, 0]),
            metric_label.animate.move_to([x_pos + 1, 2.5, 0]).set_opacity(0),
            imperial_label.animate.move_to([x_pos + 1, 2.1, 0]).set_opacity(0),
            run_time=dot_duration
        )
        
        # Update distribution curve (only if we have at least 2 points)
        heights_so_far = self.heights[:idx + 1]
        if len(heights_so_far) >= 2:
            new_curve = create_distribution_curve(heights_so_far)
            
            # Fade old curve to new curve
            if hasattr(self, 'current_curve') and self.current_curve is not None:
                self.play(
                    FadeOut(self.current_curve),
                    FadeIn(new_curve),
                    run_time=fade_duration
                )
                self.remove(self.current_curve)
            else:
                self.play(FadeIn(new_curve), run_time=fade_duration)
            
            self.add(new_curve)
            self.current_curve = new_curve
    
    def construct(self):
        # --- CAMERA SETTINGS ---
        self.camera.frame.set_width(14)
        self.camera.frame.move_to([6, 6, 0])
        self.camera.background_color = "#1a1a1a"
        
        # --- COORDINATE SYSTEM (on top) ---
        origin = np.array([1, 2, 0])
        
        # X-axis
        x_axis = Line(start=origin, end=np.array([12, 2, 0]), stroke_color=WHITE, stroke_width=2)
        
        # Y-axis
        y_axis = Line(start=origin, end=np.array([1, 9, 0]), stroke_color=WHITE, stroke_width=2)
        
        # X-axis ticks and labels (110-230cm)
        x_cm_values = [110, 130, 150, 170, 190, 210, 230]
        x_positions = np.linspace(1, 12, len(x_cm_values))
        
        x_ticks = []
        x_labels = []
        
        for pos, cm_val in zip(x_positions, x_cm_values):
            tick = Line(start=np.array([pos, 2, 0]), end=np.array([pos, 1.85, 0]), stroke_color=WHITE, stroke_width=1.5)
            x_ticks.append(tick)
            
            metric_label = Text(f"{cm_val}cm", font_size=36, color=WHITE, font="sans-serif")
            metric_label.move_to([pos, 1.3, 0])
            x_labels.append(metric_label)
            
            imperial = cm_to_imperial(cm_val)
            imperial_label = Text(imperial, font_size=34, color=WHITE, font="sans-serif")
            imperial_label.move_to([pos, 0.85, 0])
            x_labels.append(imperial_label)
        
        x_title = Text("height", font_size=40, color=WHITE, font="sans-serif")
        x_title.move_to([6.5, -0.3, 0])
        
        # Y-axis ticks and labels (0-20)
        y_values = list(range(0, 21, 2))
        y_positions = np.linspace(2, 9, len(y_values))
        
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
        y_title.move_to([-0.5, 5.5, 0])
        
        # Add coordinate system on top
        self.add(x_axis, y_axis)
        self.add(*x_ticks, *x_labels, x_title)
        self.add(*y_ticks, *y_labels, y_title)
        
        self.wait(1)
        
        # --- LOAD HEIGHT DATA ---
        df = pd.read_csv('height_synthetic.csv')
        self.heights = df['Height'].values
        self.current_curve = None
        
        # --- DROP DOTS WITH EXPLICIT TIMING ---
        # First 3 dots at 2s each with 0.5s hold
        for idx in range(0, 3):
            self.drop_dot(idx, 2, hold_duration=0.5)
        
        # Accelerating group (3-7) with gradually decreasing duration from 2s to 0.2s, no hold
        durations = np.linspace(1, 0.075, 4)
        for i, duration in enumerate(durations):
            self.drop_dot(3 + i, duration, hold_duration=0)
        
        # Fast dots from 7 to 73 (stops before 146cm outlier at index 74)
        for idx in range(7, 74):
            self.drop_dot(idx, 0.075, hold_duration=0)
        
        self.wait(1)


