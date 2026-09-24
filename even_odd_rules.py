from manim import *
import textwrap

# Two scenes, matching the two slides of the "Even and Odd" script:
#   manim -p even_odd_rules.py EvenOddAddition        (addition & subtraction)
#   manim -p even_odd_rules.py EvenOddMultiplication  (slide 9: multiplication)
# With no quality flag this renders at 4K/60fps. Pass -ql for a fast preview.
if config.pixel_height == 1080 and config.frame_rate == 60:  # manim's default
    config.pixel_width = 3840
    config.pixel_height = 2160

FONT = "Open Sans"

EVEN_C = "#4C8DF6"   # evenness: pairs, factors of 2
ODD_C = "#F5A524"    # oddness: the leftover dot, the "+1"
DOT_C = "#E6E8EB"
NO_C = "#E5484D"
PANEL_C = "#0E1116"
HILITE = YELLOW

MAIN_X = 1.7         # centre of the main stage (the rules sidebar sits left)
SIDE_X = -5.25       # centre of the rules sidebar
HEAD_Y = 3.3
DOT_Y = 1.5          # row of dots
NUM_Y = DOT_Y - 1.1  # numbers / brace labels under the dots
EQ1_Y = -1.0         # first line of algebra
EQ2_Y = -1.85        # second line of algebra

COL = 0.68           # spacing between columns of dots
DOT_R = 0.17
ROW_GAP = 0.56       # vertical distance between the two dots of a pair
CAP_W = 2 * DOT_R + 0.18  # width of a pair's capsule

CUE_W = 4.9          # script box: fixed width...
CUE_LINES = 3        # ...and fixed height, in lines of text

PARITY_COLORS = {"even": EVEN_C, "odd": ODD_C}


class Block(VGroup):
    """A number drawn as columns of dots.

    Each even part is a column of two dots in a blue capsule (a "pair").
    An odd number has one extra column: a lone orange dot with a dashed
    ghost where its missing partner would be. Columns may also be an
    ellipsis, for "some unknown number of pairs".
    """

    def __init__(self, items, single=None, ghost=None, layout=True):
        super().__init__()
        self.body = VGroup(*items)
        self.single, self.ghost = single, ghost
        if layout:
            for i, it in enumerate(items):
                it.move_to(RIGHT * i * COL)
            if single is not None:
                x = len(items) * COL
                single.move_to([x, ROW_GAP / 2, 0])
                ghost.move_to([x, -ROW_GAP / 2, 0])
        self.add(self.body)
        if single is not None:
            self.add(ghost, single)

    @property
    def pairs(self):
        return [it for it in self.body if getattr(it, "is_pair", False)]


