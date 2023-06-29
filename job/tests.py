from django.test import TestCase
from .models import Job, Education, Industry, Experience
from django.utils import timezone
import datetime
import pytest

class ModelTesting(TestCase):
        # @pytest.mark.django_db
        def create_test_job(self):
                self.job = Job()
                self.job.title = "Software Developer"
                self.job.applied_count = 0
                self.job.description = "We are seeking a skilled software developer to join our team."
                self.job.email = "info@example.com"
                self.job.candidates = []
                self.job.featured = False
                self.job.is_commission = False
                self.job.expired_at = timezone.now() + datetime.timedelta(days=30)
                self.job.address = "123 Main St"
                self.job.country = "United States"
                self.job.facebook = "https://www.facebook.com/example"
                self.job.twitter = "https://twitter.com/example"
                self.job.state = "California"
                self.job.type = ["Full-time", "Remote"]
                self.job.education = Education.Bachelors
                self.job.city = "Los Angeles"
                self.job.industry = Industry.Technology
                self.job.experience = Experience.TWO_YEAR
                self.job.min_salary = 50000
                self.job.max_salary = 80000
                self.job.positions = 2
                self.job.company_id = 1
                self.job.responsibilities = "Develop and maintain software applications."
                self.job.skills = "Python, Django, JavaScript"
                self.job.lat = 34.052235
                self.job.long = -118.243683
                self.job.user_id = 1
                self.job.created_date = timezone.now().date()
                self.job.start_date = timezone.now().date()
                self.job.weekly_hours = 40.0
                self.job.is_active = True
                self.job.is_remote = True

                self.job.save()
                return self.job