from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Pt, Inches, Cm
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT


class PowerPointmaker:

    def __init__(self, text, date):
        print(text)
        print(date)
        self.prs = Presentation()

        self.blank_slide_layout = self.prs.slide_layouts[6]
        # self.makeSlides()

    def makeSlides(self):
        for i in range(4):
            self.prs.slide_width = 11887200
            self.prs.slide_height = 6686550
            slide = self.prs.slides.add_slide(self.blank_slide_layout)
            slide.shapes.add_picture('bg.jpg',  0,0, width=self.prs.slide_width)

            txBox = slide.shapes.add_textbox(0, 0, Inches(13), Inches(7))
            txBox.text_frame.paragraphs[0].alignment = PP_PARAGRAPH_ALIGNMENT.CENTER
            tf = txBox.text_frame
            tf.word_wrap = True
            tf.clear()

            p = tf.paragraphs[0]
            run = p.add_run()
            run.text = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut,"
            run.font.color.rgb = RGBColor(255, 255, 255)
            font = run.font
            font.name = 'Calibri'
            font.size = Pt(44)

        self.prs.save('test.pptx')

    def makefirstReadingPowerPoint(self):
        pass

    def makePsalmPowerPoint(self):
        pass






