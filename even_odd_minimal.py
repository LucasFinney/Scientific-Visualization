import os
import sys

from manim import *

# Minimalist cut of the abridged addition & subtraction animation: only the
# dot pictures of each worked example, centred on screen. The only text is
# the number labels and the EVEN/ODD chip that ends each example (no
# headings, equations, notes, sidebar or script cues).
#   manim -p even_odd_minimal.py EvenOddMinimal
# With no quality flag this renders at 4K/60fps. Pass -ql for a fast preview.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from even_odd_rules import ParityScene, NO_C, ODD_C

DOT_Y = 0.0            # dots sit on the centre line of the frame
NUM_Y = DOT_Y - 1.1    # number labels under the dots
CHIP_Y = NUM_Y - 0.8   # EVEN/ODD chip under the result


class EvenOddMinimal(ParityScene):
    def construct(self):
        self.setup_scene()
        self.add_example(2, 4)
        self.add_example(3, 1)
        self.add_example(6, 3, flash_single=True)
        self.minus_one(8)
        self.minus_pairs(16, 12)

    # -----------------------------------------------------------------
    def column_xs(self, n, x=0):
        return super().column_xs(n, x)

    def number(self, s, x=0):
        return self.txt(s, fs=40).move_to([x, NUM_Y, 0])

    def conclude(self, label, value):
        """Swap the label for the result and show its EVEN/ODD chip."""
        word = "even" if value % 2 == 0 else "odd"
        result = self.number(str(value))
        chip = self.chip(word).move_to([0, CHIP_Y, 0])
        self.play(ReplacementTransform(label, result), FadeIn(chip, scale=0.5))

    def end_example(self):
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
        self.wait(0.3)

    # -----------------------------------------------------------------
    def add_example(self, x, y, flash_single=False):
        """x and y as dot groups that slide together."""
        A, B = self.dots(x), self.dots(y)
        VGroup(A, B).arrange(RIGHT, buff=1.0).move_to([0, DOT_Y, 0])
        nA, nB = self.number(str(x), A.get_x()), self.number(str(y), B.get_x())
        self.pop_in(A, B)
        self.play(FadeIn(nA), FadeIn(nB))
        if A.single is not None and B.single is not None:
            self.play(Indicate(A.single, color=ODD_C, scale_factor=1.8),
                      Indicate(B.single, color=ODD_C, scale_factor=1.8))
        label = self.number(str(x + y))
        M = self.combine(A, B, extra=[ReplacementTransform(VGroup(nA, nB),
                                                           label)], y=DOT_Y)
        if flash_single:
            self.play(Flash(M.single, color=ODD_C, line_length=0.2,
                            flash_radius=0.35))
        self.conclude(label, x + y)
        self.end_example()

    def minus_one(self, n):
        """n dots; one dot of the last pair leaves, its partner is alone."""
        A = self.dots(n).move_to([0, DOT_Y, 0])
        label = self.number(str(n))
        self.pop_in(A)
        self.play(FadeIn(label))
        cap, top, bot = A.body[-1]
        tag = self.txt("−1", NO_C, 32).next_to(top, UP, buff=0.25)
        self.play(FadeIn(tag, shift=DOWN * 0.2), top.animate.set_color(NO_C))
        self.play(VGroup(top, tag).animate.shift(UP * 0.9).set_opacity(0),
                  run_time=1)
        self.remove(top, tag)
        ghost = self.ghost().move_to(top)
        self.play(FadeOut(cap), bot.animate.set_color(ODD_C), Create(ghost),
                  run_time=0.8)
        self.play(Flash(bot, color=ODD_C, line_length=0.2, flash_radius=0.35))
        self.conclude(label, n - 1)
        self.end_example()

    def minus_pairs(self, n, m):
        """n dots; m of them leave as whole pairs, only pairs remain."""
        A = self.dots(n).move_to([0, DOT_Y, 0])
        label = self.number(str(n))
        self.pop_in(A)
        self.play(FadeIn(label))
        k = (n - m) // 2
        gone = VGroup(*A.body[k:])
        b = self.brace(gone, rf"-{m}", direction=UP)
        self.play(GrowFromCenter(b))
        self.play(VGroup(gone, b).animate.shift(UP * 1.2).set_opacity(0),
                  run_time=1.2)
        self.remove(gone, b)
        self.play(*self.recenter(list(A.body[:k]), y=DOT_Y))
        self.conclude(label, n - m)
        self.end_example()
