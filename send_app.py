from selenium import webdriver
from resume import ResumeGenerator
from fake_contacts import FakeIdentity
from kellogs_app import KellogsApplication
import logging
from datetime import datetime

log_name = f"app_{datetime.now()}.log"
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.DEBUG)

fake_id = FakeIdentity()
resume = ResumeGenerator(fake_id.curriculum(), fake_id.contacts())
resume.generate()

application = KellogsApplication(webdriver.Firefox(), fake_id.state, './resume.pdf')
application.submit()