class ParityScene(Scene):
    # ------------------------------------------------------------ text
    def txt(self, s, color=WHITE, fs=40, **kw):
        return Text(s, font=FONT, font_size=fs, color=color, **kw)

    def rule_text(self, s, fs=46):
        """Text with every 'even'/'odd' coloured by parity."""
        return self.txt(s, fs=fs, t2c={"even": EVEN_C, "odd": ODD_C})

    def mt(self, *parts, fs=52):
        """MathTex where a lone 2 is blue (pairs) and a lone 1 is orange."""
        m = MathTex(*parts, font_size=fs)
        for p in m:
            s = p.get_tex_string().strip()
            if s == "2":
                p.set_color(EVEN_C)
            elif s == "1":
                p.set_color(ODD_C)
        return m

    def implies(self, left, right, fs=46):
        """'left => right' with parity words coloured."""
        # Set it as one Text (so the baselines agree), then swap the "="
        # for a TeX arrow, since Open Sans has no arrow glyphs.
        row = self.rule_text(f"{left} = {right}", fs)
        i = len(left.replace(" ", ""))
        arrow = MathTex(r"\Rightarrow", font_size=fs * 1.2).move_to(row[i])
        row.submobjects[i] = arrow
        VGroup(*row[:i]).shift(LEFT * 0.12)
        VGroup(*row[i + 1:]).shift(RIGHT * 0.12)
        return row

    def chip(self, word, color=None, fs=26):
        color = color or PARITY_COLORS.get(word, GREY_C)
        label = self.txt(word.upper(), BLACK, fs, weight=BOLD)
        box = RoundedRectangle(corner_radius=0.1, width=label.width + 0.4,
                               height=label.height + 0.26, fill_color=color,
                               fill_opacity=1, stroke_width=0)
        return VGroup(box, label.move_to(box))

    def brace(self, mob, label, direction=DOWN, color=GREY_A, fs=42):
        b = Brace(mob, direction, buff=0.1, color=GREY_B)
        lab = label if isinstance(label, Mobject) else \
            MathTex(label, font_size=fs, color=color)
        b.put_at_tip(lab, buff=0.12)
        return VGroup(b, lab)

    # ------------------------------------------------------------ script cue
    def script(self, s, wait=0.3):
        """Bottom-right box quoting the script line this animation matches.

        The box is always the same size (easy to mask out in editing); text
        that doesn't fit in CUE_LINES lines is simply cut off."""
        inner_w = CUE_W - 0.3
        lines = []
        for line in textwrap.wrap(f"“{s}”", 42)[:CUE_LINES]:
            while line and self.txt(line, fs=17).width > inner_w:
                line = line[:-1]
            lines.append(line)
        body = self.txt("\n".join(lines), GREY_A, 17, line_spacing=0.9)
        tag = self.txt("SCRIPT", GREY_B, 12, weight=BOLD)
        # size the box for a full CUE_LINES of text, whatever this cue holds
        full = self.txt("\n".join(["Ag"] * CUE_LINES), fs=17, line_spacing=0.9)
        box = RoundedRectangle(corner_radius=0.08, width=CUE_W,
                               height=tag.height + 0.08 + full.height + 0.26,
                               fill_color=PANEL_C, fill_opacity=0.92,
                               stroke_color=GREY_D, stroke_width=2)
        box.to_corner(DR, buff=0.15)
        tag.move_to(box.get_corner(UL) + [0.15, -0.13, 0], aligned_edge=UL)
        body.next_to(tag, DOWN, buff=0.08, aligned_edge=LEFT)
        new = VGroup(box, tag, body)
        if self.cue is None:
            self.play(FadeIn(new), run_time=0.4)
        else:
            self.play(FadeOut(self.cue), FadeIn(new), run_time=0.4)
        self.cue = new
        if wait:
            self.wait(wait)

    # ------------------------------------------------------------ sidebar
    def show_sidebar(self, title):
        panel = RoundedRectangle(corner_radius=0.15, width=3.5, height=6.6,
                                 fill_color=PANEL_C, fill_opacity=1,
                                 stroke_color=GREY_D, stroke_width=2)
        panel.move_to([SIDE_X, 0.35, 0])
        t = self.txt(title, GREY_A, 24).move_to([SIDE_X, 3.3, 0])
        rule = Line(LEFT * 1.5, RIGHT * 1.5, color=GREY_D, stroke_width=2)
        rule.move_to([SIDE_X, 2.98, 0])
        self.sidebar = VGroup(panel, t, rule)
        self.rules = []
        self.play(FadeIn(self.sidebar, shift=RIGHT * 0.3))

    def promote(self, heading, target=None):
        """Shrink the finished heading into the next slot of the sidebar."""
        target = target or heading.copy()
        target.scale(0.58)
        if target.width > 3.0:
            target.scale_to_fit_width(3.0)
        y = 2.55 - 0.62 * len(self.rules)
        target.move_to([SIDE_X - 1.5, y, 0], aligned_edge=LEFT)
        self.play(ReplacementTransform(heading, target), run_time=1.2)
        self.rules.append(target)
        self.wait(0.3)

    def clear_stage(self, keep=()):
        keep = {self.cue, getattr(self, "sidebar", None),
                *getattr(self, "rules", []), *keep}
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.7)

    # ------------------------------------------------------------ headings
    def heading(self, a, op, b, result):
        """'a op b = ?' plus its answered form 'a op b = result'."""
        q = self.rule_text(f"{a} {op} {b} = ?").move_to([MAIN_X, HEAD_Y, 0])
        full = self.rule_text(f"{a} {op} {b} = {result}")
        full.move_to([MAIN_X, HEAD_Y, 0])
        return q, full

    def reveal(self, q, full):
        n = len(q) - 1
        stem, answer = full[:n], full[n:]
        self.play(ReplacementTransform(q[:n], stem),
                  ReplacementTransform(q[n:], answer), run_time=0.8)
        self.remove(stem, answer)
        self.add(full)
        self.play(Indicate(full[n:], color=HILITE, scale_factor=1.25))

    # ------------------------------------------------------------ dots
    def capsule(self):
        return RoundedRectangle(corner_radius=CAP_W / 2, width=CAP_W,
                                height=ROW_GAP + CAP_W, stroke_color=EVEN_C,
                                stroke_width=3, fill_color=EVEN_C,
                                fill_opacity=0.15)

    def pair(self):
        top = Dot(UP * ROW_GAP / 2, radius=DOT_R, color=DOT_C)
        bot = Dot(DOWN * ROW_GAP / 2, radius=DOT_R, color=DOT_C)
        p = VGroup(self.capsule(), top, bot)
        p.is_pair = True
        return p

    def lone(self):
        return Dot(radius=DOT_R, color=ODD_C)

    def ghost(self):
        return DashedVMobject(Circle(radius=DOT_R, color=ODD_C,
                                     stroke_width=2.5), num_dashes=8)

    def ellipsis(self):
        return MathTex(r"\cdots", color=GREY_B, font_size=60)

    def dots(self, n):
        """Concrete number n as pairs (+ one lone dot if n is odd)."""
        items = [self.pair() for _ in range(n // 2)]
        if n % 2:
            return Block(items, self.lone(), self.ghost())
        return Block(items)

    def gen(self, code, odd=False):
        """Generic number: 'p' = a pair, 'e' = an ellipsis of more pairs."""
        items = [self.pair() if c == "p" else self.ellipsis() for c in code]
        if odd:
            return Block(items, self.lone(), self.ghost())
        return Block(items)

    def pop_in(self, *blocks, run_time=1.2):
        mobs = []
        for b in blocks:
            mobs += [*b.body] + ([b.ghost, b.single] if b.single else [])
        self.play(LaggedStart(*[FadeIn(m, scale=0.4) for m in mobs],
                              lag_ratio=0.08, run_time=run_time))
        self.remove(*mobs)
        self.add(*blocks)

    def column_xs(self, n, x=MAIN_X):
        return [x + (i - (n - 1) / 2) * COL for i in range(n)]

    def combine(self, A, B, extra=(), y=DOT_Y):
        """Slide B's columns up against A's; two lone dots pair up."""
        items = [*A.body, *B.body]
        singles = [blk for blk in (A, B) if blk.single is not None]
        xs = self.column_xs(len(items) + (1 if singles else 0))
        anims = [it.animate.move_to([xs[i], y, 0]) for i, it in enumerate(items)]
        single = ghost = None
        top = [xs[-1], y + ROW_GAP / 2, 0]
        bot = [xs[-1], y - ROW_GAP / 2, 0]
        if len(singles) == 2:
            a, b = singles
            anims += [a.single.animate(path_arc=-PI / 3).move_to(top),
                      b.single.animate(path_arc=PI / 3).move_to(bot),
                      FadeOut(a.ghost), FadeOut(b.ghost)]
        elif singles:
            single, ghost = singles[0].single, singles[0].ghost
            anims += [single.animate.move_to(top), ghost.animate.move_to(bot)]
        self.play(*anims, *extra, run_time=1.6)
        if len(singles) == 2:
            cap = self.capsule().move_to([xs[-1], y, 0])
            self.play(a.single.animate.set_color(DOT_C),
                      b.single.animate.set_color(DOT_C),
                      Create(cap),
                      Flash(cap, color=HILITE, line_length=0.25,
                            flash_radius=0.55))
            new_pair = VGroup(cap, a.single, b.single)
            new_pair.is_pair = True
            items.append(new_pair)
            self.remove(cap)
        self.remove(A, B)
        merged = Block(items, single, ghost, layout=False)
        self.add(merged)
        return merged

    def recenter(self, items, y=DOT_Y):
        xs = self.column_xs(len(items))
        return [it.animate.move_to([xs[i], y, 0]) for i, it in enumerate(items)]

    def break_pair(self, p):
        """Take the top dot out of pair p; its partner is left alone."""
        cap, top, bot = p
        ghost = self.ghost().move_to(top)
        self.play(top.animate.set_color(NO_C).shift(UP * 0.9).set_opacity(0),
                  run_time=1)
        self.play(FadeOut(cap), bot.animate.set_color(ODD_C), Create(ghost),
                  run_time=0.8)
        self.play(Flash(bot, color=ODD_C, line_length=0.2, flash_radius=0.35))
        return ghost

    def number_under(self, s, mob, color=WHITE):
        return self.txt(s, color, 40).move_to([mob.get_x(), NUM_Y, 0])

    # ------------------------------------------------------------ algebra
    def grow_eq(self, eq, mapping, new=(), src=None, run_time=1.5):
        """Build parts of eq from copies of parts already on screen.

        mapping: list of (index or tuple of indices into src, index into eq);
        src defaults to eq itself (extending a line)."""
        src = eq if src is None else src
        anims = []
        for srcs, dst in mapping:
            srcs = srcs if isinstance(srcs, tuple) else (srcs,)
            anims.append(ReplacementTransform(
                VGroup(*[src[i].copy() for i in srcs]), eq[dst]))
        anims += [FadeIn(eq[i]) for i in new]
        self.play(*anims, run_time=run_time)

    def morph_eq(self, src, dst, mapping, run_time=1.5):
        """Rewrite src into dst, moving the mapped parts."""
        anims, used_src, used_dst = [], set(), set()
        for srcs, d in mapping:
            srcs = srcs if isinstance(srcs, tuple) else (srcs,)
            anims.append(ReplacementTransform(
                VGroup(*[src[i] for i in srcs]), dst[d]))
            used_src.update(srcs)
            used_dst.add(d)
        anims += [FadeOut(src[i]) for i in range(len(src)) if i not in used_src]
        anims += [FadeIn(dst[i]) for i in range(len(dst)) if i not in used_dst]
        self.play(*anims, run_time=run_time)

    def eq_line(self, *parts, y=EQ1_Y):
        return self.mt(*parts).move_to([MAIN_X, y, 0])

    # ------------------------------------------------------------ bubbles
    def token(self, p):
        is_two = p == 2
        c = Circle(radius=0.3, fill_color=EVEN_C if is_two else "#4A515C",
                   fill_opacity=1, stroke_color=WHITE if is_two else GREY_B,
                   stroke_width=2)
        t = self.txt(str(p), WHITE, 28, weight=BOLD).move_to(c)
        return VGroup(c, t)

    def bubble(self, n, primes, min_r=0.75, fs=44):
        """A number as a circle holding the prime factors it 'brings'."""
        toks = VGroup(*[self.token(p) for p in primes])
        if len(primes) <= 3:
            toks.arrange(RIGHT, buff=0.08)
        else:
            toks.arrange_in_grid(rows=2, buff=0.08)
        r = max(min_r, np.hypot(toks.width / 2, toks.height / 2) + 0.14)
        circ = Circle(radius=r, stroke_color=GREY_B, stroke_width=3,
                      fill_color="#15181D", fill_opacity=1)
        toks.move_to(circ)
        label = self.txt(str(n), WHITE, fs).next_to(circ, UP, buff=0.15)
        b = VGroup(circ, toks, label)
        b.circ, b.toks, b.label = circ, toks, label
        b.twos = VGroup(*[t for t, p in zip(toks, primes) if p == 2])
        return b

    def show_bubbles(self, *bubbles):
        self.play(LaggedStart(*[
            AnimationGroup(GrowFromCenter(b.circ), FadeIn(b.label),
                           LaggedStart(*[GrowFromCenter(t) for t in b.toks],
                                       lag_ratio=0.2))
            for b in bubbles], lag_ratio=0.3))

    def gather(self, factors, prod, run_time=2):
        """Every factor sends copies of its primes into the product."""
        q = self.txt("?", GREY_B, 40).move_to(prod.label)
        self.play(GrowFromCenter(prod.circ), FadeIn(q))
        srcs = [t for f in factors for t in f.toks]
        self.play(LaggedStart(*[
            TransformFromCopy(s, d, path_arc=-PI / 4)
            for s, d in zip(srcs, prod.toks)], lag_ratio=0.25),
            run_time=run_time)
        self.play(ReplacementTransform(q, prod.label))

    def verdict(self, mob, text, ok):
        """A small ✓/✗ note under mob."""
        mark = MathTex(r"\checkmark" if ok else r"\boldsymbol{\times}",
                       color=EVEN_C if ok else NO_C, font_size=40)
        note = self.txt(text, GREY_A, 24)
        return VGroup(mark, note).arrange(RIGHT, buff=0.12)\
            .next_to(mob, DOWN, buff=0.25)

    def setup_scene(self):
        self.camera.background_color = BLACK
        self.cue = None


# =====================================================================
# Slide 1: addition & subtraction
# =====================================================================
class EvenOddAddition(ParityScene):
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
    def even_plus_even(self):
        hq, head = self.heading("even", "+", "even", "even")
        self.script("If you add two even numbers together, then the result "
                    "will always be even.")
        self.play(Write(hq))
        self.reveal(hq, head)

        # Example: 2 + 4 = 6
        self.script("For example, two plus four equals six.")
        A, B = self.dots(2), self.dots(4)
        plus = self.txt("+", fs=52)
        VGroup(A, plus, B).arrange(RIGHT, buff=0.5).move_to([MAIN_X, DOT_Y, 0])
        nA, nB = self.number_under("2", A), self.number_under("4", B)
        self.pop_in(A, B)
        self.play(FadeIn(plus), FadeIn(nA), FadeIn(nB))
        n6 = self.txt("6", fs=40).move_to([MAIN_X, NUM_Y, 0])
        M = self.combine(A, B, extra=[FadeOut(plus),
                                      ReplacementTransform(VGroup(nA, nB), n6)])
        chip = self.chip("even").next_to(n6, RIGHT, buff=0.3)
        self.play(FadeIn(chip, scale=0.5))

        self.script("Even numbers are always multiples of two…")
        note = self.txt("every dot has a partner", GREY_A, 28)
        note.next_to(M, UP, buff=0.35)
        self.play(LaggedStart(*[Indicate(p[0], color=HILITE, scale_factor=1.2)
                                for p in M.body], lag_ratio=0.25),
                  FadeIn(note))
        mult = self.eq_line("6", "=", "2", r"\times", "3")
        self.play(Write(mult))
        self.wait(1)
        self.clear_stage(keep=[head])

        # General case: 2A + 2B = 2(A + B)
        self.script("…so the sum of any two even numbers will be 2 times A "
                    "plus 2 times B…")
        A, B = self.gen("ppep"), self.gen("pepp")
        plus = self.txt("+", fs=52)
        VGroup(A, plus, B).arrange(RIGHT, buff=0.45).move_to([MAIN_X, DOT_Y, 0])
        self.pop_in(A, B)
        self.play(FadeIn(plus))
        bA, bB = self.brace(A, r"A\text{ pairs}"), self.brace(B, r"B\text{ pairs}")
        self.play(GrowFromCenter(bA), GrowFromCenter(bB))
        eq = self.eq_line("2", "A", "+", "2", "B", "=", "2", "(", "A", "+", "B", ")")
        self.play(TransformFromCopy(bA[1], eq[0:2]), FadeIn(eq[2]),
                  TransformFromCopy(bB[1], eq[3:5]), run_time=1.3)

        self.script("…where A and B are integers (which could be even or "
                    "odd).")
        note = self.txt("A, B = any integers", GREY_B, 28)
        note.move_to([MAIN_X, EQ2_Y, 0])
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(1)

        self.script("That means we can factor out the two and write the sum of "
                    "two even numbers as 2 times bracket A plus B…")
        self.play(FadeOut(bA), FadeOut(bB), FadeOut(note))
        M = self.combine(A, B, extra=[FadeOut(plus)])
        bM = self.brace(M, r"A+B\text{ pairs}")
        self.play(GrowFromCenter(bM))
        self.grow_eq(eq, [((0, 3), 6), (1, 8), (2, 9), (4, 10)], new=(5, 7, 11))

        self.script("…which then means that the result will always be a "
                    "multiple of 2, so it will always be even!")
        self.play(Indicate(eq[6], color=HILITE, scale_factor=1.5))
        chip = self.chip("even").next_to(eq, RIGHT, buff=0.35)
        self.play(FadeIn(chip, scale=0.5),
                  Circumscribe(eq[6:], color=EVEN_C, buff=0.1))
        self.wait(0.5)
        self.clear_stage(keep=[head])
        self.promote(head)

    # -----------------------------------------------------------------
    def odd_plus_odd(self):
        hq, head = self.heading("odd", "+", "odd", "even")
        self.script("Here’s an odd one: the sum of two odd numbers will "
                    "always be even…")
        self.play(Write(hq))
        self.reveal(hq, head)

        # Example: 3 + 1 = 4
        self.script("…for example, 3 plus 1 is 4.")
        A, B = self.dots(3), self.dots(1)
        plus = self.txt("+", fs=52)
        VGroup(A, plus, B).arrange(RIGHT, buff=0.5).move_to([MAIN_X, DOT_Y, 0])
        nA, nB = self.number_under("3", A), self.number_under("1", B)
        self.pop_in(A, B)
        self.play(FadeIn(plus), FadeIn(nA), FadeIn(nB))
        self.play(Indicate(A.single, color=ODD_C, scale_factor=1.8),
                  Indicate(B.single, color=ODD_C, scale_factor=1.8))
        n4 = self.txt("4", fs=40).move_to([MAIN_X, NUM_Y, 0])
        M = self.combine(A, B, extra=[FadeOut(plus),
                                      ReplacementTransform(VGroup(nA, nB), n4)])
        note = self.txt("the two leftovers pair up", GREY_A, 28)
        note.next_to(M, UP, buff=0.35)
        chip = self.chip("even").next_to(n4, RIGHT, buff=0.3)
        self.play(FadeIn(note), FadeIn(chip, scale=0.5))
        self.wait(1)
        self.clear_stage(keep=[head])

        # General case
        self.script("Any odd number is going to be the result of adding 1 (or "
                    "subtracting 1) from an even number…")
        A, B = self.gen("pep", odd=True), self.gen("pep", odd=True)
        plus = self.txt("+", fs=52)
        VGroup(A, plus, B).arrange(RIGHT, buff=0.5).move_to([MAIN_X, DOT_Y, 0])
        self.pop_in(A)
        bA2 = self.brace(A.body, "2A")
        bA1 = self.brace(VGroup(A.single, A.ghost), "+1", color=ODD_C)
        self.play(GrowFromCenter(bA2))
        self.play(GrowFromCenter(bA1))
        self.wait(0.5)
        self.pop_in(B)
        self.play(FadeIn(plus))
        bB2 = self.brace(B.body, "2B")
        bB1 = self.brace(VGroup(B.single, B.ghost), "+1", color=ODD_C)
        self.play(GrowFromCenter(bB2), GrowFromCenter(bB1))

        self.script("…so the sum of two odd numbers can be written as "
                    "bracket 2A plus 1 bracket, plus bracket 2B plus 1 "
                    "bracket…")
        l1 = self.eq_line("(", "2", "A", "+", "1", ")", "+",
                          "(", "2", "B", "+", "1", ")")
        self.play(TransformFromCopy(bA2[1], l1[1:3]),
                  TransformFromCopy(bA1[1], l1[3:5]),
                  TransformFromCopy(bB2[1], l1[8:10]),
                  TransformFromCopy(bB1[1], l1[10:12]),
                  FadeIn(VGroup(l1[0], l1[5], l1[6], l1[7], l1[12])),
                  run_time=1.5)
        self.wait(0.5)

        self.script("…which would be the same as 2 times bracket A plus B "
                    "bracket, plus 2…")
        self.play(*[FadeOut(b) for b in (bA2, bA1, bB2, bB1)])
        M = self.combine(A, B, extra=[FadeOut(plus)])
        b_ab = self.brace(VGroup(*M.body[:-1]), "2(A+B)")
        b_2 = self.brace(M.body[-1], "+2")
        self.play(GrowFromCenter(b_ab), GrowFromCenter(b_2))
        l2 = self.eq_line("=", "2", "(", "A", "+", "B", ")", "+", "2", y=EQ2_Y)
        # the two leftover 1s become the new +2
        self.grow_eq(l2, [((1, 8), 1), (2, 3), (9, 5), (6, 7), ((4, 11), 8)],
                     new=(0, 2, 4, 6), src=l1)
        self.wait(0.5)

        self.script("…which in turn is 2 times bracket A plus B plus 1 "
                    "bracket.")
        l3 = self.eq_line("=", "2", "(", "A", "+", "B", "+", "1", ")", y=EQ2_Y)
        b_all = self.brace(M, r"A+B+1\text{ pairs}")
        self.morph_eq(l2, l3, [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
                               (6, 8), (7, 6), (8, 7)])
        self.play(ReplacementTransform(VGroup(b_ab, b_2), b_all))

        self.script("Whatever A plus B plus 1 is, the fact we’re "
                    "multiplying it by 2 means that the result is even.")
        self.play(Indicate(l3[1], color=HILITE, scale_factor=1.6))
        chip = self.chip("even").next_to(l3, RIGHT, buff=0.35)
        self.play(FadeIn(chip, scale=0.5),
                  LaggedStart(*[Indicate(p[0], color=EVEN_C)
                                for p in M.pairs], lag_ratio=0.15))
        self.wait(0.5)
        self.clear_stage(keep=[head])
        self.promote(head)

    # -----------------------------------------------------------------
    def even_plus_odd(self):
        hq, head = self.heading("even", "+", "odd", "odd")
        self.script("Now the mixed pairings; an even integer plus an odd "
                    "integer gives an odd integer.")
        self.play(Write(hq))
        self.reveal(hq, head)

        # Example: 6 + 3 = 9
        self.script("For example, 6 plus 3 equals 9.")
        A, B = self.dots(6), self.dots(3)
        plus = self.txt("+", fs=52)
        VGroup(A, plus, B).arrange(RIGHT, buff=0.5).move_to([MAIN_X, DOT_Y, 0])
        nA, nB = self.number_under("6", A), self.number_under("3", B)
        self.pop_in(A, B)
        self.play(FadeIn(plus), FadeIn(nA), FadeIn(nB))
        n9 = self.txt("9", fs=40).move_to([MAIN_X, NUM_Y, 0])
        M = self.combine(A, B, extra=[FadeOut(plus),
                                      ReplacementTransform(VGroup(nA, nB), n9)])
        note = self.txt("one dot is left without a partner", GREY_A, 28)
        note.next_to(M, UP, buff=0.35)
        chip = self.chip("odd").next_to(n9, RIGHT, buff=0.3)
        self.play(Flash(M.single, color=ODD_C, line_length=0.2,
                        flash_radius=0.35),
                  FadeIn(note), FadeIn(chip, scale=0.5))
        self.wait(1)
        self.clear_stage(keep=[head])

        # General case
        self.script("An even integer can be written as 2A, and an odd integer "
                    "can be written as 2B + 1…")
        A, B = self.gen("ppep"), self.gen("pep", odd=True)
        plus = self.txt("+", fs=52)
        VGroup(A, plus, B).arrange(RIGHT, buff=0.5).move_to([MAIN_X, DOT_Y, 0])
        self.pop_in(A)
        bA = self.brace(A, "2A")
        self.play(GrowFromCenter(bA))
        self.pop_in(B)
        self.play(FadeIn(plus))
        bB2 = self.brace(B.body, "2B")
        bB1 = self.brace(VGroup(B.single, B.ghost), "+1", color=ODD_C)
        self.play(GrowFromCenter(bB2), GrowFromCenter(bB1))
        l1 = self.eq_line("2", "A", "+", "(", "2", "B", "+", "1", ")")
        self.play(TransformFromCopy(bA[1], l1[0:2]),
                  TransformFromCopy(bB2[1], l1[4:6]),
                  TransformFromCopy(bB1[1], l1[6:8]),
                  FadeIn(VGroup(l1[2], l1[3], l1[8])), run_time=1.5)

        self.script("…so adding them together gives 2A plus 2B plus 1.")
        l2 = self.eq_line("=", "2", "A", "+", "2", "B", "+", "1", y=EQ2_Y)
        self.grow_eq(l2, [(0, 1), (1, 2), (2, 3), (4, 4), (5, 5), (6, 6),
                          (7, 7)], new=(0,), src=l1)
        self.wait(0.5)

        self.script("Factoring out the 2s, that turns into 2 times bracket A "
                    "plus B bracket, plus one.")
        self.play(*[FadeOut(b) for b in (bA, bB2, bB1)])
        M = self.combine(A, B, extra=[FadeOut(plus)])
        b_ab = self.brace(M.body, "2(A+B)")
        b_1 = self.brace(VGroup(M.single, M.ghost), "+1", color=ODD_C)
        l3 = self.eq_line("=", "2", "(", "A", "+", "B", ")", "+", "1", y=EQ2_Y)
        self.morph_eq(l2, l3, [(0, 0), ((1, 4), 1), (2, 3), (3, 4), (5, 5),
                               (6, 7), (7, 8)])
        self.play(GrowFromCenter(b_ab), GrowFromCenter(b_1))

        self.script("2 times A plus B will be even, but then we’re adding "
                    "1 to it, turning the result odd.")
        ub = Brace(l3[1:7], DOWN, buff=0.08, color=EVEN_C)
        ub_lab = self.txt("even", EVEN_C, 26).next_to(ub, DOWN, buff=0.08)
        self.play(GrowFromCenter(ub), FadeIn(ub_lab))
        self.play(Circumscribe(l3[7:], color=ODD_C, shape=Circle, buff=0.08),
                  Flash(M.single, color=ODD_C, line_length=0.2,
                        flash_radius=0.35))
        chip = self.chip("odd").next_to(l3, RIGHT, buff=0.35)
        self.play(FadeIn(chip, scale=0.5))
        self.wait(0.5)
        self.clear_stage(keep=[head])
        self.promote(head)

    # -----------------------------------------------------------------
    def even_minus_odd(self):
        hq, head = self.heading("even", "−", "odd", "odd")
        self.script("An even number minus an odd number is odd…")
        self.play(Write(hq))
        self.reveal(hq, head)

        # Example: 8 - 1 = 7
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
        self.wait(1)
        self.clear_stage(keep=[head])

        # General case: 2A - (2B + 1) = 2(A - B) - 1
        self.script("We can write this as 2A minus bracket 2B plus 1 bracket.")
        A = self.gen("ppeppppep").move_to([MAIN_X, DOT_Y, 0])
        self.pop_in(A)
        bA = self.brace(A, "2A")
        self.play(GrowFromCenter(bA))
        l1 = self.eq_line("2", "A", "-", "(", "2", "B", "+", "1", ")")
        self.play(TransformFromCopy(bA[1], l1[0:2]))
        self.play(FadeIn(l1[2:]))
        self.wait(0.5)

        self.script("Unfolding the brackets and pairing up our two placeholder "
                    "values, we would get 2 times bracket A minus B bracket "
                    "minus 1.")
        l2 = self.eq_line("=", "2", "A", "-", "2", "B", "-", "1", y=EQ2_Y)
        self.grow_eq(l2, [(0, 1), (1, 2), (2, 3), (4, 4), (5, 5), (6, 6),
                          (7, 7)], new=(0,), src=l1)
        # take away 2B: the last B pairs leave
        gone = VGroup(*A.body[-3:])
        bB = self.brace(gone, "-2B", direction=UP)
        self.play(FadeOut(bA), GrowFromCenter(bB))
        self.play(VGroup(gone, bB).animate.shift(UP * 1.2).set_opacity(0),
                  run_time=1.2)
        self.remove(gone, bB)
        rest = list(A.body[:-3])
        self.play(*self.recenter(rest))
        # ...and one more dot
        ghost = self.break_pair(rest[-1])
        b_ab = self.brace(VGroup(*rest[:-1]), "2(A-B)")
        b_1 = self.brace(VGroup(rest[-1][2], ghost), "-1", color=ODD_C)
        l3 = self.eq_line("=", "2", "(", "A", "-", "B", ")", "-", "1", y=EQ2_Y)
        self.morph_eq(l2, l3, [(0, 0), ((1, 4), 1), (2, 3), (3, 4), (5, 5),
                               (6, 7), (7, 8)])
        self.play(GrowFromCenter(b_ab), GrowFromCenter(b_1))

        self.script("2 times A minus B would be even, but since we’re "
                    "subtracting one from it, we get an odd number.")
        ub = Brace(l3[1:7], DOWN, buff=0.08, color=EVEN_C)
        ub_lab = self.txt("even", EVEN_C, 26).next_to(ub, DOWN, buff=0.08)
        self.play(GrowFromCenter(ub), FadeIn(ub_lab))
        self.play(Circumscribe(l3[7:], color=ODD_C, shape=Circle, buff=0.08))
        chip = self.chip("odd").next_to(l3, RIGHT, buff=0.35)
        self.play(FadeIn(chip, scale=0.5))
        self.wait(0.5)
        self.clear_stage(keep=[head])
        self.promote(head)

    # -----------------------------------------------------------------
    def even_minus_even(self):
        hq, head = self.heading("even", "−", "even", "even")
        self.script("And lastly, an even number minus an even number is "
                    "even…")
        self.play(Write(hq))
        self.reveal(hq, head)

        # Example: 16 - 12 = 4
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
        self.wait(1)
        self.clear_stage(keep=[head])

        # General case: 2A - 2B = 2(A - B)
        self.script("2A minus 2B is 2 bracket A minus B bracket…")
        A = self.gen("ppeppppep").move_to([MAIN_X, DOT_Y, 0])
        self.pop_in(A)
        bA = self.brace(A, "2A")
        self.play(GrowFromCenter(bA))
        eq = self.eq_line("2", "A", "-", "2", "B", "=", "2", "(", "A", "-", "B", ")")
        self.play(TransformFromCopy(bA[1], eq[0:2]))
        gone = VGroup(*A.body[-3:])
        bB = self.brace(gone, "-2B", direction=UP)
        self.play(GrowFromCenter(bB), FadeIn(eq[2:5]))
        self.play(FadeOut(bA),
                  VGroup(gone, bB).animate.shift(UP * 1.2).set_opacity(0),
                  run_time=1.2)
        self.remove(gone, bB)
        rest = list(A.body[:-3])
        self.play(*self.recenter(rest))
        b_ab = self.brace(VGroup(*rest), r"A-B\text{ pairs}")
        self.play(GrowFromCenter(b_ab))
        self.grow_eq(eq, [((0, 3), 6), (1, 8), (2, 9), (4, 10)], new=(5, 7, 11))

        self.script("…so whatever A minus B is, it will be an integer, and "
                    "the result will be even since we’re multiplying that "
                    "integer value by 2.")
        self.play(Indicate(eq[6], color=HILITE, scale_factor=1.5))
        chip = self.chip("even").next_to(eq, RIGHT, buff=0.35)
        self.play(FadeIn(chip, scale=0.5),
                  LaggedStart(*[Indicate(p[0], color=EVEN_C)
                                for p in rest if getattr(p, "is_pair", False)],
                              lag_ratio=0.15))
        self.wait(0.5)
        self.clear_stage(keep=[head])
        self.promote(head)


# =====================================================================
# Slide 9: multiplication (and division)
# =====================================================================
class EvenOddMultiplication(ParityScene):
    def construct(self):
        self.setup_scene()
        self.show_sidebar("Multiplying")
        self.dominance()
        self.product("even", "even", "even", (2, [2]), (6, [2, 3]), (12, [2, 2, 3]),
                     self.even_times_even)
        self.product("odd", "odd", "odd", (3, [3]), (5, [5]), (15, [3, 5]),
                     self.odd_times_odd)
        self.product("odd", "even", "even", (5, [5]), (4, [2, 2]), (20, [5, 2, 2]),
                     self.odd_times_even)
        self.division()
        self.many_factors()
        self.clear_stage()
        self.play(LaggedStart(*[Indicate(r, color=HILITE, scale_factor=1.1)
                                for r in self.rules], lag_ratio=0.2))
        self.wait(2)

    # -----------------------------------------------------------------
    def dominance(self):
        self.script("Next, we have multiplication. Here, evenness is the "
                    "“dominant” trait to make an analogy to biology.")
        title = self.txt("Multiplication", fs=50).move_to([MAIN_X, HEAD_Y, 0])
        self.play(Write(title))
        e, o, r = self.chip("even", fs=36), self.chip("odd", fs=36), \
            self.chip("even", fs=36)
        times, eq = self.txt("×", fs=56), self.txt("=", fs=56)
        row = VGroup(e, times, o, eq, r).arrange(RIGHT, buff=0.45)
        row.move_to([MAIN_X, 1.0, 0])
        dom = self.txt("dominant", EVEN_C, 28).next_to(e, DOWN, buff=0.3)
        rec = self.txt("recessive", GREY_B, 28).next_to(o, DOWN, buff=0.3)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in row[:3]],
                              lag_ratio=0.2))
        self.play(FadeIn(dom), FadeIn(rec))
        self.play(FadeIn(eq), TransformFromCopy(e, r, path_arc=-PI / 3))
        self.play(Flash(r, color=EVEN_C, flash_radius=0.8),
                  o.animate.set_opacity(0.4))
        note = self.txt("one even factor is enough to make the product even",
                        GREY_A, 28).move_to([MAIN_X, -0.9, 0])
        self.play(FadeIn(note))
        self.wait(1.5)
        self.clear_stage()

    # -----------------------------------------------------------------
    def product(self, a, b, res, fa, fb, fp, body):
        """Shared layout: bubble(a) x bubble(b) = bubble(product)."""
        op = "×"
        hq, head = self.heading(a, op, b, res)
        A, B, P = self.bubble(*fa), self.bubble(*fb), self.bubble(*fp)
        times, eq = self.txt("×", fs=56), self.txt("=", fs=56)
        row = VGroup(A, times, B, eq, P).arrange(RIGHT, buff=0.45)
        row.move_to([MAIN_X, 0.75, 0])
        # line the bubbles up by their circles, not their labels
        for m in (A, times, B, eq, P):
            m.shift(UP * (0.55 - (m.circ.get_y() if hasattr(m, "circ")
                                  else m.get_y())))
        body(hq, head, A, B, P, times, eq)
        self.clear_stage(keep=[head])
        self.promote(head)

    def intro_product(self, hq, head, A, B, P, times, eq):
        self.play(Write(hq))
        self.reveal(hq, head)

    def build_product(self, A, B, P, times, eq, math):
        self.show_bubbles(A, B)
        self.play(FadeIn(times), FadeIn(eq))
        self.gather([A, B], P)
        m = self.mt(*math).move_to([MAIN_X, EQ2_Y, 0])
        self.play(Write(m))
        return m

    def even_times_even(self, hq, head, A, B, P, times, eq):
        self.script("An even number times an even number will be even…")
        self.intro_product(hq, head, A, B, P, times, eq)

        self.script("…for example 2 times 6 is 12.")
        self.build_product(A, B, P, times, eq,
                           ["2", r"\times", "6", "=", "2", r"\times",
                            r"(", "2", r"\cdot", "3", ")", "=", "12"])

        self.script("Any number with a two in its prime factorization is "
                    "even…")
        note = self.verdict(A.circ, "has a 2", True)
        note_b = self.verdict(B.circ, "has a 2", True)
        self.play(Indicate(A.twos, color=HILITE, scale_factor=1.3),
                  Indicate(B.twos, color=HILITE, scale_factor=1.3),
                  FadeIn(note), FadeIn(note_b))

        self.script("…so multiplying together two even numbers means we "
                    "have at least two 2s in that prime factorization.")
        rects = VGroup(*[SurroundingRectangle(t, color=HILITE, buff=0.05,
                                              corner_radius=0.3)
                         for t in P.twos])
        self.play(Create(rects), *[Flash(t, color=EVEN_C, line_length=0.15,
                                         flash_radius=0.4) for t in P.twos])
        chip = self.chip("even").next_to(P.circ, DOWN, buff=0.3)
        self.play(FadeIn(chip, scale=0.5))
        self.wait(1)

    def odd_times_odd(self, hq, head, A, B, P, times, eq):
        self.script("An odd number times an odd number will be odd, like 3 "
                    "times 5 is 15.")
        self.intro_product(hq, head, A, B, P, times, eq)
        self.build_product(A, B, P, times, eq,
                           ["3", r"\times", "5", "=", "3", r"\cdot", "5",
                            "=", "15"])

        self.script("Remember, oddness or evenness depends on if anyone is "
                    "showing up to the party with a factor of two somewhere in "
                    "the prime factorization.")
        ask = self.txt("Who brought a 2?", GREY_A, 30)
        ask.next_to(VGroup(A, B), UP, buff=0.3)
        self.play(FadeIn(ask))
        for f in (A, B):
            self.play(Circumscribe(f.circ, color=HILITE, shape=Circle),
                      run_time=0.8)
            self.play(FadeIn(self.verdict(f.circ, "no 2s", False)),
                      run_time=0.5)

        self.script("When two odd numbers show up, neither have any 2s to add "
                    "to the mix, so the result won’t have any 2s either.")
        self.play(Circumscribe(P.circ, color=HILITE, shape=Circle))
        chip = self.chip("odd").next_to(P.circ, DOWN, buff=0.3)
        self.play(FadeIn(self.verdict(chip, "no 2s", False)),
                  FadeIn(chip, scale=0.5))
        self.wait(1)

    def odd_times_even(self, hq, head, A, B, P, times, eq):
        self.script("Which also means that an odd number times an even number "
                    "is even, like 5 times 4 is 20.")
        self.intro_product(hq, head, A, B, P, times, eq)
        self.build_product(A, B, P, times, eq,
                           ["5", r"\times", "4", "=", "5", r"\cdot", "2",
                            r"\cdot", "2", "=", "20"])

        self.script("The odd number shows up without any factors of two (by "
                    "definition)…")
        self.play(Circumscribe(A.circ, color=HILITE, shape=Circle))
        self.play(FadeIn(self.verdict(A.circ, "no 2s", False)))

        self.script("…but that’s fine because the even number has "
                    "brought along its own.")
        self.play(Indicate(B.twos, color=HILITE, scale_factor=1.3),
                  FadeIn(self.verdict(B.circ, "brings 2s", True)))
        self.play(LaggedStart(*[
            TransformFromCopy(s, d, path_arc=-PI / 4)
            for s, d in zip(B.twos, P.twos)], lag_ratio=0.3),
            *[Flash(t, color=EVEN_C, line_length=0.15, flash_radius=0.4)
              for t in P.twos])
        chip = self.chip("even").next_to(P.circ, DOWN, buff=0.3)
        self.play(FadeIn(chip, scale=0.5))
        self.wait(1)

    # -----------------------------------------------------------------
    def division(self):
        self.script("You may wonder, since multiplication and division are so "
                    "closely related, what are the rules for division? Really, "
                    "there are none.")
        head = self.txt("What about division?", fs=46)
        head.move_to([MAIN_X, HEAD_Y, 0])
        self.play(Write(head))

        def row(expr, word, color, y):
            tag = self.rule_text("even ÷ even", fs=26)
            m = MathTex(expr, font_size=52)
            c = self.chip(word, color)
            g = VGroup(tag, m, c).arrange(RIGHT, buff=0.5)
            g.move_to([MAIN_X, y, 0])
            return g

        rows = [row(r"12 \div 2 = 6", "even", None, 1.9),
                row(r"12 \div 4 = 3", "odd", None, 0.9),
                row(r"6 \div 4 = 1.5", "not an integer", NO_C, -0.1)]
        # line the expressions and chips up in columns
        for g in rows[1:]:
            g[0].align_to(rows[0][0], LEFT)
            g[1].align_to(rows[0][1], LEFT)
            g[2].next_to(g[1], RIGHT, buff=0.5)
        for g in rows[:2]:
            self.play(FadeIn(g[0]), Write(g[1]))
            self.play(FadeIn(g[2], scale=0.5))

        self.script("We can’t even guarantee that the result of division "
                    "will be an integer, let alone say whether it would be even "
                    "or odd.")
        g = rows[2]
        self.play(FadeIn(g[0]), Write(g[1]))
        self.play(FadeIn(g[2], scale=0.5), Indicate(g[1][0][-3:], color=NO_C))
        self.wait(0.5)

        self.script("In certain circumstances you can figure out the result "
                    "depending on particular conditions, but it’s not "
                    "something that you can determine with simple rules…")
        stamp_t = self.txt("NO SIMPLE RULE", NO_C, 40, weight=BOLD)
        stamp = VGroup(SurroundingRectangle(stamp_t, color=NO_C, buff=0.2,
                                            corner_radius=0.1, stroke_width=5),
                       stamp_t).rotate(6 * DEGREES)
        stamp.move_to([MAIN_X, -1.5, 0])
        self.play(FadeIn(stamp, scale=1.6), run_time=0.6)
        self.wait(1)
        self.clear_stage(keep=[head])
        self.promote(head, self.txt("÷  no simple rule", NO_C, 46))

    # -----------------------------------------------------------------
    def many_factors(self):
        self.script("…this pattern also generalizes to cases where we have "
                    "more than two integers multiplied together.")
        head = self.txt("More than two factors", fs=46)
        head.move_to([MAIN_X, HEAD_Y, 0])
        self.play(Write(head))

        specs = [(3, [3]), (5, [5]), (7, [7]), (4, [2, 2]), (9, [3, 3])]
        fs = [self.bubble(n, p, min_r=0.55, fs=34) for n, p in specs]
        row = VGroup()
        for i, f in enumerate(fs):
            if i:
                row.add(self.txt("×", fs=44))
            row.add(f)
        row.arrange(RIGHT, buff=0.22)
        for f in fs:  # line the circles up, whatever their size
            f.shift(UP * (row.get_y() - f.circ.get_y()))
        if row.width > 9.6:
            row.scale_to_fit_width(9.6)
        row.move_to([MAIN_X, 1.85, 0])
        prod = self.bubble(3780, [3, 5, 7, 2, 2, 3, 3], fs=36)
        prod.scale(0.85).move_to([MAIN_X - 1.0, -0.8, 0])
        prod.label.next_to(prod.circ, LEFT, buff=0.35)  # no room above it
        self.show_bubbles(*fs)
        self.play(*[FadeIn(m) for m in row if m not in fs])
        self.gather(fs, prod, run_time=2.5)

        self.script("If there’s at least one even number, then there will "
                    "be a 2 in the prime factorization of the result, so the "
                    "result will be even.")
        four = fs[3]
        self.play(Circumscribe(four.circ, color=HILITE, shape=Circle))
        self.play(*[Flash(t, color=EVEN_C, line_length=0.15, flash_radius=0.4)
                    for t in prod.twos],
                  Create(VGroup(*[SurroundingRectangle(
                      t, color=HILITE, buff=0.05, corner_radius=0.3)
                      for t in prod.twos])))
        chip = self.chip("even").next_to(prod.circ, RIGHT, buff=0.4)
        self.play(FadeIn(chip, scale=0.5))
        self.wait(1)
        self.clear_stage(keep=[head])
        self.promote(head, self.implies("one even factor", "even"))

        # Working backwards from an odd product
        self.script("If the result is odd, then that means that every single "
                    "one of the factors must also be odd.")
        head = self.txt("Odd product?", fs=46).move_to([MAIN_X, HEAD_Y, 0])
        self.play(Write(head))
        boxes = [VGroup(RoundedRectangle(corner_radius=0.1, width=1.1,
                                         height=0.9, stroke_color=GREY_B,
                                         stroke_width=3),
                        self.txt("?", GREY_B, 44)) for _ in range(4)]
        res = self.chip("odd", fs=34)
        row = VGroup()
        for i, b in enumerate(boxes):
            if i:
                row.add(self.txt("×", fs=48))
            row.add(b)
        row.add(self.txt("=", fs=48), res)
        row.arrange(RIGHT, buff=0.25).move_to([MAIN_X, 1.2, 0])
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in row],
                              lag_ratio=0.1))
        self.wait(0.5)

        # What if one of them were even? It would bring a 2...
        what_if = self.txt("if any factor were even…", GREY_A, 28)
        what_if.move_to([MAIN_X, -0.2, 0])
        two = self.token(2).move_to(boxes[1])
        self.play(FadeIn(what_if), FadeOut(boxes[1][1]),
                  GrowFromCenter(two))
        even_res = self.chip("even", fs=34).move_to(res)
        self.play(two.animate(path_arc=-PI / 3).move_to(res).set_opacity(0),
                  Transform(res, even_res), run_time=1.2)
        cross = Cross(res, stroke_color=NO_C, stroke_width=8)
        nope = self.txt("…the product would be even", NO_C, 28)
        nope.next_to(what_if, DOWN, buff=0.2)
        self.play(Create(cross), FadeIn(nope))
        self.wait(1)
        self.play(FadeOut(cross), FadeOut(what_if), FadeOut(nope),
                  Transform(res, self.chip("odd", fs=34).move_to(res)),
                  FadeIn(boxes[1][1]))
        self.remove(two)

        odds = [self.chip("odd", fs=30).move_to(b) for b in boxes]
        self.play(LaggedStart(*[ReplacementTransform(b, o)
                                for b, o in zip(boxes, odds)], lag_ratio=0.25))
        note = self.txt("so every factor must be odd", GREY_A, 30)
        note.move_to([MAIN_X, -0.4, 0])
        self.play(FadeIn(note), Circumscribe(VGroup(*odds), color=ODD_C))
        self.wait(1)
        self.clear_stage(keep=[head])
        self.promote(head, self.implies("odd product", "all odd"))
