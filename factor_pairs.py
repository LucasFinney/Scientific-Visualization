from math import ceil, isqrt, sqrt

from manim import *

# Factor pairs: why factors come in pairs that close in on the middle.
#
# Top: a number line from 1 to N. Two pointers start at opposite ends
# (1 and N) and walk toward each other: the left one steps through the
# trial divisors d = 1, 2, 3, ..., the right one always sits at N / d.
# Bottom: N dots regrouped into d rows. When d divides N the grid is a
# perfect rectangle, both ends light up in the pair's colour and an arc
# joins them. When it doesn't, the leftover dots turn red and the right
# pointer lands between two whole numbers. The search ends when the pointers
# meet (N is a perfect square) or cross, at the square root of N.
#
#   manim -p factor_pairs.py FactorPairs      (24, then 36)
#   manim -p factor_pairs.py FactorPairs36    (just one number)
# With no quality flag this renders at 4K/60fps. Pass -ql for a fast preview.
if config.pixel_height == 1080 and config.frame_rate == 60:  # manim's default
    config.pixel_width = 3840
    config.pixel_height = 2160

FONT = "Open Sans"

DOT_C = "#E6E8EB"
DIM_C = "#5A6068"
NO_C = "#E5484D"
PAIR_COLORS = ["#4C8DF6", "#F5A524", "#2EC27E", "#C678DD", "#56B6C2",
               "#E8D44D", "#FF7AB6"]

X0, X1 = -6.2, 6.2   # ends of the number line
LINE_Y = 1.1
LABEL_Y = LINE_Y - 0.38
PTR_Y = LINE_Y + 0.32
ARC_ANGLE = -0.36 * PI  # negative: arcs bow upward

GRID_Y = -1.6        # centre of the dot grid
DOT_R = 0.09


def txt(s, color=WHITE, fs=30):
    return Text(s, font=FONT, font_size=fs, color=color)


