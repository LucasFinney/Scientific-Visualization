from manim import *

class VectorArrow(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        dot = Dot([-3, -1, 0],color=BLACK)
        dot2 = Dot([2, 1, 0],color=BLACK)
        arrow = Line(dot.get_center(), dot2.get_center(),path_arc=-3).set_color(BLUE).add_tip()
        arrow2 = Line(dot.get_center(), dot2.get_center(),path_arc=1).set_color(ORANGE).add_tip()
        arrow3 = Line(dot.get_center(), dot2.get_center(),path_arc=2).set_color(RED).add_tip()
        arrow4 = Arrow(dot.get_center(), dot2.get_center()).set_color(BLACK)

        points = [
            [-3,-1,0],
            [0,-1,0],
            [-3,-1.5,0],
            [2,-1.5,0],
            [2,1,0]
        ]
        
        lines = []
        for i in range(4):
            lines = lines + [DashedLine(points[i],points[i+1]).set_color(BLACK)]
        
        self.add(dot, dot2)
        self.play(Create(arrow))
        self.play(Create(arrow2))
        self.play(Create(arrow3))
        for line in lines:
            self.play(Create(line),run_time=0.1)
        self.wait(1)
        angle = angle_between_vectors(dot2.get_center()-dot.get_center(), RIGHT)
        text = Text("Displacement",font="Open Sans").next_to(arrow4.get_center(), UP).set_color(BLACK).rotate(angle)
        
        self.play(Create(arrow4),Create(text))
        self.wait(2)