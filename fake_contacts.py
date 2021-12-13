import datetime
from math import ceil
import random
import re
from faker import Faker
from faker.providers.date_time import Provider as DatetimeProvider
from faker.providers.phone_number.en_US import Provider as PhoneProvider
from faker.providers.internet import Provider as InternetProvider
from faker.providers.address.en_US import Provider as AddressProvider
from faker.providers.company.en_US import Provider as CompanyProvider
from faker.providers.job.en_US import Provider as JobProvider
from faker.providers.lorem.en_US import Provider as LoremProvider


state_codes = {
    'MI': ['231', '248', '269', '313', '517', '586', '616', '734', '810', '906', '947', '989'],
    'NE': ['308', '402'],
    'PA': ['215', '267', '412', '484', '570', '610', '717', '724', '814', '878'],
    'TN': ['423', '615', '731', '865', '901', '931']
}


class LocalizedPhoneAddressProvider(AddressProvider, PhoneProvider):
    
    def localize_address(self, state: str) -> str:
        return f"{self.street_address()}, {self.city()}, {state} {self.zipcode_in_state(state)}"

    def localize_phone(self, state: str) -> str:
        phone = self.phone_number()
        p = re.compile(r"(\d{3,3}){1,1}")
        return p.sub(random.choice(state_codes[state]), phone, count=1)

    def localize_contacts(self, state: str) -> dict:
        return {
            'phone': self.localize_phone(state),
            'address': self.localize_address(state)
        }


class JobExperienceProvider(LoremProvider, JobProvider, CompanyProvider, AddressProvider, DatetimeProvider):

    def job_experience(self) -> str:
        start_date = self.date_this_decade(before_today=True)
        end_date = self.date_between(start_date=start_date)
        start_date = datetime.date.strftime(start_date, '%B, %Y')
        end_date = datetime.date.strftime(end_date, '%B, %Y')
        job = f"""\
        <b>{self.company()}</b> - {self.city()}, {self.country_code()}<br/>\
        <alignment=TA_RIGHT>{self.job()}: {start_date} - {end_date}</alignment><br/>\
        {''.join(self.paragraphs(nb=3))}<br/>\
        """
        return job

    def job_curricula(self, n: int = 3, n_random: bool = False) -> str:
        if n_random:
            n = ceil((0.60 + random.random() * 0.80) * n)
        return [self.job_experience() for _ in range(n)]


class EducationProvider(LoremProvider, AddressProvider, DatetimeProvider):

    def random_university(self):
        return random.choice((
            ('Rochester Insitute of Technology', 'Rochester, New York'),
            ('Massachusetts Insitute of Technology', 'Cambridge, MA'),
            ('Georgia Insitute of Technology', 'Atlanta, Georgia'),
            ('Princeton University', 'Princeton, NJ'),
            ('Harvard University', 'Cambridge, MA'),
            ('Columbia University', 'New York, NY'),
            ('Yale University', 'New Haven, CT'),
            ('Duke University', 'Durham, NC'),
            ('California Institute of Technology', 'Pasadena, CA'),
            ('University of Pennsylvania', 'Philadelphia, PA'),
            ('Stanford University', 'Stanford, CA'),
            ('University of Chicago', 'Chicago, IL'),
            ('Johns Hopkins University', 'Baltimore, MD'),
            ('Northwestern University', 'Evanston, IL'),
            ('Dartmouth College', 'Hanover, NH')
        ))
    
    def random_major(self):
        type = random.choice(('M.Sc. ', 'B.Sc. '))
        return (type, random.choice((
            'Animal Science'
            ,'Anthropology'
            ,'Architecture'
            ,'Astronomy'
            ,'Biochemistry'
            ,'Biological Sciences'
            ,'Biology'
            ,'Biomedical Engineering'
            ,'Business'
            ,'Business Administration'
            ,'Chemistry'
            ,'Cognitive Science'
            ,'Communications'
            ,'Computer Engineering'
            ,'Computer and Information Science'
            ,'Computer Science'
            ,'Criminal Justice'
            ,'Criminology'
            ,'Economics'
            ,'Education'
            ,'Engineering'
            ,'English'
            ,'Film'
            ,'Finance'
            ,'Geography'
            ,'Geology'
            ,'Health Science'
            ,'History'
            ,'Human Biology'
            ,'Human Resources'
            ,'Human Services'
            ,'International Business'
            ,'International Relations'
            ,'International Studies'
            ,'Journalism'
            ,'Linguistics'
            ,'Management Information Systems and Services'
            ,'Marketing'
            ,'Mathematics'
            ,'Mechanical Engineering'
            ,'Music'
            ,'Nursing'
            ,'Nutrition'
            ,'Pharmacy'
            ,'Philosophy'
            ,'Physics'
            ,'Physiology'
            ,'Political Science'
            ,'Psychology'
            ,'Public Health'
            ,'Public Policy'
            ,'Real Estate'
            ,'Social Work'
            ,'Sociology'
            ,'Statistics'
            ,'Zoology'
        )))

    def education(self) -> str:
        uni = self.random_university()
        major = self.random_major()
        edu = f"""\
        <b>{uni[0]}</b> - {uni[1]}<br/>
        <b>{major[0]}</b>  {major[1]}<br/>
        """
        return edu
    
    def education_curricula(self, n: int = 3, n_random: bool = False) -> str:
        if n_random:
            n = ceil((0.60 + random.random() * 0.80) * n)
        return [self.education() for _ in range(n)]


fake = Faker('en_US')
fake.add_provider(DatetimeProvider)
fake.add_provider(InternetProvider)
fake.add_provider(LoremProvider)
fake.add_provider(LocalizedPhoneAddressProvider)
fake.add_provider(JobExperienceProvider)
fake.add_provider(EducationProvider)


class FakeIdentity():

    def __init__(self):
        self.state = random.choice(list(state_codes.keys()))
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.name = f"{self.first_name} {self.last_name}"
        self.website = f"http://github.com/{self.name.lower().replace(' ', '')}/"
        self.email = f"{self.name.lower().replace(' ', '')}@{fake.free_email_domain()}"
        self.phone = fake.localize_phone(self.state)
        self.address = fake.localize_address(self.state)
        self.objective = fake.paragraph(nb_sentences=3)
        self.summary = fake.paragraph(nb_sentences=3)
        self.education = fake.education_curricula(n=2, n_random=True)
        self.experience = fake.job_curricula(n=3, n_random=True)


    def contacts(self):
        return {
            'name': self.name,
            'website': self.website,
            'email': self.email,
            'phone': self.phone,
            'address': self.website
        }

    def curriculum(self):
        return {
            'objective': self.objective,
            'summary': self.summary,
            'education': self.education,
            'experience': self.experience
        }


if __name__ == '__main__':
    print(FakeIdentity().contacts())