class FactorPairs(Scene):
    NUMBERS = [24, 36]

    def construct(self):
        self.camera.background_color = BLACK
        for n in self.NUMBERS:
            self.factor(n)

    # ------------------------------------------------------------ layout
    def xpt(self, v):
        """Point on the number line for (possibly fractional) value v."""
        x = X0 + (v - 1) * (X1 - X0) / (self.N - 1)
        return np.array([x, LINE_Y, 0])

    def grid_positions(self, d):
        """N dots filled column by column into columns of height d."""
        cols = ceil(self.N / d)
        s = self.S
        ox = -(cols - 1) * s / 2
        oy = GRID_Y + (d - 1) * s / 2
        return [np.array([ox + (i // d) * s, oy - (i % d) * s, 0])
                for i in range(self.N)]

    def label(self, v):
        """Tick label for v, created on first use."""
        if v not in self.labels:
            lab = txt(str(v), fs=24).move_to([self.xpt(v)[0], LABEL_Y, 0])
            self.labels[v] = lab
        return self.labels[v]

    def pointer(self):
        return (Triangle(color=WHITE, fill_opacity=1, stroke_width=0)
                .rotate(PI).scale(0.12))

    # ------------------------------------------------------------ story
    def factor(self, N):
        self.N = N
        self.S = min(0.36, (X1 - X0) / (N - 1))
        self.labels = {}
        self.pairs = []
        self.side = VGroup()

        # The number, then its dots and the line from 1 to N.
        big = txt(str(N), fs=140)
        self.play(FadeIn(big, scale=0.6))
        self.wait(0.4)

        line = Line(self.xpt(1), self.xpt(N), color=GREY_B, stroke_width=3)
        ticks = VGroup(*[
            Line(UP * h, DOWN * h, color=GREY_B, stroke_width=2)
            .move_to(self.xpt(v))
            for v in range(1, N + 1)
            for h in [0.14 if v in (1, N) else 0.08]])
        self.dots = VGroup(*[Dot(radius=DOT_R, color=DOT_C)
                             for _ in range(N)])
        for dot, p in zip(self.dots, self.grid_positions(1)):
            dot.move_to(p)

        self.play(Create(line), LaggedStart(*[Create(t) for t in ticks],
                                            lag_ratio=0.03),
                  FadeIn(self.label(1)),
                  ReplacementTransform(big, self.label(N)),
                  run_time=1.3)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in self.dots],
                              lag_ratio=0.04), run_time=1.2)

        self.lp = self.pointer().move_to([self.xpt(1)[0], PTR_Y, 0])
        self.rp = self.pointer().move_to([self.xpt(N)[0], PTR_Y, 0])
        self.play(FadeIn(self.lp, shift=DOWN * 0.2),
                  FadeIn(self.rp, shift=DOWN * 0.2))

        d = 1
        while d * d <= N:
            self.try_divisor(d)
            d += 1
        root = isqrt(N)
        if root * root == N:
            self.meet(root)
        else:
            self.cross(d)
        self.show_root()
        self.gallery()

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.4)

    def move_pointers(self, d):
        return [self.lp.animate.move_to([self.xpt(d)[0], PTR_Y, 0])
                .set_color(WHITE),
                self.rp.animate.move_to([self.xpt(self.N / d)[0], PTR_Y, 0])
                .set_color(WHITE)]

    def try_divisor(self, d):
        N = self.N
        lab = self.label(d)
        anims = self.move_pointers(d)
        anims.append(FadeOut(self.side))
        if lab not in self.mobjects:
            anims.append(FadeIn(lab, shift=UP * 0.15))
        for dot, p in zip(self.dots, self.grid_positions(d)):
            anims.append(dot.animate.move_to(p).set_color(DOT_C))
        self.play(*anims, run_time=1.3)

        rows = txt(str(d), fs=30)
        grid = self.dots
        if N % d:
            # Leftovers: the dots don't make a rectangle.
            left = VGroup(*self.dots[N - N % d:])
            rows.set_color(DIM_C).next_to(grid, LEFT, buff=0.35)
            self.side = VGroup(rows)
            self.play(left.animate.set_color(NO_C), self.rp.animate
                      .set_color(NO_C), FadeIn(rows))
            self.play(Wiggle(left, scale_value=1.3), run_time=0.8)
            self.play(lab.animate.set_color(DIM_C), run_time=0.4)
            self.wait(0.3)
            return

        # A perfect rectangle: d and N/d are a factor pair.
        c = PAIR_COLORS[len(self.pairs) % len(PAIR_COLORS)]
        e = N // d
        partner = self.label(e)
        cols = txt(str(e), fs=30)
        rows.set_color(c).next_to(grid, LEFT, buff=0.35)
        cols.set_color(c).next_to(grid, DOWN, buff=0.3)
        self.side = VGroup(rows, cols)

        anims = [grid.animate.set_color(c), lab.animate.set_color(c),
                 self.lp.animate.set_color(c), self.rp.animate.set_color(c),
                 FadeIn(rows), FadeIn(cols)]
        if partner in self.mobjects:
            anims.append(partner.animate.set_color(c))
        else:
            anims.append(FadeIn(partner.set_color(c), shift=UP * 0.15))
        self.play(*anims)

        if e != d:
            arc = ArcBetweenPoints(self.xpt(d) + UP * 0.14,
                                   self.xpt(e) + UP * 0.14,
                                   angle=ARC_ANGLE, color=c, stroke_width=5)
            self.play(Create(arc), run_time=0.9)
        else:
            arc = Dot(self.xpt(d) + UP * 0.14, radius=0.07, color=c)
            self.play(FadeIn(arc, scale=3))
        self.pairs.append((d, e, c, arc))
        self.wait(0.6)

    def meet(self, r):
        """Square: both pointers landed on the same tick."""
        self.play(Flash(self.lp, color=self.pairs[-1][2], flash_radius=0.4,
                        line_length=0.25), run_time=1)
        self.wait(0.3)

    def cross(self, d):
        """Next trial divisor puts the pointers past each other."""
        lab = self.label(d)
        self.play(*self.move_pointers(d), FadeOut(self.side),
                  FadeIn(lab, shift=UP * 0.15), run_time=1.3)
        self.side = VGroup()
        self.play(self.lp.animate.set_color(NO_C),
                  self.rp.animate.set_color(NO_C))
        self.play(Wiggle(VGroup(self.lp, self.rp), scale_value=1.4),
                  run_time=0.9)
        self.play(FadeOut(lab), run_time=0.4)

    def show_root(self):
        """The pointers can't pass the square root: that's the middle."""
        x = self.xpt(sqrt(self.N))[0]
        mark = DashedLine([x, LINE_Y - 0.2, 0], [x, LINE_Y + 2.2, 0],
                          color=GREY_B, dash_length=0.08, stroke_width=2)
        root = txt(f"√{self.N}", GREY_B, 24).next_to(mark, UP, buff=0.1)
        self.play(FadeOut(self.side), FadeOut(self.lp), FadeOut(self.rp),
                  Create(mark), FadeIn(root))
        self.side = VGroup()
        # Every factor, pair by pair from the outside in.
        for d, e, c, arc in self.pairs:
            labs = VGroup(self.label(d), self.label(e))
            self.play(Indicate(labs, color=c, scale_factor=1.5),
                      arc.animate.set_stroke(width=8), run_time=0.6)
            self.play(arc.animate.set_stroke(width=5), run_time=0.2)

    def gallery(self):
        """Each pair's rectangle, side by side, in the pair's colour."""
        thumbs = VGroup()
        for d, e, c, _ in self.pairs:
            thumbs.add(VGroup(*[Square(1, stroke_width=0, fill_color=c,
                                       fill_opacity=1)
                                .move_to([j * 1.15, -i * 1.15, 0])
                                for i in range(d) for j in range(e)]))
        thumbs.arrange(RIGHT, buff=2.2, aligned_edge=UP)
        thumbs.scale_to_fit_width(X1 - X0)
        if thumbs.height > 2.4:
            thumbs.scale_to_fit_height(2.4)
        thumbs.move_to([0, GRID_Y, 0])

        self.play(self.dots.animate.set_opacity(0).scale(0.6), run_time=0.6)
        self.remove(self.dots)
        self.play(LaggedStart(*[
            AnimationGroup(Indicate(arc, color=c, scale_factor=1.05),
                           FadeIn(t, shift=UP * 0.3))
            for t, (_, _, c, arc) in zip(thumbs, self.pairs)],
            lag_ratio=0.6), run_time=0.9 * len(self.pairs))


class FactorPairs36(FactorPairs):
    NUMBERS = [36]
