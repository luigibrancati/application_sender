from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont


contact_var = {
        'name': 'Nicholas Depinet',
        'website': 'http://github.com/nickdepinet/',
        'email': 'depinetnick@gmail.com',
        'address': '3092 Nathaniel Rochester Hall, Rochester, NY 14623',
        'phone': '(614)365-1089'}
data_var = {
    'objective': ' '.join(['Seeking co-operative employment',
                'in the field of software development,',
                'preferably working in python and web backend infrastructure or distributed computing, ',
                'to start June 2016.']),
    'summary': ' '.join(['I love to use programming to solve interesting problems.',
                'I love working in Python (which is why I generated this resume in Python using ReportLab), but I am comfortable working in a variety of languages.',
                'I am currently exploring the exciting world of distributed and cloud computing, and love to discuss the unique opportunities this type of computing presents.']),
    'education': '<br/>'.join(['<b>Rochester Insitute of Technology</b>',
                '<b>B.S.</b>  Computer Science',
                '<b>Expected Graduation</b>  2017']),
    'skills': '<br/>'.join(['<b>Languages</b>  Python, Java, C#, C, MIPS Assembly, Bash, jQuery, HTML, CSS',
                '<b>Tools</b>  Git/Mercurial, Vim, Django, Tornado, Twisted, Autobahn, ReportLab',
                '<b>Platforms</b>  Linux (Debian, RHEL), OSX, Windows',
                '<b>Services</b>  Microsoft Application Insights, MySQL, PostgreSQL, MongoDB, Apache/Nginx, HAProxy, Gunicorn']),
    'experience': [''.join(['<b>Microsoft</b> - Redmond, WA<br/>',
                '<alignment=TA_RIGHT>Software Engineer Intern: May - August 2015</alignment><br/>',
                'Designed and developed a distributed testing framework to allow for the execution of ',
                'the principals of testing in production of Windows 10 Universal Apps across many devices.',
                'Development done in C#, using Microsoft Application Insights as a data backend.<br/>']),
                ''.join(['<b>Nebula</b> - Seattle, WA<br/>',
                '<alignment=TA_RIGHT>Software Development Intern, Control Plane: June - August 2014</alignment><br/>',
                'Developed improvements to the initial installation Out-of-box experience (OOBE) of the Nebula One product. ',
                'Development done in python.<br/>']),
                ''.join(['<b>SpkrBar</b> - Columbus, OH<br/>',
                '<alignment=TA_RIGHT>Software Developer: September - December 2013</alignment><br/>',
                'Developed and maintained the front and backend of a startup website using Python and the Django framework. ',
                'The website allows technical conferences, speakers, and attendees to connect and keep up to date. ']),
                ''.join(['<b>Olah Healthcare</b> - Columbus, OH<br/>',
                '<alignment=TA_RIGHT>Software Engineering Intern: May - August 2013</alignment><br/>',
                'Developed a web application using Python and the Django framework ',
                'to allow hospitals to easily store, search, and retrieve archived medical records. ',
                'Primary Responsibility was the design and implementation of the metadata storage backend, and search functionality.']),
                ''.join(['<b>Computer Science House</b> - Rochester, NY<br/>',
                'Drink Administrator: February 2013 - Present<br/>',]),
                ''.join(['<b>STI-Healthcare</b> - Columbus, OH<br/>',
                'Network & Server Administration Intern: May - August 2012<br/>',])],
    'projects': [
                ''.join(['<b>Hangman</b> - http://github.com/nickdepinet/hangman<br/>',
                'Implemented a command line hangman game engine and an artifical intelligence player in python.',
                'The AI uses letter frequencies from the english dictionary and additionally word frequencies from the ',
                'Google corpus make intelligent guesses as to the next letter.']),
                ''.join(['<b>g()(\'al\')</b> - http://github.com/eatnumber1/goal<br/>',
                'Completed the first python solution to the g()(\'al\') programming challenge. ',
                'The "goal" of the g()(\'al\') challenge is to enable the calling of g()(\'al\') in the source of the ',
                'language of choice with n ()\'s, and to be returned the string "goal" with the appropriate number of "o"s.']),
                ''.join(['<b>DrinkPi</b> - http://github.com/jeid64/drinkpi/<br/>',
                'Worked with a partner to replace a failing component in the Computer Science House drink machines. ',
                'The software controlling the machines was previously written in java and running on Dallas TINI microcomputers. ',
                'These TINI\'s were failing and were no longer produced, so we re-wrote the software in python to run on a ',
                'Raspberry Pi. The software talks to the drink server over sockets using the SUNDAY protocol, and to the drink ',
                'machine hardware using the 1-Wire protocol and a usb 1-Wire bus master.']),
                ''.join(['<b>TempMon</b> - http://github.com/nickdepinet/tempmon/<br/>',
                'Implemented a temperature monitoring system for a server room using a Raspberry Pi. ',
                'The system monitors temperature using a series of DSB1820 temperature sensors. ',
                'When the temperature exceeds a set limit, an email notification is sent. ',
                'The software, including temperature reading, threading, and email notification is written in python.']),
                ''.join(['<b>Nexus Q Development</b> - http://github.com/nickdepinet/android_device_google_steelhead<br/>'])]}


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
            ['EDUCATION', Paragraph(data['education'], self.styles['Content'])],
            ['SKILLS', Paragraph(data['skills'], self.styles['Content'])],
            ['EXPERIENCE', [Paragraph(x, self.styles['Content']) for x in data['experience']]],
            ['PROJECTS', [Paragraph(x, self.styles['Content']) for x in data['projects']]]
            ]
        self.contact = contact

    def build_pdf(self):
        pdfname = 'resume.pdf'
        doc = SimpleDocTemplate(
            pdfname,
            pagesize=letter,
            bottomMargin=.5 * inch,
            topMargin=.7 * inch,
            rightMargin=.4 * inch,
            leftMargin=.4 * inch)  # set the doc template
        style = self.styles["Normal"]  # set the style to normal
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
            onFirstPage=self.myPageWrapper(
                self.contact)
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

    def generate(self):
        self.build_pdf()
