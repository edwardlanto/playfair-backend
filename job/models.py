import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import date
from ckeditor.fields import RichTextField
from company.models import Company
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Education(models.TextChoices):
    Bachelors = 'Bachelors'
    Masters = 'Masters'
    Phd = 'Phd'

class RateType(models.TextChoices):
    Salary = 'Salary'
    Hourly = 'Hourly'

class Industry(models.TextChoices):
    Accounting = 'Accounting'
    Advertising = 'Advertising'
    Agriculture = 'Agriculture'
    Architecture = 'Architecture'
    Arts = 'Arts'
    Automative = 'Automative'
    Banking = 'Banking'
    Biotechnology = 'Biotechnology'
    Business = 'Business'
    BusinessDevelopment = 'Business Development'
    Chemical = 'Chemical'
    Construction = 'Construction'
    Consulting = 'Consulting'
    ConsumerServices = 'Consumer Services'
    CustomerService = 'Customer Service'
    DataEntry = 'Data Entry'
    Design = 'Design'
    Education = 'Education'
    Energy = 'Energy'
    Engineering = 'Engineering'
    Entertainment = 'Entertainment'
    Environmental = 'Environmental'
    EventPlanning = 'Event Planning'
    Fashion = 'Fashion'
    Finance = 'Finance'
    FoodServices = 'Food Services'
    Gaming = 'Gaming'
    Government = 'Government'
    Graphics = 'Graphics'
    HealthBeauty = 'Health & Beauty'
    Healthcare = 'Healthcare'
    Hospitality = 'Hospitality'
    HumanResources = 'Human Resources'
    InformationTechnology = 'Information Technology'
    Insurance = 'Insurance'
    InteriorDesign = 'Interior Design'
    Investment = 'Investment'
    Journalism = 'Journalism'
    Legal = 'Legal'
    LegalServices = 'Legal Services'
    Logistics = 'Logistics'
    Manufacturing = 'Manufacturing'
    Marketing = 'Marketing'
    Media = 'Media'
    Military = 'Military'
    Music = 'Music'
    Nonprofit = 'Nonprofit'
    Operations = 'Operations'
    Pharmaceutical = 'Pharmaceutical'
    Photography = 'Photography'
    ProductManagement = 'Product Management'
    ProjectManagement = 'Project Management'
    PublicHealth = 'Public Health'
    PublicRelations = 'Public Relations'
    QualityAssurance = 'Quality Assurance'
    RealEstate = 'Real Estate'
    Research = 'Research'
    Restaurant = 'Restaurant'
    Retail = 'Retail'
    Sales = 'Sales'
    Science = 'Science'
    Security = 'Security'
    SocialServices = 'Social Services'
    Software = 'Software'
    Sports = 'Sports'
    SupplyChain = 'Supply Chain'
    Telecommunications = 'Telecommunications'
    Tourism = 'Tourism'
    Training = 'Training'
    Transportation = 'Transportation'
    Travel = 'Travel'
    Utilities = 'Utilities'
    Video = 'Video'
    WealthManagement = 'Wealth Management'
    WritingTranslation = 'Writing & Translation'

class Experience(models.TextChoices):
    NO_EXPERIENCE = 'No Experience'
    ONE_YEAR = '1 Year'
    TWO_YEAR = '2 Years'
    THREE_YEAR = '3 Years'
    FOUR_YEAR = '4 Years'
    FIVE_YEAR_PLUS = '5 Years+'

def return_date_time():
    now = datetime.datetime.now()
    return now 

class Job(models.Model):
    id = models.CharField(max_length = 50, default = uuid.uuid4, primary_key = True, editable = False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200, null=True)
    applied_count = models.CharField(max_length=200, null=True, default=0, blank=True)
    description = RichTextField(blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    candidates = ArrayField(models.JSONField(null=True), blank=True)
    featured = models.BooleanField(default=False, auto_created=False)
    is_commission = models.BooleanField(default=False, auto_created=False)
    expired_at = models.DateField(default=date.today, auto_now=False)
    address = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True)
    work_status = models.CharField(max_length=20, default="Full-Time")
    type = ArrayField(models.JSONField(), blank=True, null=True)
    education = models.CharField(
        max_length=100,
        choices=Education.choices,
        default=Education.Bachelors
    )
    rate_type = models.CharField(
        max_length=100,
        choices=RateType.choices,
        default=RateType.Salary
    )
    city = models.CharField(max_length=100, null=True)
    industry = models.CharField(max_length=100, null=True, default='Sales')
    experience = models.CharField(
        max_length=100,
        choices=Experience.choices,
        default=Experience.NO_EXPERIENCE
    )
    min_salary = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    max_salary = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(1000000)], null=True)
    positions = models.IntegerField(default=1)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name="company", blank=True)
    responsibilities = RichTextField(blank=True, null=True)
    skills = ArrayField(models.JSONField(), blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null=True)
    created_date = models.DateField(auto_now_add=True, null=True)
    start_date = models.DateField(null=True, default=datetime.date.today)
    weekly_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, default=0.00)
    is_active = models.BooleanField(default=True, auto_created=True)
    is_remote = models.BooleanField(default=False, auto_created=True)
    
class JobCategories(models.Model):
    jobCategory_title = models.CharField(max_length=200, null=True)

class JobCategory(models.Model):
    jobCategory_title = models.CharField(max_length=200, null=True)
    jobCategory_count = models.IntegerField(default=0)

class CandidatesCoverLetter(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    coverLetter = models.CharField(max_length=3000, null=True)
    resume = models.CharField(max_length=200)