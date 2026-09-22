from manim import *

# Render at high resolution (4K/60fps). Run with:
#   manim -p multi_part_ratio.py MultiPartRatio
# (add -ql instead while iterating, for a fast low-res preview)
config.pixel_width = 3840
config.pixel_height = 2160
config.frame_rate = 60

FONT = "Open Sans"
FS = 40  # base font size for ratio/fraction text

RED_P = "#E5484D"
BLUE_P = "#3E7BFA"
GREEN_P = "#30A46C"
HILITE = YELLOW

S = 0.3       # width of one small "part" (Mixture B's part size)
H = 0.65      # height of every paint bar
X0 = -5.9     # left edge of the bar area
Y_A = 1.4     # row for Mixture A
Y_B = -0.9    # row for Mixture B
MATH_X = 0.9  # left edge of the math column


class MultiPartRatio(Scene):
    """Red:Blue = 2:3 and Blue:Green = 9:4 combined into Red:Blue:Green = 6:9:4.

    Each ratio is drawn as a bar of equal-sized paint "parts". Mixture A's parts
    are 3x wider than Mixture B's, so both blue sections have the same length
    (the same amount of blue). Cutting every A part into thirds turns 2:3 into
    6:9, the blue parts then line up one-to-one, and the bars merge.
    """

    def construct(self):
        self.camera.background_color = BLACK
        self.caption = None

        # ---------- helpers ----------
        def txt(s, color=WHITE, fs=FS):
            return Text(s, font=FONT, font_size=fs, color=color)

        def parts(n, w, color):
            return VGroup(*[
                Rectangle(width=w, height=H, fill_color=color, fill_opacity=1,
                          stroke_color=BLACK, stroke_width=5)
                for _ in range(n)
            ]).arrange(RIGHT, buff=0)

        def ratio_row(w1, c1, w2, c2, n1, n2):
            # [word1, ":", word2, "=", n1, ":", n2]
            return VGroup(
                txt(w1, c1), txt(":"), txt(w2, c2), txt("="),
                txt(n1, c1), txt(":"), txt(n2, c2),
            ).arrange(RIGHT, buff=0.2)

        def fraction(top, bot):
            line = Line(LEFT, RIGHT, color=WHITE, stroke_width=3)
            line.width = max(top.width, bot.width) + 0.3
            top.next_to(line, UP, buff=0.12)
            bot.next_to(line, DOWN, buff=0.12)
            return VGroup(top, line, bot)

        def fraction_row(w1, c1, w2, c2, n1, n2):
            # [[word1, line, word2], "=", [n1, line, n2]]
            return VGroup(
                fraction(txt(w1, c1), txt(w2, c2)), txt("="),
                fraction(txt(n1, c1), txt(n2, c2)),
            ).arrange(RIGHT, buff=0.3)

        def set_caption(s):
            new = txt(s, GREY_A, 34).move_to(UP * 3.4)
            if self.caption is None:
                self.play(FadeIn(new, shift=DOWN * 0.2))
            else:
                self.play(FadeOut(self.caption, shift=UP * 0.2),
                          FadeIn(new, shift=UP * 0.2))
            self.caption = new

        def tag(letter, y):
            c = Circle(radius=0.28, color=GREY_B, stroke_width=3)
            return VGroup(c, txt(letter, GREY_A, 28)).move_to([X0 - 0.6, y, 0])

        def paint_can(color, name):
            body = RoundedRectangle(corner_radius=0.1, width=1.4, height=1.6,
                                    fill_color="#8A8F98", fill_opacity=1,
                                    stroke_color=GREY_B, stroke_width=3)
            band = Rectangle(width=1.4, height=0.6, fill_color=color,
                             fill_opacity=1, stroke_width=0).move_to(body)
            top = Ellipse(width=1.4, height=0.35, fill_color=color,
                          fill_opacity=1, stroke_color=GREY_B, stroke_width=3)
            top.move_to(body.get_top())
            handle = Arc(radius=0.75, start_angle=PI * 0.15, angle=PI * 0.7,
                         color=GREY_B, stroke_width=4)
            handle.move_to(top.get_center() + UP * 0.3)
            label = txt(name, color, 30).next_to(body, DOWN, buff=0.3)
            return VGroup(handle, body, band, top, label)

        # =============================================
        # Intro: three colors of paint
        # =============================================
        set_caption("Three colors of paint: red, blue, and green")
        cans = VGroup(
            paint_can(RED_P, "Red"),
            paint_can(BLUE_P, "Blue"),
            paint_can(GREEN_P, "Green"),
        ).arrange(RIGHT, buff=1.6).move_to(DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.5) for c in cans],
                              lag_ratio=0.25))
        self.wait(1.5)
        self.play(LaggedStart(*[FadeOut(c, shift=DOWN * 0.5) for c in cans],
                              lag_ratio=0.15))

        # =============================================
        # Mixture A: red : blue = 2 : 3  (big parts, 3S wide)
        # =============================================
        set_caption("Mixture A: red to blue is 2 to 3")
        a_red = parts(2, 3 * S, RED_P)
        a_blue = parts(3, 3 * S, BLUE_P)
        bar_a = VGroup(a_red, a_blue).arrange(RIGHT, buff=0)
        bar_a.move_to([X0, Y_A, 0], aligned_edge=LEFT)
        tag_a = tag("A", Y_A)

        ratio_a = ratio_row("Red", RED_P, "Blue", BLUE_P, "2", "3")
        ratio_a.move_to([MATH_X, Y_A, 0], aligned_edge=LEFT)

        self.play(FadeIn(tag_a))
        self.play(
            LaggedStart(*[GrowFromEdge(p, LEFT) for p in [*a_red, *a_blue]],
                        lag_ratio=0.2),
            Write(ratio_a),
            run_time=2,
        )
        self.wait(1.5)

        # =============================================
        # Mixture B: blue : green = 9 : 4  (small parts, S wide)
        # Its blue section sits directly under A's blue section.
        # =============================================
        set_caption("Mixture B: blue to green is 9 to 4")
        b_blue = parts(9, S, BLUE_P)
        b_green = parts(4, S, GREEN_P)
        bar_b = VGroup(b_blue, b_green).arrange(RIGHT, buff=0)
        bar_b.move_to([a_blue.get_left()[0], Y_B, 0], aligned_edge=LEFT)
        tag_b = tag("B", Y_B)

        ratio_b = ratio_row("Blue", BLUE_P, "Green", GREEN_P, "9", "4")
        ratio_b.move_to([MATH_X, Y_B, 0], aligned_edge=LEFT)

        self.play(FadeIn(tag_b))
        self.play(
            LaggedStart(*[GrowFromEdge(p, LEFT) for p in [*b_blue, *b_green]],
                        lag_ratio=0.08),
            Write(ratio_b),
            run_time=2,
        )
        self.wait(1.5)

        # =============================================
        # Same amount of blue in both mixtures
        # =============================================
        set_caption("Keep the same amount of blue in both mixtures")
        guides = VGroup(*[
            DashedLine([x, Y_A + H / 2 + 0.15, 0], [x, Y_B - H / 2 - 0.15, 0],
                       color=HILITE, stroke_width=3, dash_length=0.1)
            for x in (a_blue.get_left()[0], a_blue.get_right()[0])
        ])
        blue_boxes = VGroup(
            SurroundingRectangle(a_blue, color=HILITE, buff=0.06),
            SurroundingRectangle(b_blue, color=HILITE, buff=0.06),
        )
        self.play(Create(guides), Create(blue_boxes))
        self.wait(1.5)
        self.play(FadeOut(guides), FadeOut(blue_boxes))

        # =============================================
        # The question: Red : Blue : Green = ? : ? : ?
        # =============================================
        set_caption("What is the combined ratio?")
        question = VGroup(
            txt("Red", RED_P), txt(":"), txt("Blue", BLUE_P), txt(":"),
            txt("Green", GREEN_P), txt("="),
            txt("?", RED_P), txt(":"), txt("?", BLUE_P), txt(":"),
            txt("?", GREEN_P),
        ).arrange(RIGHT, buff=0.2).move_to(DOWN * 3.1)
        q_marks = [question[6], question[8], question[10]]
        self.play(Write(question))
        self.wait(2)

        # =============================================
        # Isolate the info: ratios as fractions (blue on the bottom)
        # =============================================
        set_caption("Write each ratio as a fraction")
        self.play(Indicate(ratio_a, color=HILITE, scale_factor=1.08))

        frac_a = fraction_row("Red", RED_P, "Blue", BLUE_P, "2", "3")
        frac_a.move_to([MATH_X, Y_A, 0], aligned_edge=LEFT)
        (fa_wtop, fa_wline, fa_wbot), fa_eq, (fa_top, fa_line, fa_bot) = frac_a
        self.play(
            ReplacementTransform(ratio_a[0], fa_wtop),
            ReplacementTransform(ratio_a[1], fa_wline),
            ReplacementTransform(ratio_a[2], fa_wbot),
            ReplacementTransform(ratio_a[3], fa_eq),
            ReplacementTransform(ratio_a[4], fa_top),
            ReplacementTransform(ratio_a[5], fa_line),
            ReplacementTransform(ratio_a[6], fa_bot),
            run_time=1.5,
        )
        self.wait(1.5)

        # Flip B around so blue is second: green : blue = 4 : 9
        flipped = ratio_row("Green", GREEN_P, "Blue", BLUE_P, "4", "9")
        flipped.move_to([MATH_X, Y_B, 0], aligned_edge=LEFT)
        self.play(
            ratio_b[0].animate(path_arc=-PI / 2).move_to(flipped[2]),
            ratio_b[2].animate(path_arc=-PI / 2).move_to(flipped[0]),
            ratio_b[4].animate(path_arc=-PI / 2).move_to(flipped[6]),
            ratio_b[6].animate(path_arc=-PI / 2).move_to(flipped[4]),
            ratio_b[1].animate.move_to(flipped[1]),
            ratio_b[3].animate.move_to(flipped[3]),
            ratio_b[5].animate.move_to(flipped[5]),
            run_time=1.5,
        )
        self.wait(1)

        frac_b = fraction_row("Green", GREEN_P, "Blue", BLUE_P, "4", "9")
        frac_b.move_to([MATH_X, Y_B, 0], aligned_edge=LEFT)
        (fb_wtop, fb_wline, fb_wbot), fb_eq, (fb_top, fb_line, fb_bot) = frac_b
        self.play(
            ReplacementTransform(ratio_b[2], fb_wtop),
            ReplacementTransform(ratio_b[1], fb_wline),
            ReplacementTransform(ratio_b[0], fb_wbot),
            ReplacementTransform(ratio_b[3], fb_eq),
            ReplacementTransform(ratio_b[6], fb_top),
            ReplacementTransform(ratio_b[5], fb_line),
            ReplacementTransform(ratio_b[4], fb_bot),
            run_time=1.5,
        )
        self.wait(1.5)

        # =============================================
        # The parts don't match: 3 big blue parts vs 9 small ones
        # =============================================
        set_caption("The blue parts aren't the same size yet")

        def brace_label(mob, direction, s, color, scale=0.8):
            b = Brace(mob, direction, buff=0.08, color=GREY_B)
            label = txt(s, color).scale(scale)
            b.put_at_tip(label, buff=0.12)
            return VGroup(b, label)

        def brace_text(s, color, like):
            return txt(s, color).scale(0.8).move_to(like)

        br_a_red = brace_label(a_red, UP, "2 parts", RED_P)
        br_a_blue = brace_label(a_blue, UP, "3 parts", BLUE_P)
        br_b_blue = brace_label(b_blue, DOWN, "9 parts", BLUE_P)

        self.play(FadeIn(br_a_red), FadeIn(br_a_blue), FadeIn(br_b_blue))
        self.play(Indicate(fa_bot, color=HILITE), Indicate(fb_bot, color=HILITE))
        self.wait(1)

        # One big A part = three small B parts
        one_big = SurroundingRectangle(a_blue[0], color=HILITE, buff=0.03)
        three_small = SurroundingRectangle(b_blue[:3], color=HILITE, buff=0.03)
        self.play(Create(one_big))
        self.play(TransformFromCopy(one_big, three_small))
        self.wait(1.5)
        self.play(FadeOut(one_big), FadeOut(three_small))

        # =============================================
        # Scale 2/3 up to 6/9: cut every A part into thirds
        # =============================================
        set_caption("Multiply the top and bottom by 3")
        self.play(Indicate(fb_bot, color=HILITE, scale_factor=1.3))

        x3_top = txt("× 3", HILITE).next_to(fa_top, RIGHT, buff=0.15)
        x3_bot = txt("× 3", HILITE).next_to(fa_bot, RIGHT, buff=0.15)
        self.play(Write(x3_top), Write(x3_bot))
        self.wait(0.5)

        # Yellow cut lines through each big part
        cuts = VGroup()
        for p in [*a_red, *a_blue]:
            for k in (1, 2):
                x = p.get_left()[0] + k * S
                cuts.add(Line([x, Y_A + H / 2, 0], [x, Y_A - H / 2, 0],
                              color=HILITE, stroke_width=4))
        self.play(LaggedStart(*[Create(c) for c in cuts], lag_ratio=0.08),
                  run_time=1.5)

        new_red = parts(6, S, RED_P).move_to(a_red)
        new_blue = parts(9, S, BLUE_P).move_to(a_blue)
        new_top = txt("6", RED_P).move_to(fa_top)
        new_bot = txt("9", BLUE_P).move_to(fa_bot)
        self.play(
            FadeOut(cuts),
            ReplacementTransform(a_red, new_red),
            ReplacementTransform(a_blue, new_blue),
            ReplacementTransform(VGroup(fa_top, x3_top), new_top),
            ReplacementTransform(VGroup(fa_bot, x3_bot), new_bot),
            Transform(br_a_red[1], brace_text("6 parts", RED_P, br_a_red[1])),
            Transform(br_a_blue[1], brace_text("9 parts", BLUE_P, br_a_blue[1])),
            run_time=1.5,
        )
        a_red, a_blue, fa_top, fa_bot = new_red, new_blue, new_top, new_bot
        self.wait(1)

        # ...which is the ratio 6 : 9
        arrow = Arrow(LEFT, RIGHT, color=GREY_B, stroke_width=4,
                      max_tip_length_to_length_ratio=0.3).scale(0.4)
        arrow.next_to(VGroup(fa_top, fa_line, fa_bot), RIGHT, buff=0.3)
        ratio_69 = VGroup(txt("6", RED_P), txt(":"), txt("9", BLUE_P))
        ratio_69.arrange(RIGHT, buff=0.2).next_to(arrow, RIGHT, buff=0.3)
        self.play(GrowArrow(arrow), FadeIn(ratio_69, shift=RIGHT * 0.2))
        self.wait(1)

        # Every blue part now lines up one-to-one
        set_caption("Now the blue parts match, 9 for 9")
        matches = VGroup(*[
            Line(top.get_bottom(), bot.get_top(), color=HILITE, stroke_width=2)
            for top, bot in zip(a_blue, b_blue)
        ])
        self.play(LaggedStart(*[Create(m) for m in matches], lag_ratio=0.1))
        self.wait(1.5)

        # =============================================
        # Combine: slide the bars together along the shared blue
        # =============================================
        set_caption("Combine the two mixtures")
        self.play(FadeOut(matches), FadeOut(br_a_red), FadeOut(br_a_blue),
                  FadeOut(br_b_blue), FadeOut(tag_a), FadeOut(tag_b))

        y_mid = (Y_A + Y_B) / 2
        self.play(
            VGroup(a_red, a_blue).animate.shift(UP * (y_mid - Y_A)),
            VGroup(b_blue, b_green).animate.shift(UP * (y_mid - Y_B)),
            run_time=1.5,
        )
        self.remove(a_blue)  # b_blue now sits exactly on top of it
        self.play(Flash(b_blue.get_center(), color=HILITE, line_length=0.4,
                        flash_radius=b_blue.width / 2 + 0.2))
        combined = VGroup(a_red, b_blue, b_green)
        self.wait(1)

        # Count the parts of each color
        br_red = brace_label(a_red, DOWN, "6", RED_P, scale=1)
        br_blue = brace_label(b_blue, DOWN, "9", BLUE_P, scale=1)
        br_green = brace_label(b_green, DOWN, "4", GREEN_P, scale=1)
        self.play(LaggedStart(FadeIn(br_red), FadeIn(br_blue), FadeIn(br_green),
                              lag_ratio=0.4))
        self.wait(0.5)

        # =============================================
        # Fill in the answer: 6 red, 9 blue (from A), 4 green (from B)
        # =============================================
        set_caption("6 parts red, 9 parts blue, 4 parts green")
        sources = [(br_red[1], fa_top), (br_blue[1], fa_bot),
                   (br_green[1], fb_top)]
        answers = [txt(s, c).move_to(q) for s, c, q in
                   zip("694", [RED_P, BLUE_P, GREEN_P], q_marks)]
        for (from_bar, from_frac), ans, q in zip(sources, answers, q_marks):
            self.play(
                Indicate(from_frac, color=HILITE),
                FadeOut(q),
                TransformFromCopy(from_bar, ans, path_arc=-PI / 4),
                run_time=1,
            )

        answer_box = SurroundingRectangle(
            VGroup(question[0], *answers), color=HILITE, buff=0.2,
            corner_radius=0.1,
        )
        self.play(Create(answer_box))
        self.play(Circumscribe(combined, color=HILITE, buff=0.1))
        self.wait(3)
