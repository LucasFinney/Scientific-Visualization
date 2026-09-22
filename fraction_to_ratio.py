from manim import *

# Render at high resolution (4K/60fps). Run with:
#   manim -p fraction_to_ratio.py FractionToRatio
# (add -ql instead while iterating, for a fast low-res preview)
config.pixel_width = 3840
config.pixel_height = 2160
config.frame_rate = 60

FONT = "Open Sans"
FS = 34  # base font size for all fraction/ratio text


class FractionToRatio(Scene):
    """2 dogs/1 cat and 3 hamsters/4 cats -> equivalent ratios -> a single
    combined ratio 8 dogs : 4 cats : 3 hamsters -> bare numbers 8 : 4 : 3."""

    def construct(self):
        self.camera.background_color = BLACK

        def make_fraction(num_str, den_str):
            num = Text(num_str, font=FONT, font_size=FS, color=WHITE)
            den = Text(den_str, font=FONT, font_size=FS, color=WHITE)
            line = Line(LEFT, RIGHT, color=WHITE, stroke_width=3)
            line.width = max(num.width, den.width) + 0.4
            num.next_to(line, UP, buff=0.15)
            den.next_to(line, DOWN, buff=0.15)
            return VGroup(num, line, den)

        # =============================================
        # Step 1: show "2 dogs / 1 cat" and "3 hamsters / 4 cats"
        # =============================================
        frac1 = make_fraction("2 dogs", "1 cat").move_to(LEFT * 3.2)
        frac2 = make_fraction("3 hamsters", "4 cats").move_to(RIGHT * 3.2)
        num1, line1, den1 = frac1
        num2, line2, den2 = frac2

        self.play(Write(frac1), Write(frac2))
        self.wait(1)

        # =============================================
        # Step 2: morph "2 dogs / 1 cat" into "8 dogs / 4 cats"
        # =============================================
        new_frac1 = make_fraction("8 dogs", "4 cats").move_to(frac1.get_center())
        self.play(TransformMatchingShapes(frac1, new_frac1))
        self.wait(1)
        frac1 = new_frac1
        num1, line1, den1 = frac1

        # =============================================
        # Step 3: flip "3 hamsters / 4 cats" into "4 cats / 3 hamsters"
        # =============================================
        self.play(CyclicReplace(num2, den2))
        self.wait(1)
        num2, den2 = den2, num2  # num2 now holds "4 cats" (top), den2 "3 hamsters" (bottom)

        # =============================================
        # Step 4: morph the fraction notation into two ratios
        #   "8 dogs : 4 cats"  and  "4 cats : 3 hamsters"
        # =============================================
        ratio1_layout = VGroup(
            Text("8 dogs", font=FONT, font_size=FS, color=WHITE),
            Text(":", font=FONT, font_size=FS, color=WHITE),
            Text("4 cats", font=FONT, font_size=FS, color=WHITE),
        ).arrange(RIGHT, buff=0.25).move_to(frac1.get_center())

        ratio2_layout = VGroup(
            Text("4 cats", font=FONT, font_size=FS, color=WHITE),
            Text(":", font=FONT, font_size=FS, color=WHITE),
            Text("3 hamsters", font=FONT, font_size=FS, color=WHITE),
        ).arrange(RIGHT, buff=0.25).move_to(frac2.get_center())

        self.play(
            num1.animate.move_to(ratio1_layout[0].get_center()),
            Transform(line1, ratio1_layout[1]),
            den1.animate.move_to(ratio1_layout[2].get_center()),
            num2.animate.move_to(ratio2_layout[0].get_center()),
            Transform(line2, ratio2_layout[1]),
            den2.animate.move_to(ratio2_layout[2].get_center()),
        )
        self.wait(1)
        colon1, colon2 = line1, line2  # these mobjects now read as ":"

        # =============================================
        # Step 5: slide the two ratios together so their shared
        # "4 cats" term overlaps, forming "8 dogs : 4 cats : 3 hamsters"
        # =============================================
        shift2 = den1.get_center() - num2.get_center()
        self.play(VGroup(num2, colon2, den2).animate.shift(shift2))
        self.wait(0.5)
        self.play(FadeOut(num2))  # duplicate "4 cats" removed; den1 remains as the shared term
        self.wait(1)

        # =============================================
        # Step 6: fade away the animal words, then close the gaps
        # to leave the bare ratio "8 : 4 : 3"
        # =============================================
        self.play(
            FadeOut(num1[1:]), FadeOut(den1[1:]), FadeOut(den2[1:]),
        )
        self.wait(0.3)

        visible_now = VGroup(num1[0], colon1, den1[0], colon2, den2[0])
        targets = VGroup(
            Text("8", font=FONT, font_size=FS, color=WHITE),
            Text(":", font=FONT, font_size=FS, color=WHITE),
            Text("4", font=FONT, font_size=FS, color=WHITE),
            Text(":", font=FONT, font_size=FS, color=WHITE),
            Text("3", font=FONT, font_size=FS, color=WHITE),
        ).arrange(RIGHT, buff=0.3).move_to(visible_now.get_center())

        self.play(
            num1[0].animate.move_to(targets[0].get_center()),
            colon1.animate.move_to(targets[1].get_center()),
            den1[0].animate.move_to(targets[2].get_center()),
            colon2.animate.move_to(targets[3].get_center()),
            den2[0].animate.move_to(targets[4].get_center()),
        )
        self.wait(2)
