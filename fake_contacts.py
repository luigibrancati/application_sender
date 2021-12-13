from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
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
        {date.strftime(self.start_date, '%B, %Y')} - {date.strftime(self.end_date, '%B, %Y') if self.end_date else 'current'}
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
        <alignment=TA_RIGHT>{self.title}: {date.strftime(self.start_date, '%B, %Y')} - {date.strftime(self.end_date, '%B, %Y') if self.end_date else 'current'}</alignment><br/>\
        {''.join(self.desc)}<br/>\
        """


class JobExperienceProvider(LoremProvider, JobProvider, CompanyProvider, AddressProvider, DatetimeProvider):

    def random_job_duration(self) -> int:
        return random.randint(2, 24)

    def random_job_experience(self, start_dt: datetime=None, duration: int=None) -> Job:        
        if start_dt:
            start_date = start_dt
        else:
            start_date = self.date_this_decade(before_today=True)

        end_date = start_date
        if duration:
            end_date = end_date + relativedelta(months=duration)
        else:
            end_date = self.date_between(start_date=start_date)

        return Job(self.company(), f"{self.city()}, {self.country_code()}", start_date, end_date, self.job(), self.paragraphs(nb=3))

    def random_job_curriculum(self, n: int = 3, n_random: bool = False) -> str:
        if n_random:
            n = ceil((0.60 + random.random() * 0.80) * n)
        return [self.random_job_experience() for _ in range(n)]


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
    
    def random_major(self, grade=None):
        if grade:
            maj_grade = 'B.Sc. ' if 'B' in grade else 'M.Sc. '
        else:
            maj_grade = random.choice(('M.Sc. ', 'B.Sc. '))
        return (maj_grade, random.choice((
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

    def random_maj_duration(self, maj_grade: str) -> int:
        return (36 if 'B' in maj_grade else 24) + random.randint(-2, 6)

    def random_education(self, start_year: int=None, maj_grade: str='', duration: int=None) -> Education:
        uni = self.random_university()
        major = self.random_major(maj_grade)
        
        if start_year:
            start_date = date(start_year, 9, 1)
        else:
            start_date = self.date_this_decade(before_today=True).replace(day=1, month=9)
        
        end_date = start_date
        if duration:
            end_date = end_date + relativedelta(months=duration)
        else:
            end_date = end_date + relativedelta(months=self.random_maj_duration(major[0]))

        return Education(uni[0], uni[1], start_date, end_date, major[1], major[0])
    
    def random_education_curriculum(self, n: int = 3, n_random: bool = False) -> str:
        if n_random:
            n = ceil((0.60 + random.random() * 0.80) * n)
        return [self.random_education() for _ in range(n)]

class CurriculumProvider(EducationProvider, JobExperienceProvider):
    
    def random_curriculum(self, n_edu: int=2, n_jobs: int=2, n_random: bool=True):
        if n_random:
            n_edu = ceil((0.60 + random.random() * 0.80) * n_edu)
            n_jobs = ceil((0.60 + random.random() * 0.80) * n_jobs)
        job_months = [self.random_job_duration() for _ in range(n_jobs)]
        grades = ['B'] + [random.choice(['B', 'M']) for _ in range(n_edu-1)]
        edu_months = [fake.random_maj_duration(g) for g in grades]
        total_months = sum(edu_months)+sum(job_months)
        start_date = datetime.now().date() - relativedelta(months=total_months) - relativedelta(years=1)

        edu_curr = []
        job_curr = []
        for i in range(n_edu):
            ec = fake.random_education(start_year=start_date.year, maj_grade=grades[i], duration=edu_months[i])
            edu_curr.append(ec)
            start_date = ec.end_date
        for i in range(n_jobs):
            job = fake.random_job_experience(start_dt=start_date, duration=job_months[i])
            job_curr.append(job)
            start_date = job.end_date
        return edu_curr, job_curr


fake = Faker('en_US')
fake.add_provider(DatetimeProvider)
fake.add_provider(InternetProvider)
fake.add_provider(LoremProvider)
fake.add_provider(LocalizedPhoneAddressProvider)
fake.add_provider(JobExperienceProvider)
fake.add_provider(EducationProvider)
fake.add_provider(MiscProvider)
fake.add_provider(CurriculumProvider)


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
        self.education, self.work_experience = fake.random_curriculum()
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
    print(FakeIdentity().curriculum())