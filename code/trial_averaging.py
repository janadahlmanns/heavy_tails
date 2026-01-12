from manim import *
import numpy as np

def wobbly_curve(x, shift=10):
    """
    Generate a smooth wobbly curve with two Gaussian peaks.
    Peak 1: height ~1.5 at x=2
    Peak 2: height ~2.0 at x=5
    Wobbles around baseline with ±0.2 amplitude
    """
    # Gaussian peaks
    peak1 = np.exp(-((x - 2) ** 2) / 0.3) * 1.5
    peak2 = np.exp(-((x - 5) ** 2) / 0.4) * 2.0
    
    # Natural wobble (noise)
    np.random.seed(42)  # For reproducibility
    wobble = np.sin(x * 1.5) * 0.15 + np.cos(x * 0.8) * 0.1
    
    return peak1 + peak2 + wobble + shift
def wobbly_curve2(x, shift=7):
    """
    Generate a smooth wobbly curve with two Gaussian peaks.
    Peak 1: height 1.7 at x=5
    Peak 2: height 1.4 at x=9
    Wobbles around baseline with different pattern
    """
    # Gaussian peaks
    peak1 = np.exp(-((x - 5) ** 2) / 0.35) * 1.7
    peak2 = np.exp(-((x - 9) ** 2) / 0.45) * 1.4
    
    # Different natural wobble pattern
    np.random.seed(123)  # Different seed for different pattern
    wobble = np.sin(x * 1.2) * 0.12 + np.cos(x * 0.9) * 0.13
    
    return peak1 + peak2 + wobble + shift

def wobbly_curve3(x, shift=4):
    """
    Generate a smooth wobbly curve with three Gaussian peaks.
    Peak 1: height 1.3 at x=1
    Peak 2: height 1.9 at x=5
    Peak 3: height 1.2 at x=7
    Wobbles around baseline with yet another pattern
    """
    # Gaussian peaks
    peak1 = np.exp(-((x - 1) ** 2) / 0.4) * 1.3
    peak2 = np.exp(-((x - 5) ** 2) / 0.3) * 1.9
    peak3 = np.exp(-((x - 7) ** 2) / 0.35) * 1.2
    
    # Different natural wobble pattern
    np.random.seed(456)  # Different seed for different pattern
    wobble = np.sin(x * 1.3) * 0.14 + np.cos(x * 0.7) * 0.11
    
    return peak1 + peak2 + peak3 + wobble + shift
class TrialAveraging(MovingCameraScene):
    def construct(self):
        # --- CAMERA SETTINGS ---
        self.camera.frame.set_width(14)
        self.camera.frame.move_to([6, 6, 0])
        self.camera.background_color = "#1a1a1a"
        
        # Create horizontal white lines at various y values with width 2
        y_values = [0, 2, 4, 6, 8, 10, 12]
        lines = []
        labels = []
        
        for y in y_values:
            line = Line(start=np.array([0, y, 0]), end=np.array([12, y, 0]), stroke_color="#666666", stroke_width=2)
            lines.append(line)
            
            # Create label at middle of line, slightly above
            label = Text(f"y={y}", font_size=24, color=WHITE)
            label.move_to([5, y + 0.4, 0])
            labels.append(label)
        
        # Create vertical white lines at various x values with width 2
        x_values = [0, 2, 4, 6, 8, 10, 12]
        
        for x in x_values:
            line = Line(start=np.array([x, 0, 0]), end=np.array([x, 12, 0]), stroke_color="#666666", stroke_width=2)
            lines.append(line)
            
            # Create label at 1/3 the length, slightly to the right
            label = Text(f"x={x}", font_size=24, color=WHITE)
            label.move_to([x + 0.4, 10/3, 0])
            labels.append(label)
        
        # Display all lines and labels
        for line in lines:
            self.add(line)
        for label in labels:
            self.add(label)
        
        # --- DRAW CURVE ---
        # Sample the wobbly curve function
        x_samples = np.linspace(0, 12, 300)
        y_samples = np.array([wobbly_curve(x) for x in x_samples])
        
        # Create curve points
        curve_points = np.array([[x, y, 0] for x, y in zip(x_samples, y_samples)])
        
        # Create and display the curve
        curve = VMobject(stroke_color=WHITE, stroke_width=4)
        curve.set_points_as_corners(curve_points)
        
        self.add(curve)
        
        # --- DRAW SECOND CURVE ---
        # Sample the second wobbly curve function
        y_samples2 = np.array([wobbly_curve2(x) for x in x_samples])
        
        # Create curve points
        curve_points2 = np.array([[x, y, 0] for x, y in zip(x_samples, y_samples2)])
        
        # Create and display the second curve
        curve2 = VMobject(stroke_color=WHITE, stroke_width=4)
        curve2.set_points_as_corners(curve_points2)
        
        self.add(curve2)
        
        # --- DRAW THIRD CURVE ---
        # Sample the third wobbly curve function
        y_samples3 = np.array([wobbly_curve3(x) for x in x_samples])
        
        # Create curve points
        curve_points3 = np.array([[x, y, 0] for x, y in zip(x_samples, y_samples3)])
        
        # Create and display the third curve
        curve3 = VMobject(stroke_color=WHITE, stroke_width=4)
        curve3.set_points_as_corners(curve_points3)
        
        self.add(curve3)
        
        # First 2 seconds: all three shifted curves are visible and static
        self.wait(2)
        
        # Second 2 seconds: all three curves slide down to shift=0
        # Each curve moves different distances but all take 2 seconds
        self.play(
            curve.animate.shift(DOWN * 10),
            curve2.animate.shift(DOWN * 7),
            curve3.animate.shift(DOWN * 4),
            run_time=2
        )
        
        # Third 2 seconds: keep all three curves static at shift=0
        self.wait(2)
        
        # --- DRAW UNSHIFTED VERSIONS OF THE THREE CURVES ---
        # Unshifted curve 1 (wobbles around y=0) - REMOVED
        
        # Unshifted curve 2 (wobbles around y=0)
        y_samples_unshifted2 = np.array([wobbly_curve2(x, shift=0) for x in x_samples])
        curve_points_unshifted2 = np.array([[x, y, 0] for x, y in zip(x_samples, y_samples_unshifted2)])
        curve_unshifted2 = VMobject(stroke_color=WHITE, stroke_width=4)
        curve_unshifted2.set_points_as_corners(curve_points_unshifted2)
        self.add(curve_unshifted2)
        
        # Unshifted curve 3 (wobbles around y=0)
        y_samples_unshifted3 = np.array([wobbly_curve3(x, shift=0) for x in x_samples])
        curve_points_unshifted3 = np.array([[x, y, 0] for x, y in zip(x_samples, y_samples_unshifted3)])
        curve_unshifted3 = VMobject(stroke_color=WHITE, stroke_width=4)
        curve_unshifted3.set_points_as_corners(curve_points_unshifted3)
        self.add(curve_unshifted3)
