from datetime import datetime, date, timedelta
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
from faker.providers.misc import Provider as MiscProvider


state_codes = {
    'MI': ['231', '248', '269', '313', '517', '586', '616', '734', '810', '906', '947', '989'],
    'NE': ['308', '402'],
    'PA': ['215', '267', '412', '484', '570', '610', '717', '724', '814', '878'],
    'TN': ['423', '615', '731', '865', '901', '931']
}


class LocalizedPhoneAddressProvider(AddressProvider, PhoneProvider):
    
    def localize_address(self, state: str) -> str:
        return self.street_address(), self.city(), state, self.zipcode_in_state(state)

    def localize_phone(self, state: str) -> str:
        phone = self.phone_number()
        p = re.compile(r"(\d{3,3}){1,1}")
        return p.sub(random.choice(state_codes[state]), phone, count=1)


class Education():

    def __init__(self, uni, loc, start, end, major, type):
        self.uni = uni
        self.location = loc
        self.start_date = start
        self.end_date = end
        self.major = major
        self.type = type

    def __str__(self) -> str:
        return f"""\
        <b>{self.uni}</b> - {self.location}<br/>
        {self.type} {self.major}<br/>
        {date.strftime(self.start_date, '%B, %Y')} - {date.strftime(self.end_date, '%B, %Y')}
        """


class Job():

    def __init__(self, company, loc, start, end, title, desc):
        self.company = company
        self.location = loc
        self.start_date = start
        self.end_date = end
        self.title = title
        self.desc = desc

    def __str__(self) -> str:
        return f"""\
        <b>{self.company}</b> - {self.location}<br/>\
        <alignment=TA_RIGHT>{self.title}: {date.strftime(self.start_date, '%B, %Y')} - {date.strftime(self.end_date, '%B, %Y')}</alignment><br/>\
        {''.join(self.desc)}<br/>\
        """


class JobExperienceProvider(LoremProvider, JobProvider, CompanyProvider, AddressProvider, DatetimeProvider):

    def job_experience(self) -> str:
        start_date = self.date_this_decade(before_today=True)
        end_date = self.date_between(start_date=start_date)
        return Job(self.company(), f"{self.city()}, {self.country_code()}", start_date, end_date, self.job(), self.paragraphs(nb=3))

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
            'Accounting',
            'Advertising/ Media',
            'Agricultural Economics',
            'Agriculture/ Aquaculture/ Forestry',
            'Agriculture Engineering',
            'Air Conditioning/Refrigeration',
            'Airline Operation/ Airport Management',
            'Airplane Mechanics',
            'Animal Science/ Veterinary',
            'Anthropology',
            'Architecture',
            'Art/ Design/ Creative/ Multimedia',
            'Aviation/ Aeronautics/ Astronautics/ Aircraft Engineering',
            'Baking Science & Technology',
            'Behavioral Science',
            'Bioengineering/ Biomedical Engineering',
            'Biological Science',
            'Biology',
            'BioTechnology',
            'Business Studies/ Administration/ Management',
            'Chemical Engineering',
            'Chemistry',
            'Civil Engineering',
            'Commerce',
            'Commercial Design',
            'Communications/ Mass Communications',
            'Computer/ Telecommunication Engineering',
            'Computer Science/ Information Technology',
            'Counseling/ Guidance/ Vocational Career Development',
            'Criminal Justice',
            'Data Processing',
            'Dentistry',
            'Economics',
            'Education/ Teaching/ Training',
            'Electrical/ Electronic Engineering',
            'Engineering',
            'English/ English Literature',
            'Environmental/ Health/ Safety Engineering',
            'Environmental Health',
            'Finance/ Accountancy/ Banking',
            'Food & Beverage Services Management',
            'Food Science & Technology',
            'Food Technology/ Nutrition/ Dietetic',
            'Geographical Science',
            'Geology/ Geophysics',
            'Grain Processing',
            'Health/ Medicine/ Medical Science',
            'History',
            'Home Economics',
            'Hospitality/ Travel/ Tourism/ Hotel Management',
            'Humanities/ Liberal Arts',
            'Human Resource Management',
            'Industrial/ Labor Relations',
            'Industrial Design',
            'Industrial Engineering',
            'Industrial Technology',
            'Information Systems',
            'International Relations',
            'Journalism',
            'Law/ Juris Doctorate',
            'Library Management',
            'Life Sciences',
            'Linguistics/ Languages',
            'Logistic/ Transportation',
            'Marine Engineering',
            'Maritime Studies',
            'Marketing',
            'Material Science Engineering',
            'Mathematics',
            'Mechanical/ Electromechanical Engineering',
            'Medical Technology',
            'Metal Fabrication/ Tool & Die/ Welding Engineering',
            'Microbiology',
            'Mining/Mineral Engineering',
            'Music/ Performing Arts Studies',
            'Not Applicable',
            'Nursing',
            'Optometry',
            'Package Engineering',
            'Packaging',
            'Personal Services',
            'Petroleum/ Oil/ Gas Engineering',
            'Pharmacy/ Pharmacology',
            'Philosophy',
            'Physical Therapy/ Physiotherapy',
            'Physics',
            'Political Science',
            'Pre-Law',
            'Pre-Med',
            'Production/ Operations',
            'Property Development/ Real Estate Management',
            'Protective Services & Management',
            'Psychology',
            'Quantitative Analysis',
            'Radio/ TV/ Film',
            'Retailing',
            'Safety & Construction',
            'Science',
            'Secretarial',
            'Selling/ Sales Management/ Retail',
            'Social Science/ Sociology',
            'Social Welfare',
            'Sociology',
            'Speech Pathology',
            'Sports Science & Management',
            'Statistics',
            'Taxation',
            'Textile/ Fashion Design',
            'Theology',
            'Traffic',
            'Urban Studies'
        )))

    def education(self) -> str:
        start_date = self.date_this_decade(before_today=True).replace(day=1)
        end_date = self.date_between(start_date=start_date).replace(day=1)
        uni = self.random_university()
        major = self.random_major()
        return Education(uni[0], uni[1], start_date, end_date, major[1], major[0])
    
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
fake.add_provider(MiscProvider)


