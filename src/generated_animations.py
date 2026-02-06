from manim import *

class GeneratedScene_20260206_213401(Scene):
    def construct(self):
        # 1. Create the Environment
        # A large white rectangle representing the Pong table boundaries
        boundary = Rectangle(height=6, width=10, color=WHITE)
        
        # 2. Initialize the Ball
        # Small white circle with white fill
        ball = Circle(radius=0.2, color=WHITE, fill_opacity=1)
        # Starting slightly off-center
        ball.move_to(RIGHT * 1 + UP * 1)

        # 3. Display the Setup
        self.play(Create(boundary))
        self.play(FadeIn(ball))
        self.wait(0.5)

        # Calculate bounce points
        # To make it look like it's hitting the edges, we account for the radius (0.2)
        # Boundaries: x in [-5, 5], y in [-3, 3]
        # Hitting points: x_limit = 4.8, y_limit = 2.8
        
        bounce_points = [
            [3.0, 2.8, 0],   # Bounce 1: Top Edge
            [4.8, 0.5, 0],   # Bounce 2: Right Edge
            [1.0, -2.8, 0],  # Bounce 3: Bottom Edge
            [-4.8, -1.5, 0], # Bounce 4: Left Edge
            [-2.0, 2.8, 0]   # Bounce 5: Top Edge
        ]

        # 4-8. Execute the Bounces
        # Using rate_func=linear to mimic the constant velocity of a Pong ball
        for point in bounce_points:
            self.play(
                ball.animate.move_to(point),
                run_time=0.8,
                rate_func=linear
            )

        # 9. Move to Center
        # Animate the ball moving to the exact center of the screen
        self.play(
            ball.animate.move_to(ORIGIN),
            run_time=1,
            rate_func=smooth
        )
        self.wait(0.2)

        # 10. Prepare the Symbol
        # Create a large Pi symbol using MathTex
        pi_symbol = MathTex(r"\pi", font_size=144, color=WHITE)
        pi_symbol.move_to(ORIGIN)

        # 11. Transformation
        # Morph the white circle (ball) into the Pi symbol
        self.play(
            Transform(ball, pi_symbol),
            run_time=1.5
        )

        # 12. Final Pause
        # Allow the transformation to linger for 2 seconds
        self.wait(2)

# To render this scene:
# manim -pql file_name.py GeneratedScene_20260206_213401