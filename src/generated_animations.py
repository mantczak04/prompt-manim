from manim import *

class GeneratedScene_20260207_223622(Scene):
    def construct(self):
        # 1. Introduction of the Series
        sum_text = MathTex("S", "=", "1", "+", "2", "+", "4", "+", "8", "+", "\\dots")
        sum_text.to_edge(UP, buff=1)
        
        self.play(Write(sum_text))
        self.wait(1)

        # 2. The Algebraic Manipulation (Part 1)
        # Highlight terms from 2 onwards
        rect = SurroundingRectangle(sum_text[4:], color=YELLOW, buff=0.1)
        self.play(Create(rect))
        
        # Explain factoring out a 2
        factoring_note = Tex("Factor out a 2", color=YELLOW).scale(0.8).next_to(rect, DOWN)
        self.play(Write(factoring_note))
        self.wait(1)

        # Equation: S = 1 + 2(1 + 2 + 4 + ...)
        shifted_eq = MathTex("S", "=", "1", "+", "2", "(", "1", "+", "2", "+", "4", "+", "\\dots", ")")
        shifted_eq.next_to(sum_text, DOWN, buff=1.5)
        
        # Map original terms to factored terms
        self.play(
            ReplacementTransform(sum_text.copy(), shifted_eq),
            FadeOut(factoring_note),
            FadeOut(rect)
        )
        self.wait(1)

        # 3. The Substitution
        # Create a brace under (1 + 2 + 4 + ...)
        brace = Brace(shifted_eq[6:-1], DOWN, color=BLUE)
        brace_label = brace.get_tex("S")
        brace_label.set_color(BLUE)
        
        self.play(Create(brace), Write(brace_label))
        self.wait(1)

        # Equation: S = 1 + 2S
        algebra_eq = MathTex("S", "=", "1", "+", "2", "S")
        algebra_eq.next_to(shifted_eq, DOWN, buff=1)
        algebra_eq.set_color_by_tex("S", BLUE)
        # Left S should be white for consistency until solved
        algebra_eq[0].set_color(WHITE) 
        
        self.play(TransformMatchingTex(shifted_eq.copy(), algebra_eq))
        self.play(FadeOut(brace), FadeOut(brace_label))
        self.wait(1)

        # 4. Solving for S
        # Step: S - 2S = 1
        solve_1 = MathTex("S", "-", "2S", "=", "1")
        solve_1.move_to(algebra_eq)
        
        self.play(Indicate(algebra_eq[4:])) # Indicate 2S
        self.play(TransformMatchingTex(algebra_eq, solve_1))
        self.wait(0.5)

        # Step: -S = 1
        solve_2 = MathTex("-S", "=", "1")
        solve_2.move_to(solve_1)
        self.play(TransformMatchingTex(solve_1, solve_2))
        self.wait(0.5)

        # Final step: S = -1
        final_result = MathTex("S", "=", "-1")
        final_result.move_to(solve_2).set_color(GREEN)
        box = SurroundingRectangle(final_result, color=GREEN, buff=0.2)
        
        self.play(TransformMatchingTex(solve_2, final_result))
        self.play(Create(box))
        self.wait(2)

        # 5. The Geometric Series Perspective
        # Clear screen for new section
        self.play(FadeOut(sum_text), FadeOut(shifted_eq), FadeOut(final_result), FadeOut(box))
        
        formula = MathTex(r"\sum_{n=0}^{\infty} r^n = \frac{1}{1-r}", color=YELLOW)
        formula.to_edge(UP)
        
        constraint = Tex("Usually requires $|r| < 1$", color=RED_A).scale(0.6)
        constraint.to_corner(UR)
        
        self.play(Write(formula))
        self.play(FadeIn(constraint))
        self.wait(1)

        # Substituting r = 2
        geo_sub = MathTex("1 + 2 + 4 + 8 + \\dots", "=", "\\frac{1}{1-2}")
        geo_sub.next_to(formula, DOWN, buff=1)
        
        self.play(Write(geo_sub))
        self.wait(1)

        # Calculate result
        geo_calc = MathTex("=", "\\frac{1}{-1}", "=", "-1")
        geo_calc.next_to(geo_sub, DOWN)
        geo_calc[-1].set_color(GREEN)
        
        self.play(Write(geo_calc))
        self.wait(2)

        # 6. Visual Comparison (2-adic Intuition)
        self.play(FadeOut(geo_sub), FadeOut(geo_calc), FadeOut(formula), FadeOut(constraint))
        
        adic_title = Tex("2-adic Perspective").to_edge(UP)
        binary_val = MathTex("\\dots 111111_2")
        plus_one = MathTex("+ 1")
        line = Line(LEFT, RIGHT).width = 3
        
        binary_val.shift(UP*0.5)
        plus_one.next_to(binary_val, DOWN, aligned_edge=RIGHT)
        line.next_to(plus_one, DOWN)
        
        self.play(Write(adic_title))
        self.play(Write(binary_val))
        self.play(Write(plus_one), Create(line))
        self.wait(1)

        # Carry effect
        result_adic = MathTex("\\dots 000000_2")
        result_adic.next_to(line, DOWN, aligned_edge=RIGHT)
        
        explanation = Tex("Infinite carries make it 0", color=BLUE).scale(0.8).next_to(result_adic, DOWN)
        
        self.play(Write(result_adic))
        self.play(Write(explanation))
        self.wait(1)
        
        conclusion_logic = MathTex("S + 1 = 0 \\implies S = -1", color=GREEN).next_to(explanation, DOWN)
        self.play(Write(conclusion_logic))
        self.wait(2)

        # 7. Conclusion
        self.play(FadeOut(adic_title), FadeOut(binary_val), FadeOut(plus_one), 
                 FadeOut(line), FadeOut(result_adic), FadeOut(explanation), FadeOut(conclusion_logic))
        
        final_statement = MathTex("1 + 2 + 4 + 8 + \\dots = -1")
        final_statement.scale(1.5).set_color(GREEN)
        
        subtitle = Tex("Convergent in 2-adic numbers, divergent in Reals.").scale(0.7)
        subtitle.next_to(final_statement, DOWN, buff=0.5)
        
        self.play(Write(final_statement))
        self.play(FadeIn(subtitle))
        self.wait(3)
        
        self.play(FadeOut(final_statement), FadeOut(subtitle))