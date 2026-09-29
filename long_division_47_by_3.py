from manim import *

# Long division of 47 by 3, one digit at a time.
#   manim -pql long_division_47_by_3.py LongDivision
# Use -qh (or -qk) for a final render.

FONT = "Consolas"
FS = 56
COL = [0.0, 0.75]                      # x of the tens and ones columns
ROW = {"q": 2.0, "n": 1.1, "p1": 0.2, "d1": -0.7, "p2": -1.6, "d2": -2.5}
HI = YELLOW_D                          # the digit being worked on
OUT = GREEN_C                          # finished quotient / remainder
DIM = GREY_B


def digit(ch, col, row, color=WHITE):
    return Text(ch, font=FONT, font_size=FS, color=color).move_to(
        [COL[col], ROW[row], 0])


def rule(row, c0, c1):
    """Horizontal line just under `row`, spanning columns c0..c1."""
    y = ROW[row] - 0.45
    return Line([COL[c0] - 0.4, y, 0], [COL[c1] + 0.4, y, 0],
                stroke_width=3, color=DIM)


class LongDivision(Scene):
    def construct(self):
        # --- setup: 3 ) 47 ---------------------------------------------
        top = ROW["n"] + 0.5
        bracket = VGroup(
            Line([-0.65, top, 0], [-0.65, ROW["n"] - 0.5, 0]),
            Line([-0.65, top, 0], [COL[1] + 0.45, top, 0]),
        ).set_stroke(DIM, 3)
        divisor = digit("3", 0, "n").set_x(-1.25)
        n4, n7 = digit("4", 0, "n"), digit("7", 1, "n")
        self.play(Create(bracket), FadeIn(divisor), FadeIn(n4), FadeIn(n7))
        self.wait(0.6)

        # --- step 1: 3 into 4 goes once --------------------------------
        self.play(divisor.animate.set_color(HI), n4.animate.set_color(HI))
        q1 = digit("1", 0, "q", HI)
        self.play(FadeIn(q1, shift=DOWN * 0.3))
        self.wait(0.4)

        p1 = digit("3", 0, "p1", HI)
        self.play(TransformFromCopy(divisor, p1))
        line1 = rule("p1", 0, 0)
        self.play(Create(line1))
        d1 = digit("1", 0, "d1", HI)
        self.play(FadeIn(d1, shift=UP * 0.2))
        self.play(*[m.animate.set_color(WHITE) for m in (divisor, n4, q1, p1, d1)])
        self.wait(0.4)

        # --- step 2: bring down the 7 ----------------------------------
        b7 = digit("7", 1, "d1", HI)
        self.play(n7.animate.set_color(HI),
                  TransformFromCopy(n7, b7))
        self.play(n7.animate.set_color(WHITE))
        self.wait(0.4)
        r17 = VGroup(d1, b7)
        self.play(r17.animate.set_color(HI))
        self.wait(0.3)

        # --- step 3: 3 into 17 goes 5 times ----------------------------
        q2 = digit("5", 1, "q", HI)
        self.play(divisor.animate.set_color(HI), FadeIn(q2, shift=DOWN * 0.3))
        self.wait(0.4)

        p2 = VGroup(digit("1", 0, "p2", HI), digit("5", 1, "p2", HI))
        self.play(TransformFromCopy(divisor, p2))
        line2 = rule("p2", 0, 1)
        self.play(Create(line2))
        rem = digit("2", 1, "d2", HI)
        self.play(FadeIn(rem, shift=UP * 0.2))
        self.wait(0.4)

        # --- result: 15 remainder 2 ------------------------------------
        self.play(*[m.animate.set_color(WHITE) for m in (divisor, r17, p2)])
        self.play(q1.animate.set_color(OUT), q2.animate.set_color(OUT),
                  rem.animate.set_color(OUT))
        self.wait(0.4)

        result = Text("47 = 3 × 15 + 2", font=FONT, font_size=40, color=DIM)
        result.move_to([0, -3.5, 0])
        self.play(FadeIn(result, shift=UP * 0.2))
        self.wait(2)
