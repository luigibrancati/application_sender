from typing import final
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
from utils import delay
import logging
import time
import os
from datetime import datetime


class KellogsApplication():
    _TIMEOUT = 30
    _URLS = {
        'NE': "https://jobs.kellogg.com/job/Omaha-Permanent-Production-Associate-Omaha-NE-68103/817685900/z",
        'MI': "https://jobs.kellogg.com/job/Battle-Creek-Permanent-Production-Associate-Battle-Creek-MI-49014/817685300/",
        'PA': "https://jobs.kellogg.com/job/Lancaster-Permanent-Production-Associate-Lancaster-PA-17601/817684800/",
        'TN': "https://jobs.kellogg.com/job/Memphis-Permanent-Production-Associate-Memphis-TN-38114/817685700/"
    }

    def __init__(self, driver, state, resume_path):
        self.driver = driver
        self.driver.implicitly_wait(10)
        self.url = KellogsApplication._URLS[state]
        self.resume_path = resume_path
    
    @staticmethod
    @delay()
    def _send_keys(el, keys):
        el.clear()
        el.send_keys(keys)

    @delay(t=2)
    def _wait_element(self, locator):
        try:
            WebDriverWait(self.driver, KellogsApplication._TIMEOUT).until(
                EC.presence_of_element_located(locator)
            )
            WebDriverWait(self.driver, KellogsApplication._TIMEOUT).until(
                EC.element_to_be_clickable(locator)
            )
            WebDriverWait(self.driver, KellogsApplication._TIMEOUT).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logging.error("timeout")
            self.driver.quit()
            exit(1)

    def driver_connect(self):
        # Connect to url
        logging.info("Connecting to url %s" % self.url)
        self.driver.get(self.url)

    def accept_cookie(self):
        # Accept cookie if present
        logging.info("Accepting cookies")
        try:
            self.driver.find_element(By.ID, "cookie-acknowledge").click()
            logging.info("Cookies accepted")
        except NoSuchElementException:
            logging.info("Cookies accept button not found")
            pass

    def new_application(self):
        logging.info("Searching the button to start a new application")
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary.btn-large.btn-lg.dropdown-toggle').click()
            self.driver.find_element(By.ID, 'applyOption-top-manual').click()
            logging.info("Started a new application")
        except:
            logging.error("Button to start a new application not found")
            self.driver.quit()
            exit(1)

    def create_new_account(self):
        # Click link to create new account
        logging.info("Creating a new account")
        try:
            self._wait_element(self.driver, KellogsApplication._TIMEOUT, (By.CSS_SELECTOR, '.bottomLink a'))
            WebDriverWait(self.driver, KellogsApplication._TIMEOUT).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "loading_indicator_layout_static"))
            )
            self.driver.find_element(By.CSS_SELECTOR, '.bottomLink a').click()
            logging.info("Started process to create a new account")
        except NoSuchElementException:
            logging.error("Could not find the link to create a new account")
            self.driver.quit()
            exit(1)
        except TimeoutException:
            logging.error("timeout")
            self.driver.quit()
            exit(1)

    def fill_new_account_info(self, fake_id):
        # Filling new account infos
        logging.info("Filling fake id infos into new account")
        self._wait_element(self.driver, KellogsApplication._TIMEOUT, (By.ID, "fbclc_userName"))
        self._send_keys(self.driver.find_element(By.ID, "fbclc_userName"), fake_id.email)
        self._send_keys(self.driver.find_element(By.ID, "fbclc_emailConf"), fake_id.email)
        self._send_keys(self.driver.find_element(By.ID, "fbclc_pwd"), fake_id.pwd)
        self._send_keys(self.driver.find_element(By.ID, "fbclc_pwdConf"), fake_id.pwd)
        self._send_keys(self.driver.find_element(By.ID, "fbclc_fName"), fake_id.first_name)
        self._send_keys(self.driver.find_element(By.ID, "fbclc_lName"), fake_id.last_name)
        self._send_keys(self.driver.find_element(By.ID, "fbclc_phoneNumber"), fake_id.phone)
        Select(self.driver.find_element(By.ID, "fbclc_ituCode")).select_by_value('US')
        Select(self.driver.find_element(By.ID, "fbclc_country")).select_by_value('US')

    def solve_captcha(self):
        logging.info("Starting CAPTCHA")
        logging.info("CAPTCHA must be solved by hand")
        # Must be done by hand unfortunately
        logging.info("Finding CAPTCHA iframe")
        self._wait_element(self.driver, KellogsApplication._TIMEOUT, (By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]'))
        self.driver.execute_script("document.getElementById('dataPrivacyId').scrollIntoView(true);")
        logging.info("Switching to CAPTCHA iframe")
        self.driver.switch_to.frame(self.driver.find_element(By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]'))
        logging.info("Clicking CAPTCHA spinner")
        spinner = self.driver.find_element(By.CLASS_NAME, "recaptcha-checkbox-border")
        spinner.click()
        time.sleep(2)
        logging.info("Switching back to main window")
        self.driver.switch_to.default_content()
        try:
            logging.info("Waiting for CAPTCHA to be solved")
            WebDriverWait(self.driver, 4*KellogsApplication._TIMEOUT).until_not(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'iframe[title="recaptcha challenge expires in two minutes"]'))
            )
        except TimeoutException:
            logging.error("timeout")
            self.driver.quit()
            exit(1)
        time.sleep(2)
        logging.info("Accepting privacy")
        self._wait_element(self.driver, KellogsApplication._TIMEOUT, (By.ID, "dataPrivacyId"))
        self.driver.find_element(By.ID, "dataPrivacyId").click()
        self.driver.find_element(By.ID, "dlgButton_20:").click()
        self.driver.find_element(By.ID, "fbclc_createAccountButton").click()
        logging.info("Account created")

    def load_resume(self):
        # Loading resume
        logging.info("Loading resume")
        try:
            self._wait_element(self.driver, KellogsApplication._TIMEOUT, (By.CLASS_NAME, "attachActions"))
            self.driver.find_element(By.CLASS_NAME, "attachActions").click()
            self._send_keys(self.driver.find_element(By.ID, "49:_file"), os.path.abspath(self.resume_path)) # Upload Resume
        except Exception as e:
            logging.error(f"Error while loading resume: {e}")
            self.driver.quit()
            exit(1)   
        logging.info("Resume has been loaded")

    def fill_profile_info(self, fake_id):
        # Filling missing profile infos
        logging.info("Filling out profile and candidate infos")
        self._wait_element(self.driver, KellogsApplication._TIMEOUT, (By.NAME, "currentTitle"))
        self._send_keys(self.driver.find_element(By.NAME, "currentTitle"), fake_id.title) # Title
        self._wait_element(self.driver, KellogsApplication._TIMEOUT, (By.NAME, "citizen"))
        Select(self.driver.find_element(By.NAME, "citizen")).select_by_visible_text("Yes") # Citizen of US
        self.driver.find_element(By.NAME, "expectedSalaryRange").self._send_keys("100000") # Salary expectation
        Select(self.driver.find_element(By.NAME, "candidateSource")).select_by_value("3217000") # Source for job posting
        Select(self.driver.find_element(By.NAME, "presentEmployer")).select_by_value("299") # Kellog is present employer

    def fill_equal_employment(self, fake_id):
        # Filling EE infos
        logging.info("Filling out equal employement infos")
        self._wait_element(self.driver, KellogsApplication._TIMEOUT, (By.NAME, "custCountry"))
        Select(self.driver.find_element(By.NAME, "custCountry")).select_by_value("3206850") # Country of origin
        Select(self.driver.find_element(By.NAME, "veteranStatus")).select_by_value("299") # Veteran
        Select(self.driver.find_element(By.NAME, "disabilityStatus")).select_by_value("299") # Disability
        Select(self.driver.find_element(By.NAME, "custAge")).select_by_value("298") # Age 18+
        Select(self.driver.find_element(By.NAME, "cust_sponsor")).select_by_value("299") # Sponsorship
        Select(self.driver.find_element(By.NAME, "custPrev")).select_by_value("299") # Worked for kellogs
        Select(self.driver.find_element(By.NAME, "custcontr")).select_by_value("299") # Contractor for Kellogs
        Select(self.driver.find_element(By.NAME, "custRel")).select_by_value("299") # Relative for kellogs
        Select(self.driver.find_element(By.NAME, "custAccom")).select_by_value("298") # Accomodation
        Select(self.driver.find_element(By.NAME, "custgender")).select_by_value("71046" if fake_id.gender == 'F' else "71047") # Gender
        Select(self.driver.find_element(By.NAME, "disabilityselection")).select_by_value("71280") # Disability 2

    def fill_questionnaire(self):
        # Solving questionnaire
        logging.info("Filling out math questionnaire")
        for i, rg in enumerate(self.driver.find_elements(By.CLASS_NAME, 'radioGroup')):
            for c in rg.find_elements_by_class_name('sfRadioInputField'):
                if i == 0 and c.text == 'Yes':
                    c.find_element_by_tag_name('a').click()
                if i == 1 and c.text == '350 LBS':
                    c.find_element_by_tag_name('a').click()
                if i == 2 and c.text == '800 LBS':
                    c.find_element_by_tag_name('a').click()
                if i == 3 and c.text == 'Yes':
                    c.find_element_by_tag_name('a').click()

    def fill_missing_infos(self, fake_id, faker):
        # Filling infos usually missing
        logging.info("Filling out status of education")
        [Select(el).select_by_value('296') for el in self.driver.find_elements(By.NAME, 'VFLD4')]
        logging.info("Checking for missing fields")
        for div in self.driver.find_elements(By.CSS_SELECTOR, 'div.rcmFormSection.row'):
                h2 = div.find_element_by_tag_name('h2')
                if h2.text == 'Formal Education':
                    logging.info("Adding fields usually missing from education")
                    for i, uni in enumerate(div.find_elements_by_css_selector('.sectionContentOpen.sectionContent.rcmFormSectionContent div.row div.row')):
                        type = Select(uni.find_element_by_name('VFLD3'))
                        type.select_by_value("197" if 'B' in fake_id.education[i].type else "357")
                        major = Select(uni.find_element_by_name('VFLD2'))
                        index = [o.text for o in major.options].index(fake_id.education[i].major)
                        if index:
                            logging.info("Added major %s %s to education row %i" % (fake_id.education[i].type, fake_id.education[i].major, i))
                            major.select_by_index(index)
                        else:
                            logging.info("Couldn't find major %s %s in education row %i" % (fake_id.education[i].type, fake_id.education[i].major, i))
                elif h2.text == 'Candidate-Specific Information':
                    logging.info("Added major %s %s to education row %i" % (fake_id.education[i].type, fake_id.education[i].major, i))
                    try:
                        datepicker = div.find_element_by_css_selector('div.row span.datepicker input')
                        datepicker.click()
                        datepicker.clear()
                        self._send_keys(datepicker, datetime.strftime(fake_id.availability_date, '%m/%d/%Y')) # Date available
                        logging.info("Set availability")
                    except NoSuchElementException:
                        logging.info("Couldn't find availability datepicker")
                        pass

    def apply(self):
        # Click the submit button
        logging.info("Submitting application")
        for button in self.driver.find_elements(By.CLASS_NAME, 'rcmSaveButton'):
            if 'submit' in button.get_attribute('onclick'):
                button.click()
                logging.info("Application submitted")
                break

    def close(self):
        logging.info("Closing driver")
        self.driver.close()

    def submit(self, fake_id):
        self.driver_connect()
        self.accept_cookie()
        self.new_application()
        self.create_new_account()
        self.fill_new_account_info(fake_id)
        self.solve_captcha()
        time.sleep(2)
        self.load_resume()
        self.fill_profile_info(fake_id)
        self.fill_equal_employment(fake_id)
        self.fill_questionnaire()
        self.fill_missing_infos(fake_id)
        self.apply()
        self.close()