class FakeIdentity():

    def __init__(self):
        self.gender = random.choice(('M', 'F'))
        self.title = 'Mr.' if self.gender == 'M' else 'Ms.'
        self.street_address, self.city, self.state, self.zipcode_in_state = fake.localize_address(random.choice(list(state_codes.keys())))
        self.first_name = fake.first_name_male() if self.gender == 'M' else fake.first_name_female()
        self.last_name = fake.last_name()
        self.name = f"{self.first_name} {self.last_name}"
        self.website = f"http://github.com/{self.name.lower().replace(' ', '')}/"
        self.email = f"{self.name.lower().replace(' ', '')}@{fake.free_email_domain()}"
        self.phone = fake.localize_phone(self.state)
        self.objective = fake.paragraph(nb_sentences=3)
        self.summary = fake.paragraph(nb_sentences=3)
        self.education = fake.education_curricula(n=2, n_random=True)
        self.work_experience = fake.job_curricula(n=3, n_random=True)
        self.pwd = fake.password()
        self.availability_date = self.calc_availability_date()

    def _build_address(self):
        return f"{self.street_address}, {self.city}, {self.state} {self.zipcode_in_state}"

    def calc_availability_date(self):
        max_date = max([e.end_date for e in self.education] + [w.end_date for w in self.work_experience])
        max_date = max(max_date, datetime.now().date())
        return fake.date_between(max_date + timedelta(days=10), max_date + timedelta(days=60))

    def contacts(self):
        return {
            'name': self.name,
            'website': self.website,
            'email': self.email,
            'phone': self.phone,
            'address': self._build_address()
        }

    def curriculum(self):
        return {
            'objective': self.objective,
            'summary': self.summary,
            'education': [str(edu) for edu in self.education],
            'experience': [str(exp) for exp in self.work_experience]
        }


if __name__ == '__main__':
    print(FakeIdentity().availability_date)