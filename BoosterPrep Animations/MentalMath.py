from manim import *


class MentalMath(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # =============================================
        # Phase 1: Rewrite 0.5 × 0.075 as 0.001 × 75/2
        # =============================================

        expr1 = MathTex(r"0.5", r"\times", r"0.075", color=BLACK, font_size=44)
        self.play(Write(expr1))
        self.wait(1)

        # Show recognition: 0.5 = 1/2
        note_half = MathTex(r"0.5 = \tfrac{1}{2}", color=BLUE, font_size=32)
        note_half.next_to(expr1, DOWN, buff=0.6)
        self.play(FadeIn(note_half, shift=UP * 0.2))
        self.wait(0.8)

        # Show recognition: 0.075 = 0.001 × 75
        note_75 = MathTex(r"0.075 = 0.001 \times 75", color=BLUE, font_size=32)
        note_75.next_to(note_half, DOWN, buff=0.3)
        self.play(FadeIn(note_75, shift=UP * 0.2))
        self.wait(1)

        # Transform to substituted form
        expr2 = MathTex(
            r"\tfrac{1}{2}", r"\times", r"0.001", r"\times", r"75",
            color=BLACK, font_size=44,
        )
        self.play(FadeOut(note_half, note_75))
        self.play(TransformMatchingShapes(expr1, expr2))
        self.wait(1)

        # Rearrange to 0.001 × 75/2
        expr3 = MathTex(
            r"0.001", r"\times", r"\frac{75}{2}",
            color=BLACK, font_size=44,
        )
        self.play(TransformMatchingShapes(expr2, expr3))
        self.wait(1.5)

        # Move expression up to make room for long division
        self.play(expr3.animate.to_edge(UP, buff=0.5))

        # =============================================
        # Phase 2: Long division 75 ÷ 2
        # =============================================

        div_label = Text(
            "Long division: 75 ÷ 2",
            font="Segoe UI", font_size=26, color=BLUE,
        ).next_to(expr3, DOWN, buff=0.5).align_to(expr3, LEFT)
        self.play(Write(div_label))

        # Build the long division layout
        #    3 7 . 5
        #   -------
        # 2 | 7 5 . 0

        div_group_pos = div_label.get_center() + DOWN * 2

        divisor = MathTex(r"2", color=BLACK, font_size=40)
        dividend = MathTex(r"7", r"5", r".", r"0", color=BLACK, font_size=40)
        dividend.arrange(RIGHT, buff=0.15)

        # Position divisor and dividend
        divisor.move_to(div_group_pos + LEFT * 1.8)
        dividend.move_to(div_group_pos + RIGHT * 0.1)

        # The "bracket" lines
        vert_line = Line(
            divisor.get_corner(UR) + RIGHT * 0.1 + UP * 0.25,
            divisor.get_corner(DR) + RIGHT * 0.1 + DOWN * 0.05,
            color=BLACK, stroke_width=2,
        )
        horiz_line = Line(
            vert_line.get_top(),
            vert_line.get_top() + RIGHT * (dividend.get_width() + 0.3),
            color=BLACK, stroke_width=2,
        )

        self.play(
            FadeIn(divisor),
            FadeIn(dividend),
            Create(vert_line),
            Create(horiz_line),
        )
        self.wait(0.5)

        # Quotient digits will go above the horizontal line
        q_offset = horiz_line.get_top() + UP * 0.15

        # --- Step 1: 7 ÷ 2 = 3 remainder 1 ---
        q3 = MathTex(r"3", color=RED, font_size=40)
        q3.move_to(q_offset + RIGHT * (dividend[0].get_center()[0] - dividend.get_center()[0]))

        step1_note = Text("7 ÷ 2 = 3 R1", font="Segoe UI", font_size=22, color=DARK_GRAY)
        step1_note.next_to(dividend, RIGHT, buff=0.8)

        self.play(Write(q3), FadeIn(step1_note, shift=LEFT * 0.2))
        self.wait(0.5)

        # Show subtraction: 3×2 = 6, 7-6 = 1, bring down 5 → 15
        sub6 = MathTex(r"6", color=BLACK, font_size=40)
        sub6.next_to(dividend[0], DOWN, buff=0.3)
        sub_line1 = Line(
            sub6.get_corner(DL) + DOWN * 0.08 + LEFT * 0.05,
            sub6.get_corner(DR) + DOWN * 0.08 + RIGHT * 0.05,
            color=BLACK, stroke_width=2,
        )
        minus1 = MathTex(r"-", color=BLACK, font_size=32).next_to(sub6, LEFT, buff=0.1)

        self.play(FadeIn(minus1, sub6), Create(sub_line1))

        rem15 = MathTex(r"1", r"5", color=BLACK, font_size=40)
        rem15.arrange(RIGHT, buff=0.15)
        rem15.next_to(sub_line1, DOWN, buff=0.15)
        rem15.align_to(dividend[1], RIGHT)

        self.play(Write(rem15))
        self.wait(0.5)
        self.play(FadeOut(step1_note))

        # --- Step 2: 15 ÷ 2 = 7 remainder 1 ---
        q7 = MathTex(r"7", color=RED, font_size=40)
        q7.move_to(q_offset + RIGHT * (dividend[1].get_center()[0] - dividend.get_center()[0]))

        step2_note = Text("15 ÷ 2 = 7 R1", font="Segoe UI", font_size=22, color=DARK_GRAY)
        step2_note.next_to(dividend, RIGHT, buff=0.8)

        self.play(Write(q7), FadeIn(step2_note, shift=LEFT * 0.2))
        self.wait(0.5)

        sub14 = MathTex(r"1", r"4", color=BLACK, font_size=40)
        sub14.arrange(RIGHT, buff=0.15)
        sub14.next_to(rem15, DOWN, buff=0.3)
        sub14.align_to(rem15, RIGHT)
        sub_line2 = Line(
            sub14.get_corner(DL) + DOWN * 0.08 + LEFT * 0.05,
            sub14.get_corner(DR) + DOWN * 0.08 + RIGHT * 0.05,
            color=BLACK, stroke_width=2,
        )
        minus2 = MathTex(r"-", color=BLACK, font_size=32).next_to(sub14, LEFT, buff=0.1)

        self.play(FadeIn(minus2, sub14), Create(sub_line2))

        rem10 = MathTex(r"1", r"0", color=BLACK, font_size=40)
        rem10.arrange(RIGHT, buff=0.15)
        rem10.next_to(sub_line2, DOWN, buff=0.15)
        # Align with the decimal: shift one digit right
        rem10.align_to(dividend[3], RIGHT)

        # Decimal point in quotient
        q_dot = MathTex(r".", color=RED, font_size=40)
        q_dot.move_to(q_offset + RIGHT * (dividend[2].get_center()[0] - dividend.get_center()[0]))

        self.play(Write(rem10), Write(q_dot))
        self.wait(0.5)
        self.play(FadeOut(step2_note))

        # --- Step 3: 10 ÷ 2 = 5 remainder 0 ---
        q5 = MathTex(r"5", color=RED, font_size=40)
        q5.move_to(q_offset + RIGHT * (dividend[3].get_center()[0] - dividend.get_center()[0]))

        step3_note = Text("10 ÷ 2 = 5 R0", font="Segoe UI", font_size=22, color=DARK_GRAY)
        step3_note.next_to(dividend, RIGHT, buff=0.8)

        self.play(Write(q5), FadeIn(step3_note, shift=LEFT * 0.2))
        self.wait(0.5)

        sub10 = MathTex(r"1", r"0", color=BLACK, font_size=40)
        sub10.arrange(RIGHT, buff=0.15)
        sub10.next_to(rem10, DOWN, buff=0.3)
        sub10.align_to(rem10, RIGHT)
        sub_line3 = Line(
            sub10.get_corner(DL) + DOWN * 0.08 + LEFT * 0.05,
            sub10.get_corner(DR) + DOWN * 0.08 + RIGHT * 0.05,
            color=BLACK, stroke_width=2,
        )
        minus3 = MathTex(r"-", color=BLACK, font_size=32).next_to(sub10, LEFT, buff=0.1)

        self.play(FadeIn(minus3, sub10), Create(sub_line3))

        rem0 = MathTex(r"0", color=BLACK, font_size=40)
        rem0.next_to(sub_line3, DOWN, buff=0.15)
        rem0.align_to(sub10, RIGHT)

        self.play(Write(rem0))
        self.wait(0.5)
        self.play(FadeOut(step3_note))

        # Highlight the quotient
        quotient_group = VGroup(q3, q7, q_dot, q5)
        q_box = SurroundingRectangle(quotient_group, color=GREEN, buff=0.1)
        self.play(Create(q_box))
        self.wait(1.5)

        # =============================================
        # Phase 3: Substitute 37.5 back in
        # =============================================

        # Fade out long division
        div_all = VGroup(
            div_label, divisor, dividend, vert_line, horiz_line,
            q3, q7, q_dot, q5, q_box,
            minus1, sub6, sub_line1, rem15,
            minus2, sub14, sub_line2, rem10,
            minus3, sub10, sub_line3, rem0,
        )
        self.play(FadeOut(div_all))

        # Show the substitution: 0.001 × 75/2  →  0.001 × 37.5
        self.play(expr3.animate.move_to(ORIGIN))
        self.wait(0.5)

        expr4 = MathTex(
            r"0.001", r"\times", r"37.5",
            color=BLACK, font_size=44,
        )
        self.play(TransformMatchingShapes(expr3, expr4))
        self.wait(1)

        # Final result
        expr5 = MathTex(
            r"= \, 0.0375",
            color=BLACK, font_size=44,
        ).next_to(expr4, DOWN, buff=0.4)

        self.play(Write(expr5))

        final_group = VGroup(expr4, expr5)
        final_box = SurroundingRectangle(final_group, color=RED, buff=0.15, corner_radius=0.1)
        self.play(Create(final_box))
        self.wait(1)

        # Clean up to final answer
        answer = MathTex(r"0.5 \times 0.075 = 0.0375", color=BLACK, font_size=48)
        answer_box = SurroundingRectangle(answer, color=RED, buff=0.15, corner_radius=0.1)

        self.play(
            FadeOut(expr4, expr5, final_box),
            FadeIn(answer),
        )
        self.play(Create(answer_box))
        self.wait(3)
