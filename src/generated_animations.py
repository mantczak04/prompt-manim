from manim import *
import numpy as np

class GeneratedScene_20260201_132726(Scene):
    def construct(self):
        # 1. Scene Setup
        # Create coordinate system
        axes = Axes(
            x_range=[-3 * PI, 3 * PI, PI],
            y_range=[-2.5, 2.5, 1],
            axis_config={"include_tip": True},
            tips=False
        ).scale(0.8).to_edge(DOWN, buff=0.5)

        # Labels for axes (multiples of PI)
        x_label_values = [
            (-3 * PI, "-3\\pi"), (-2 * PI, "-2\\pi"), (-PI, "-\\pi"),
            (PI, "\\pi"), (2 * PI, "2\\pi"), (3 * PI, "3\\pi")
        ]
        x_labels = VGroup()
        for val, tex in x_label_values:
            lab = MathTex(tex, font_size=20).next_to(axes.c2p(val, 0), DOWN)
            x_labels.add(lab)

        # Title and Base Equation
        title = Text("Trigonometric Transformations", font_size=36).to_edge(UP)
        eq_label = MathTex("f(x) = \\cos(x)", color=WHITE).to_edge(UR, buff=1).shift(LEFT * 0.5)
        
        # Base Curve
        cosine_curve = axes.plot(lambda x: np.cos(x), color=WHITE)
        
        # Initial Animation
        self.play(Write(axes), Write(x_labels))
        self.play(Write(title))
        self.play(Create(cosine_curve), Write(eq_label))
        self.wait(1)

        # 2. Introduce Constant a
        a_value = 2
        a_text = MathTex("a = 2", color=YELLOW).next_to(eq_label, DOWN, buff=0.5)
        self.play(FadeIn(a_text))
        self.wait(1)

        # 3. Horizontal Shift Right (x - a)
        new_eq_1 = MathTex("f(x) = \\cos(x - 2)", color=BLUE).move_to(eq_label.get_center())
        curve_shift_right = axes.plot(lambda x: np.cos(x - a_value), color=BLUE)
        
        # Arrow indicating shift
        arrow_right = Arrow(
            start=axes.c2p(0, 0), 
            end=axes.c2p(a_value, 0), 
            buff=0, 
            color=YELLOW, 
            stroke_width=5
        ).shift(UP * 0.5)
        shift_text = MathTex("+2", color=YELLOW, font_size=24).next_to(arrow_right, UP, buff=0.1)

        self.play(
            ReplacementTransform(eq_label, new_eq_1),
            Transform(cosine_curve, curve_shift_right),
            GrowArrow(arrow_right),
            Write(shift_text)
        )
        eq_label = new_eq_1 # Update reference
        self.wait(1.5)

        # 4. Horizontal Shift Left (x + a)
        new_eq_2 = MathTex("f(x) = \\cos(x + 2)", color=BLUE).move_to(eq_label.get_center())
        curve_shift_left = axes.plot(lambda x: np.cos(x + a_value), color=BLUE)
        
        arrow_left = Arrow(
            start=axes.c2p(0, 0), 
            end=axes.c2p(-a_value, 0), 
            buff=0, 
            color=YELLOW, 
            stroke_width=5
        ).shift(UP * 0.5)
        shift_text_left = MathTex("-2", color=YELLOW, font_size=24).next_to(arrow_left, UP, buff=0.1)

        self.play(
            ReplacementTransform(eq_label, new_eq_2),
            Transform(cosine_curve, curve_shift_left),
            ReplacementTransform(arrow_right, arrow_left),
            ReplacementTransform(shift_text, shift_text_left)
        )
        eq_label = new_eq_2
        self.wait(1.5)

        # 5. Horizontal Stretch (x / a)
        new_eq_3 = MathTex("f(x) = \\cos(x / 2)", color=GREEN).move_to(eq_label.get_center())
        curve_stretch = axes.plot(lambda x: np.cos(x / a_value), color=GREEN)

        self.play(
            ReplacementTransform(eq_label, new_eq_3),
            Transform(cosine_curve, curve_stretch),
            FadeOut(arrow_left),
            FadeOut(shift_text_left)
        )
        eq_label = new_eq_3
        self.wait(1.5)

        # 6. Horizontal Compression (x * a)
        new_eq_4 = MathTex("f(x) = \\cos(2x)", color=RED).move_to(eq_label.get_center())
        curve_compress = axes.plot(lambda x: np.cos(a_value * x), color=RED)

        self.play(
            ReplacementTransform(eq_label, new_eq_4),
            Transform(cosine_curve, curve_compress)
        )
        eq_label = new_eq_4
        self.wait(1.5)

        # 7. Non-linear Frequency (x^a)
        new_eq_5 = MathTex("f(x) = \\cos(x^2)", color=PURPLE).move_to(eq_label.get_center())
        # Higher density of points for the chirp effect to look smooth
        curve_chirp = axes.plot(lambda x: np.cos(x**2), color=PURPLE, x_range=[-3*PI, 3*PI], use_smoothing=True)

        self.play(
            ReplacementTransform(eq_label, new_eq_5),
            Transform(cosine_curve, curve_chirp)
        )
        eq_label = new_eq_5
        self.wait(2)

        # 8. Conclusion - Return to Original
        final_eq = MathTex("f(x) = \\cos(x)", color=WHITE).move_to(eq_label.get_center())
        original_curve = axes.plot(lambda x: np.cos(x), color=WHITE)

        self.play(
            ReplacementTransform(eq_label, final_eq),
            Transform(cosine_curve, original_curve)
        )
        self.wait(1)

        # Fade out everything
        self.play(
            FadeOut(axes),
            FadeOut(x_labels),
            FadeOut(title),
            FadeOut(final_eq),
            FadeOut(a_text),
            FadeOut(cosine_curve)
        )
        self.wait(1)

# To run this animation, use the following command:
# manim -pql scene_file_name.py GeneratedScene_20260201_132726