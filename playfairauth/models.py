from xmlrpc.client import ResponseError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4
from django.utils import timezone
import uuid
from django.utils.timezone import now
from company.models import Company
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from phone_field import PhoneField
from django.db.models.signals import post_save, pre_save
from ckeditor.fields import RichTextField
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

class CustomUserModelManager(BaseUserManager):
  def create_user(self, username, email, password=None, account_type="", first_name="", last_name=""):
    """
      Creates a custom user with the given fields
    """

    if CustomUserModel.objects.filter(email=email).exists():
      raise ResponseError({"error": "Email already exists"})
    
    user = self.model(
      username = username,
      email = self.normalize_email(email),
      account_type = account_type,
      first_name = first_name,
      last_name = last_name
    )

    user.set_password(password)
    user.save(using = self._db)

    return user
  
  def create_superuser(self, email, password):

    if password is None:
        raise TypeError('Superusers must have a password.')

    user = self.create_user(email, email, password)
    user.is_superuser = True
    user.is_staff = True
    user.save()

    return user

class CustomUserModel(AbstractBaseUser, PermissionsMixin):
  id = models.CharField(max_length = 50, default = uuid4, primary_key = True, editable = False)
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  username = models.CharField(max_length = 50, unique = True, null = True, blank = False)
  email = models.EmailField(max_length = 100, unique = True, null = False, blank = False)
  auth_provider = models.CharField(max_length=50, blank=True, default='email')
  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []
  forgot_password_token = models.CharField(max_length = 200, editable = False, null=True, unique=True)
  forgot_password_timestamp = models.DateTimeField(null=True)
  first_name = models.CharField(max_length=30, blank=True)
  last_name = models.CharField(max_length=50, blank=True)
  date_joined = models.DateTimeField(default=timezone.now)
  is_active = models.BooleanField(default=True)
  is_deleted = models.BooleanField(default=False)
  created_date = models.DateTimeField(default=timezone.now)
  modified_date = models.DateTimeField(default=timezone.now)
  status = models.CharField(max_length=100, default="Active")
  is_candidate = models.BooleanField(default=False)
  is_employer = models.BooleanField(default=False)
  account_type = models.CharField(max_length=100, default="candidate")
  is_staff  = models.BooleanField(default = False)
  is_superuser = models.BooleanField(default = False)
  image = models.FileField(null=True)
  is_complete = models.BooleanField(default = False)
  objects = CustomUserModelManager()

  class Meta:
    verbose_name = "Custom User"

class CustomUserProfile(models.Model):
    id = models.CharField(max_length = 50, default = uuid.uuid4, primary_key = True, editable = False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey("playfairauth.CustomUserModel", related_name="userprofile", on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    resume = models.FileField(null=True)
    address = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=10, default="", null=True)
    bio = RichTextField(null=True, default="")
    phone = PhoneField(blank=True, help_text='Contact phone number')
    country = models.JSONField(null=True)
    city = models.JSONField(null=True)
    state = models.JSONField(null=True)
    website = models.URLField(max_length = 200, default="", null=True)
    linkedIn = models.CharField(max_length=100, default="", null=True)
    instagram = models.CharField(max_length=100, default="", null=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100, null=True)
    education_level = models.CharField(max_length=100, default="", null=True)
    rating = models.CharField(max_length=5, null=True)
    unit = models.CharField(max_length=10, null=True)
    logo = models.FileField(null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, default="")
    # education = models.JSONField(null=True)
    experience = models.CharField(max_length=100, null=True, default="")
    is_age_visible = models.BooleanField(default=True)
    languages = ArrayField(models.JSONField(), default=list)
    skills = ArrayField(models.JSONField(), null=True)
    interests = ArrayField(models.JSONField(), null=True)
    allow_in_listings = models.BooleanField(default=False)
    first_logged_in = models.BooleanField(default=False)
    age = models.IntegerField(default=16)
    expected_salary = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    current_salary = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    dob = models.DateField(null=True)
    is_candidate = models.BooleanField(default=False)
    is_expected_salary_visible = models.BooleanField(default=True)
    created_date =  models.DateTimeField(default=now )
    is_complete = models.BooleanField(default = False)
    stripe_account = models.CharField(max_length=100, null=True, blank=True)
    stripe_bank_token = models.CharField(max_length=100, null=True, blank=True)
    stripe_person = models.CharField(max_length=50, null=True, blank=True)
    stripe_id_front = models.CharField(max_length=50, null=True, blank=True)
    stripe_id_back = models.CharField(max_length=50, null=True, blank=True)
    
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

# @receiver(post_save, sender=CustomUserModel)
# def save_company(sender, instance, created, **kwargs):
#     user = instance
#     current_user = CustomUserModel.objects.get(id=user.id)
#     if created:
#         company = Company(user=user)
#         company.save()