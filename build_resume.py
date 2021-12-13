from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
import pandas as pd


class ResumeGenerator():
    # Set the page height and width
    HEIGHT = 11 * inch
    WIDTH = 8.5 * inch

    def __init__(self, data, contact):
        # Import our font
        registerFont(TTFont('Inconsolata', 'fonts/Inconsolata-Regular.ttf'))
        registerFont(TTFont('InconsolataBold', 'fonts/Inconsolata-Bold.ttf'))
        registerFontFamily('Inconsolata', normal='Inconsolata', bold='InconsolataBold')

        # Set our styles
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(name='Content',
                                fontFamily='Inconsolata',
                                fontSize=8,
                                spaceAfter=.1*inch))
        
        self.data = [
            ['OBJECTIVE', Paragraph(data['objective'], self.styles['Content'])],
            ['SUMMARY', Paragraph(data['summary'], self.styles['Content'])],
            ['EDUCATION', [Paragraph(x, self.styles['Content']) for x in data['education']]],
            ['EXPERIENCE', [Paragraph(x, self.styles['Content']) for x in data['experience']]]
        ]
        self.contact = contact

    def generate(self):
        pdfname = 'resume.pdf'
        doc = SimpleDocTemplate(
            pdfname,
            pagesize=letter,
            bottomMargin=.5 * inch,
            topMargin=.7 * inch,
            rightMargin=.4 * inch,
            leftMargin=.4 * inch)  # set the doc template
        # style = self.styles["Normal"]  # set the style to normal
        story = []  # create a blank story to tell
        contentTable = Table(
            self.data,
            colWidths=[
                0.8 * inch,
                6.9 * inch])
        tblStyle = TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONT', (0, 0), (-1, -1), 'Inconsolata'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT')])
        contentTable.setStyle(tblStyle)
        story.append(contentTable)
        doc.build(
            story,
            onFirstPage=self.myPageWrapper()
            )
        return pdfname

    def myPageWrapper(self):
        """
            Draw the framework for the first page,
            pass in contact info as a dictionary
        """
        # template for static, non-flowables, on the first page
        # draws all of the contact information at the top of the page
        def myPage(canvas, doc):
            canvas.saveState()  # save the current state
            canvas.setFont('InconsolataBold', 16)  # set the font for the name
            canvas.drawString(
                .4 * inch,
                ResumeGenerator.HEIGHT - (.4 * inch),
                self.contact['name'])  # draw the name on top left page 1
            canvas.setFont('Inconsolata', 8)  # sets the font for contact
            canvas.drawRightString(
                ResumeGenerator.WIDTH - (.4 * inch),
                ResumeGenerator.HEIGHT - (.4 * inch),
                self.contact['website'])  
            canvas.line(.4 * inch, ResumeGenerator.HEIGHT - (.47 * inch), 
                ResumeGenerator.WIDTH - (.4 * inch), ResumeGenerator.HEIGHT - (.47 * inch))
            canvas.drawString(
                .4 * inch,
                ResumeGenerator.HEIGHT - (.6 * inch),
                self.contact['phone'])
            canvas.drawCentredString(
                ResumeGenerator.WIDTH / 2.0,
                ResumeGenerator.HEIGHT - (.6 * inch),
                self.contact['address'])
            canvas.drawRightString(
                ResumeGenerator.WIDTH - (.4 * inch),
                ResumeGenerator.HEIGHT - (.6 * inch),
                self.contact['email'])
            # restore the state to what it was when saved
            canvas.restoreState()
        return myPage
