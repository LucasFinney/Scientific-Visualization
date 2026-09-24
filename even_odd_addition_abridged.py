import os
import sys

from manim import *

# Abridged cut of the addition & subtraction slide from even_odd_rules.py:
# each rule is stated and shown with its worked example, without the general
# algebraic (2A + 2B ...) derivations.
#   manim -p even_odd_addition_abridged.py EvenOddAdditionAbridged
# With no quality flag this renders at 4K/60fps. Pass -ql for a fast preview.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from even_odd_rules import ParityScene, MAIN_X, DOT_Y, NUM_Y, HILITE, EVEN_C, ODD_C


class EvenOddAdditionAbridged(ParityScene):
    def construct(self):
        self.setup_scene()
        self.intro()
        self.show_sidebar("Adding & Subtracting")
        self.even_plus_even()
        self.odd_plus_odd()
        self.even_plus_odd()
        self.even_minus_odd()
        self.even_minus_even()
        self.clear_stage()
        self.play(LaggedStart(*[Indicate(r, color=HILITE, scale_factor=1.1)
                                for r in self.rules], lag_ratio=0.2))
        self.wait(2)

    # -----------------------------------------------------------------
    def mystery_box(self):
        box = RoundedRectangle(corner_radius=0.12, width=1.7, height=1.2,
                               stroke_color=GREY_B, stroke_width=3)
        box.content = self.txt("?", GREY_B, 56).move_to(box)
        return VGroup(box, box.content)

    def intro(self):
        self.script("For the GRE, you may be asked abstract questions about "
                    "whether the result of some operation is even or odd…")
        title = self.rule_text("even or odd?", fs=60).move_to(UP * 2.6)
        a, b, r = [self.mystery_box() for _ in range(3)]
        op, eq = self.txt("+", fs=64), self.txt("=", fs=64)
        row = VGroup(a, op, b, eq, r).arrange(RIGHT, buff=0.5).move_to(UP * 0.4)
        tags = [self.chip("even").next_to(a, DOWN, buff=0.3),
                self.chip("odd").next_to(b, DOWN, buff=0.3),
                self.chip("?").next_to(r, DOWN, buff=0.3)]
        self.play(Write(title))
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.3) for m in row],
                              lag_ratio=0.15))
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tags],
                              lag_ratio=0.2))

        self.script("…without knowing the individual values you’re "
                    "working with.")
        self.play(*[Wiggle(m[1]) for m in (a, b, r)])
        self.wait(0.5)

        self.script("Thankfully, you don’t need to know the values in "
                    "addition or multiplication to identify if the result will "
                    "be even or odd!")

        def cycle(pairs, f):
            for x, y in pairs:
                self.play(*[Transform(m[1], self.txt(str(v), WHITE, 48)
                                      .move_to(m[0]))
                            for m, v in ((a, x), (b, y), (r, f(x, y)))],
                          run_time=0.45)
                self.wait(0.3)

        self.play(Transform(tags[2], self.chip("odd").move_to(tags[2])),
                  Flash(tags[2], color=ODD_C))
        cycle([(4, 7), (10, 3), (36, 15), (128, 9)], lambda x, y: x + y)
        self.play(Transform(op, self.txt("×", fs=64).move_to(op)),
                  Transform(tags[2], self.chip("even").move_to(tags[2])),
                  Flash(tags[2], color=EVEN_C))
        cycle([(4, 7), (10, 3), (36, 15), (128, 9)], lambda x, y: x * y)
        self.wait(0.5)
        self.clear_stage()

    # -----------------------------------------------------------------
    def rule(self, a, op, b, result, line):
        """Write 'a op b = ?' and answer it, cued by the script line."""
        hq, head = self.heading(a, op, b, result)
        self.script(line)
        self.play(Write(hq))
        self.reveal(hq, head)
        return head

    def finish(self, head):
        self.wait(1)
        self.clear_stage(keep=[head])
        self.promote(head)

    def add_example(self, x, y, note_text, flash_single=False):
        """x + y shown as dots sliding together."""
        A, B = self.dots(x), self.dots(y)
        plus = self.txt("+", fs=52)
        VGroup(A, plus, B).arrange(RIGHT, buff=0.5).move_to([MAIN_X, DOT_Y, 0])
        nA, nB = self.number_under(str(x), A), self.number_under(str(y), B)
        self.pop_in(A, B)
        self.play(FadeIn(plus), FadeIn(nA), FadeIn(nB))
        if A.single is not None and B.single is not None:
            self.play(Indicate(A.single, color=ODD_C, scale_factor=1.8),
                      Indicate(B.single, color=ODD_C, scale_factor=1.8))
        total = self.txt(str(x + y), fs=40).move_to([MAIN_X, NUM_Y, 0])
        M = self.combine(A, B, extra=[FadeOut(plus),
                                      ReplacementTransform(VGroup(nA, nB), total)])
        word = "even" if (x + y) % 2 == 0 else "odd"
        chip = self.chip(word).next_to(total, RIGHT, buff=0.3)
        note = self.txt(note_text, GREY_A, 28).next_to(M, UP, buff=0.35)
        extra = [Flash(M.single, color=ODD_C, line_length=0.2,
                       flash_radius=0.35)] if flash_single else []
        self.play(*extra, FadeIn(note), FadeIn(chip, scale=0.5))

    # -----------------------------------------------------------------
    def even_plus_even(self):
        head = self.rule("even", "+", "even", "even",
                         "If you add two even numbers together, then the "
                         "result will always be even.")
        self.script("For example, two plus four equals six.")
        self.add_example(2, 4, "every dot has a partner")
        self.finish(head)

    def odd_plus_odd(self):
        head = self.rule("odd", "+", "odd", "even",
                         "Here’s an odd one: the sum of two odd numbers will "
                         "always be even…")
        self.script("…for example, 3 plus 1 is 4.")
        self.add_example(3, 1, "the two leftovers pair up")
        self.finish(head)

    def even_plus_odd(self):
        head = self.rule("even", "+", "odd", "odd",
                         "Now the mixed pairings; an even integer plus an odd "
                         "integer gives an odd integer.")
        self.script("For example, 6 plus 3 equals 9.")
        self.add_example(6, 3, "one dot is left without a partner",
                         flash_single=True)
        self.finish(head)

    def even_minus_odd(self):
        head = self.rule("even", "−", "odd", "odd",
                         "An even number minus an odd number is odd…")
        self.script("…for example 8 minus 1 equals 7.")
        A = self.dots(8).move_to([MAIN_X, DOT_Y, 0])
        n = self.txt("8", fs=40).move_to([MAIN_X, NUM_Y, 0])
        self.pop_in(A)
        self.play(FadeIn(n))
        n2 = self.txt("8 − 1", fs=40).move_to(n)
        self.play(TransformMatchingShapes(n, n2))
        self.break_pair(A.body[-1])
        n7 = self.txt("7", fs=40).move_to(n2)
        chip = self.chip("odd").next_to(n7, RIGHT, buff=0.3)
        note = self.txt("its partner is left alone", GREY_A, 28)
        # not next_to(A): the removed dot, faded out above the row, still
        # counts toward A's bounds and would push the note into the heading
        note.move_to([MAIN_X, DOT_Y + 0.8, 0])
        self.play(ReplacementTransform(n2, n7), FadeIn(chip, scale=0.5),
                  FadeIn(note))
        self.finish(head)

    def even_minus_even(self):
        head = self.rule("even", "−", "even", "even",
                         "And lastly, an even number minus an even number is "
                         "even…")
        self.script("…for example, 16 minus 12 equals 4.")
        A = self.dots(16).move_to([MAIN_X, DOT_Y, 0])
        n = self.txt("16", fs=40).move_to([MAIN_X, NUM_Y, 0])
        self.pop_in(A)
        self.play(FadeIn(n))
        gone = VGroup(*A.body[2:])
        b12 = self.brace(gone, r"-12", direction=UP)
        n2 = self.txt("16 − 12", fs=40).move_to(n)
        self.play(GrowFromCenter(b12), TransformMatchingShapes(n, n2))
        self.play(VGroup(gone, b12).animate.shift(UP * 1.2).set_opacity(0),
                  run_time=1.2)
        self.remove(gone, b12)
        rest = list(A.body[:2])
        self.play(*self.recenter(rest))
        n4 = self.txt("4", fs=40).move_to(n2)
        chip = self.chip("even").next_to(n4, RIGHT, buff=0.3)
        note = self.txt("whole pairs leave, only pairs remain", GREY_A, 28)
        note.move_to([MAIN_X, DOT_Y + 0.8, 0])
        self.play(ReplacementTransform(n2, n4), FadeIn(chip, scale=0.5),
                  FadeIn(note))
        self.finish(head)
