from resume import ResumeGenerator
from fake_contacts import FakeIdentity

fake_id = FakeIdentity()
resume = ResumeGenerator(fake_id.curriculum(), fake_id.contacts())
resume.generate()