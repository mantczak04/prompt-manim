from manim import *

class GeneratedScene_20260221_141530(Scene):
    def construct(self):
        # 1. Setup the Coordinate System
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True}
        ).shift(DOWN * 0.5)
        
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        # Define a function: f(x) = 0.5x^2 + 1
        def func(x):
            return 0.5 * (x**2) + 1
            
        graph = axes.plot(func, x_range=[0, 4], color=BLUE)
        graph_label = MathTex("f(x)").next_to(graph, UR, buff=0.1)

        # Step 1: Display Axes and Graph
        self.play(Create(axes), Write(labels))
        self.play(Create(graph), Write(graph_label))
        self.wait(1)

        # 2. Concept: Area under the curve
        # We want to find the area between a and b
        a, b = 1, 3.5
        line_a = axes.get_vertical_line(axes.c2p(a, func(a)), color=WHITE)
        line_b = axes.get_vertical_line(axes.c2p(b, func(b)), color=WHITE)
        label_a = MathTex("a").next_to(axes.c2p(a, 0), DOWN)
        label_b = MathTex("b").next_to(axes.c2p(b, 0), DOWN)

        self.play(Create(line_a), Create(line_b), Write(label_a), Write(label_b))
        self.wait(1)

        # 3. Riemann Sums: Approximation with Rectangles
        # Start with a coarse approximation (large dx)
        dx_coarse = 1.0
        rects_1 = axes.get_riemann_rectangles(
            graph, 
            x_range=[a, b], 
            dx=dx_coarse, 
            stroke_width=0.5, 
            fill_opacity=0.5,
            color=YELLOW
        )
        
        approx_text = MathTex(r"\text{Area } \approx \sum f(x_i) \Delta x").to_edge(UP)
        
        self.play(Write(approx_text))
        self.play(Create(rects_1))
        self.wait(1)

        # Transition to finer approximation (smaller dx)
        dx_medium = 0.4
        rects_2 = axes.get_riemann_rectangles(
            graph, 
            x_range=[a, b], 
            dx=dx_medium, 
            stroke_width=0.3, 
            fill_opacity=0.5,
            color=YELLOW
        )
        
        self.play(Transform(rects_1, rects_2))
        self.wait(0.5)

        dx_fine = 0.1
        rects_3 = axes.get_riemann_rectangles(
            graph, 
            x_range=[a, b], 
            dx=dx_fine, 
            stroke_width=0.1, 
            fill_opacity=0.5,
            color=YELLOW
        )
        
        self.play(Transform(rects_1, rects_3))
        self.wait(1)

        # 4. The limit: The Definite Integral
        # Representing the exact area
        exact_area = axes.get_area(graph, x_range=[a, b], color=BLUE, opacity=0.6)
        integral_tex = MathTex(r"\text{Area} = \int_{a}^{b} f(x) \, dx").to_edge(UP)

        self.play(
            FadeOut(rects_1),
            FadeIn(exact_area),
            Transform(approx_text, integral_tex)
        )
        self.play(approx_text.animate.set_color(BLUE))
        
        self.wait(3)