
from django.db import models
from django.utils import timezone
# Create your models here.
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
    
# Custom user model
class CustomUser(AbstractUser):
    username = None
    first_name = None  # Remove first_name
    last_name = None   # Remove last_name
    email = models.EmailField(unique=True)
    organisation = models.CharField(max_length=255)
    #password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['organisation']

    objects = CustomUserManager()


    def __str__(self):
        return self.email


class AddEvents(models.Model):
    organisation=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="events")
    event_name=models.CharField(max_length=100,null=False)
    event_date=models.DateField(null=False)
    start_time=models.TimeField()
    end_time=models.TimeField()
    event_venue=models.CharField(max_length=100)
    event_description=models.TextField()
    registration_fee=models.IntegerField()
    event_poster=models.ImageField(upload_to='event_posters/')
    #organisation=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.event_name} - {self.organisation.organisation}"
    
    
class Register(models.Model):
    event_id=models.ForeignKey(AddEvents,on_delete=models.CASCADE)
    participant_name=models.CharField(max_length=100)
    participant_email=models.EmailField()
    participant_no=models.BigIntegerField()
    participant_clg=models.CharField(max_length=100)
    participant_dept=models.CharField(max_length=100)
    participant_sem=models.CharField(max_length=50)
    participant_payment=models.ImageField(upload_to='participant_payments/')
    def __str__(self):
        return f"{self.participant_name} - {self.event_id.event_name}"