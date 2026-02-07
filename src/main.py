from manim import *

#!/usr/bin/env python

class MinimalExample(Scene):
    def construct(self):
        # Tex
        text = Tex(r"Minimal example")
        
        # MathTex
        math = MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n}")
        
        # VGroup and arrange
        group = VGroup(text, math).arrange(DOWN)
        
        # Write
        self.play(Write(text))
        
        # FadeIn with shift
        self.play(FadeIn(math, shift=DOWN))
        
        # wait
        self.wait()
        
        # to_corner
        text.to_corner(UP + LEFT)
        
        # Transform
        new_text = Tex("Transformed")
        self.play(Transform(text, new_text))
        
        # LaggedStart and FadeOut
        self.play(LaggedStart(FadeOut(math, shift=DOWN)))
        
        # NumberPlane
        grid = NumberPlane()
        
        # add
        self.add(grid)
        
        # Create with run_time and lag_ratio
        self.play(Create(grid, run_time=2, lag_ratio=0.1))
        
        # move_to
        text.move_to(ORIGIN)
        
        # prepare_for_nonlinear_transform
        grid.prepare_for_nonlinear_transform()
        
        # animate.apply_function
        self.play(
            grid.animate.apply_function(
                lambda p: p + np.array([np.sin(p[1]), np.sin(p[0]), 0])
            )
        )
        
        # Circle
        circle = Circle()
        
        # Square
        square = Square()
        
        # flip
        square.flip(RIGHT)
        
        # rotate
        square.rotate(-TAU / 4)
        
        # set_fill
        circle.set_fill(PINK, opacity=0.5)
        
        self.play(Create(square))
        self.play(Transform(square, circle))
        
        # ApplyPointwiseFunction
        self.play(
            ApplyPointwiseFunction(
                lambda point: complex_to_R3(np.exp(R3_to_complex(point))),
                square,
            )
        )
        
        # tex_to_color_map
        colored = Tex("Text", tex_to_color_map={"Text": YELLOW})
        self.play(Write(colored))
        
        # DecimalNumber
        decimal = DecimalNumber(0, show_ellipsis=True, num_decimal_places=3, include_sign=True)
        
        # to_edge
        square.to_edge(UP)
        
        # add_updater
        decimal.add_updater(lambda d: d.next_to(square, RIGHT))
        decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
        
        self.add(decimal)
        
        # animate.to_edge, rate_func, there_and_back
        self.play(square.animate.to_edge(DOWN), rate_func=there_and_back, run_time=3)
        
        # scale
        pi = MathTex(r"\pi").scale(3)
        
        # set_color
        pi.set_color(BLUE)
        
        # shift
        pi.shift(LEFT)
        
        # Triangle
        triangle = Triangle()
        
        # Polygon
        pentagon = Polygon(
            *[[np.cos(2 * np.pi / 5 * i), np.sin(2 * np.pi / 5 * i), 0] for i in range(5)]
        )
        
        shapes = VGroup(triangle, pentagon, pi)
        
        # SpiralIn with fade_in_fraction
        self.play(SpiralIn(shapes, fade_in_fraction=0.9))
        
        # set_default
        Triangle.set_default(stroke_width=10)
        
        # joint_type
        t1 = Triangle(joint_type=LineJointType.ROUND)
        t2 = Triangle(joint_type=LineJointType.BEVEL)
        
        grp = VGroup(t1, t2).arrange(RIGHT)
        
        # set with width
        grp.set(width=config.frame_width - 1)
        
        self.add(grp)
        self.wait() 