from manim import *


class TitrationCalc(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Title ---
        title = Text(
            "Titration: Finding Volume of NaOH",
            font="Segoe UI",
            font_size=36,
            color=BLACK,
        )
        self.play(Write(title))
        self.wait(1.5)
        self.play(title.animate.scale(0.7).to_edge(UP))

        # --- Given information ---
        given_header = Text("Given:", font="Segoe UI", font_size=30, color=BLUE).next_to(
            title, DOWN, buff=0.5
        ).align_to(title, LEFT)

        given_lines = VGroup(
            MathTex(r"M_{\text{NaOH}} = 2.00 \text{ M}", color=BLACK),
            MathTex(r"V_{\text{H}_2\text{SO}_4} = 75.0 \text{ mL}", color=BLACK),
            MathTex(r"M_{\text{H}_2\text{SO}_4} = 0.500 \text{ M}", color=BLACK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(given_header, DOWN, aligned_edge=LEFT, buff=0.3)

        self.play(Write(given_header))
        for line in given_lines:
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.6)
        self.wait(1)

        # Clear for next step
        self.play(FadeOut(given_header, given_lines))

        # --- Step 1: Balanced equation ---
        step1_label = Text(
            "Step 1: Balanced Equation", font="Segoe UI", font_size=28, color=BLUE
        ).next_to(title, DOWN, buff=0.5).align_to(title, LEFT)

        equation = MathTex(
            r"2\text{NaOH}", r"+", r"\text{H}_2\text{SO}_4",
            r"\rightarrow", r"\text{Na}_2\text{SO}_4", r"+", r"2\text{H}_2\text{O}",
            color=BLACK,
            font_size=40,
        ).next_to(step1_label, DOWN, buff=0.4)

        ratio_note = MathTex(
            r"\text{Mole ratio: } 2 \text{ mol NaOH} : 1 \text{ mol H}_2\text{SO}_4",
            color=DARK_GRAY,
            font_size=32,
        ).next_to(equation, DOWN, buff=0.4)

        self.play(Write(step1_label))
        self.play(Write(equation))
        self.wait(0.5)

        # Highlight the coefficients
        box_naoh = SurroundingRectangle(equation[0], color=RED, buff=0.08)
        box_acid = SurroundingRectangle(equation[2], color=RED, buff=0.08)
        self.play(Create(box_naoh), Create(box_acid))
        self.play(Write(ratio_note))
        self.wait(2)

        self.play(FadeOut(step1_label, equation, ratio_note, box_naoh, box_acid))

        # --- Step 2: Moles of H2SO4 ---
        step2_label = Text(
            "Step 2: Moles of H₂SO₄", font="Segoe UI", font_size=28, color=BLUE
        ).next_to(title, DOWN, buff=0.5).align_to(title, LEFT)

        mol_formula = MathTex(
            r"n = M \times V",
            color=BLACK,
            font_size=36,
        ).next_to(step2_label, DOWN, buff=0.4)

        mol_sub = MathTex(
            r"n_{\text{H}_2\text{SO}_4}",
            r"=",
            r"0.500 \text{ M}",
            r"\times",
            r"0.0750 \text{ L}",
            color=BLACK,
            font_size=36,
        ).next_to(mol_formula, DOWN, buff=0.35)

        mol_result = MathTex(
            r"n_{\text{H}_2\text{SO}_4}",
            r"=",
            r"0.0375 \text{ mol}",
            color=BLACK,
            font_size=36,
        ).next_to(mol_sub, DOWN, buff=0.35)

        # Highlight the conversion 75.0 mL -> 0.0750 L
        convert_note = MathTex(
            r"75.0 \text{ mL} = 0.0750 \text{ L}",
            color=DARK_GRAY,
            font_size=28,
        ).next_to(mol_sub, RIGHT, buff=0.4)

        self.play(Write(step2_label))
        self.play(Write(mol_formula))
        self.wait(0.5)
        self.play(Write(mol_sub))
        self.play(FadeIn(convert_note, shift=UP * 0.2))
        self.wait(0.8)
        self.play(Write(mol_result))

        result_box = SurroundingRectangle(mol_result[2], color=GREEN, buff=0.08)
        self.play(Create(result_box))
        self.wait(2)

        self.play(FadeOut(step2_label, mol_formula, mol_sub, mol_result, convert_note, result_box))

        # --- Step 3: Moles of NaOH ---
        step3_label = Text(
            "Step 3: Moles of NaOH (using mole ratio)", font="Segoe UI", font_size=28, color=BLUE
        ).next_to(title, DOWN, buff=0.5).align_to(title, LEFT)

        ratio_eq = MathTex(
            r"n_{\text{NaOH}}",
            r"=",
            r"2",
            r"\times",
            r"n_{\text{H}_2\text{SO}_4}",
            color=BLACK,
            font_size=36,
        ).next_to(step3_label, DOWN, buff=0.4)

        ratio_sub = MathTex(
            r"n_{\text{NaOH}}",
            r"=",
            r"2",
            r"\times",
            r"0.0375 \text{ mol}",
            color=BLACK,
            font_size=36,
        ).next_to(ratio_eq, DOWN, buff=0.35)

        ratio_result = MathTex(
            r"n_{\text{NaOH}}",
            r"=",
            r"0.0750 \text{ mol}",
            color=BLACK,
            font_size=36,
        ).next_to(ratio_sub, DOWN, buff=0.35)

        self.play(Write(step3_label))
        self.play(Write(ratio_eq))
        self.wait(0.5)
        self.play(Write(ratio_sub))
        self.wait(0.5)
        self.play(Write(ratio_result))

        result_box2 = SurroundingRectangle(ratio_result[2], color=GREEN, buff=0.08)
        self.play(Create(result_box2))
        self.wait(2)

        self.play(FadeOut(step3_label, ratio_eq, ratio_sub, ratio_result, result_box2))

        # --- Step 4: Volume of NaOH ---
        step4_label = Text(
            "Step 4: Volume of NaOH", font="Segoe UI", font_size=28, color=BLUE
        ).next_to(title, DOWN, buff=0.5).align_to(title, LEFT)

        vol_formula = MathTex(
            r"V = \frac{n}{M}",
            color=BLACK,
            font_size=36,
        ).next_to(step4_label, DOWN, buff=0.4)

        vol_sub = MathTex(
            r"V_{\text{NaOH}}",
            r"=",
            r"\frac{0.0750 \text{ mol}}{2.00 \text{ M}}",
            color=BLACK,
            font_size=36,
        ).next_to(vol_formula, DOWN, buff=0.35)

        vol_result = MathTex(
            r"V_{\text{NaOH}}",
            r"=",
            r"0.0375 \text{ L}",
            color=BLACK,
            font_size=36,
        ).next_to(vol_sub, DOWN, buff=0.35)

        vol_ml = MathTex(
            r"V_{\text{NaOH}}",
            r"=",
            r"37.5 \text{ mL}",
            color=BLACK,
            font_size=40,
        ).next_to(vol_result, DOWN, buff=0.35)

        self.play(Write(step4_label))
        self.play(Write(vol_formula))
        self.wait(0.5)
        self.play(Write(vol_sub))
        self.wait(0.8)
        self.play(Write(vol_result))
        self.wait(0.5)
        self.play(Write(vol_ml))

        final_box = SurroundingRectangle(vol_ml, color=RED, buff=0.12, corner_radius=0.1)
        self.play(Create(final_box))
        self.wait(1)

        # --- Final answer emphasis ---
        self.play(
            FadeOut(step4_label, vol_formula, vol_sub, vol_result),
            vol_ml.animate.move_to(ORIGIN),
            final_box.animate.move_to(ORIGIN),
        )
        self.play(FadeOut(title))

        answer_label = Text(
            "37.5 mL of NaOH is needed to reach\nthe second equivalence point.",
            font="Segoe UI",
            font_size=30,
            color=DARK_GRAY,
            line_spacing=1.3,
        ).next_to(vol_ml, DOWN, buff=0.5)

        self.play(FadeIn(answer_label, shift=UP * 0.3))
        self.wait(3)
