from selenium import webdriver
from build_resume import ResumeGenerator
from fake_contacts import FakeIdentity
from kellogs_app import KellogsApplication
import logging
from datetime import datetime

log_name = f"./logs/app_{datetime.now()}.log"
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.INFO)

fake_id = FakeIdentity()
resume = ResumeGenerator(fake_id.curriculum(), fake_id.contacts())
resume.generate()

application = KellogsApplication(webdriver.Firefox(), fake_id.state, './resume.pdf')
application.submit(fake_id)
