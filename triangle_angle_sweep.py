from manim import *
import numpy as np


class TriangleAngleSweep(Scene):
    """Animate a triangle as its interior angle sweeps from ~0° to 90°,
    showing how the side lengths change. The triangle is oriented so that
    the 'opposite' side is on the right side of the screen."""

    def construct(self):
        # --- layout constants ---
        hyp_len = 4.0
        vertex_left = LEFT * 3  # vertex where the swept angle lives

        # --- angle tracker ---
        theta = ValueTracker(45)  # degrees
        
        # Set background to white
        self.camera.background_color = WHITE


        # --- helper: triangle vertices from angle ---
        def get_points(angle_deg):
            rad = angle_deg * DEGREES
            A = vertex_left
            adj = hyp_len * np.cos(rad)
            opp = hyp_len * np.sin(rad)
            B = A + RIGHT * adj          # bottom-right (right angle here)
            C = B + UP * opp             # top-right
            return A, B, C, adj, opp

        # --- colored triangle sides ---
        def make_sides():
            A, B, C, _, _ = get_points(theta.get_value())
            return VGroup(
                Line(A, B, color=GREEN, stroke_width=3),   # adjacent
                Line(B, C, color=RED, stroke_width=3),      # opposite
                Line(A, C, color=BLUE, stroke_width=3),     # hypotenuse
            )

        sides = always_redraw(make_sides)

        # --- right-angle marker at B ---
        def make_right_angle():
            A, B, C, _, _ = get_points(theta.get_value())
            s = 0.22
            return VMobject(stroke_width=1.5, color=BLACK).set_points_as_corners([
                B + UP * s, B + UP * s + LEFT * s, B + LEFT * s, B
            ])

        right_mark = always_redraw(make_right_angle)

        # --- angle arc at A ---
        def make_arc():
            A, B, C, _, _ = get_points(theta.get_value())
            rad = theta.get_value() * DEGREES
            return Arc(radius=0.55, start_angle=0, angle=rad,
                       arc_center=A, color=ORANGE, stroke_width=2)

        angle_arc = always_redraw(make_arc)

        # --- angle label ---
        def make_angle_label():
            A, B, C, _, _ = get_points(theta.get_value())
            rad = theta.get_value() * DEGREES
            mid = rad / 2
            # Adjust the positioning of the label so that it is further from the arc as the angle becomes shorter, and closer as the angle becomes longer.
            pos = A + 0.75 * np.array([np.cos(mid), np.sin(mid), 0])  # position at the midpoint of the arc
            pos += np.array([np.cos(mid), np.sin(mid), 0]) * (1 - theta.get_value() / 90)  # adjust position based on angle
            t = Text(f"{theta.get_value():.0f}°", color=ORANGE, font="Open Sans")
            t.scale(0.5)
            t.move_to(pos)
            return t

        angle_label = always_redraw(make_angle_label)

        def make_adj_label():
            A, B, C, adj, opp = get_points(theta.get_value())
            mid = (A + B) / 2
            if adj < opp:
                display_text = "shorter"
            elif adj > opp:
                display_text = "longer"
            else:
                display_text = "equal"
            t = Text(display_text, color=RED, font="Open Sans")
            t.scale(0.5)
            t.next_to(mid, DOWN, buff=0.25)
            return t

        adj_label = always_redraw(make_adj_label)

        def make_opp_label():
            A, B, C, adj, opp = get_points(theta.get_value())
            mid = (B + C) / 2
            if adj > opp:
                display_text = "shorter"
            elif adj < opp:
                display_text = "longer"
            else:
                display_text = "equal"
            t = Text(display_text, color=RED, font="Open Sans")
            t.scale(0.5)
            t.next_to(mid, RIGHT, buff=0.25)
            return t

        opp_label = always_redraw(make_opp_label)


        # --- show everything ---
        self.play(
            FadeIn(sides), FadeIn(right_mark),
            FadeIn(angle_arc), FadeIn(angle_label),
            FadeIn(adj_label), FadeIn(opp_label),
            run_time=0.1,
        )

        self.wait(0.1)
        explanations = [
            ("At 45°, the sides are the same length.", 45),
            ("Above 45°, the adjacent side is shorter.", 60),
            ("Below 45°, the adjacent side is longer.", 30),    
        ]
        
        expl = Text(explanations[0][0], color=BLACK, font="Open Sans").move_to(sides.get_bottom() + DOWN)
        expl.scale(0.5)
        self.play(Write(expl))
        
        for i in range(1, len(explanations)):
            text, angle = explanations[i]
            self.play(theta.animate.set_value(angle), rate_func=smooth, run_time=1)
            expl_new = Text(text, color=BLACK, font="Open Sans").next_to(expl, DOWN, buff=-0.1)
            expl_new.scale(0.5)
            self.play(Write(expl_new))
            self.wait(0.5)
            expl = expl_new


        self.play(FadeOut(Group(*self.mobjects)))
