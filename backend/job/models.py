import os
import geocoder
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gismodel
from django.contrib.gis.geos import Point
from datetime import datetime, timedelta
from geopy.geocoders import Photon
# Create your models here.
class JobType(models.Choices):
    Permanent = 'Permanent'
    Temporary = 'Temporary'
    Internship = 'Internship'
class EducationType(models.Choices):
    Bachelors = 'Bachelors'
    Masters = 'Masters'
    Phd = 'PHD'   
class Industry(models.Choices):
    Banking = 'Banking'
    IT = 'IT'
    Healthcare = 'Healthcare'
    Education = 'Education'
    Telecommunication = 'Telecommunication'
    Business = 'Business'
    Other = ' Other'
class ExperienceLevel(models.Choices):
    NO_EXPERIENCE = 'No Experience'
    ONE_YEAR = '1 Year'
    TWO_YEAR = '2 Years'
    THRE_YEARS_PLUS = '3+ Years'

def return_date_time():
    now = datetime.now()
    return now + timedelta(days=30)

class Job(models.Model):
    title = models.CharField(max_length=256) 
    description = models.TextField(null=True)
    email = models.EmailField(max_length=100, unique=True)
    address = models.CharField(max_length=256)
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.Permanent)
    education = models.CharField(max_length=20, choices=EducationType.choices, default=EducationType.Bachelors)
    industry = models.CharField(max_length=20, choices=Industry.choices, default=Industry.Business)
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.NO_EXPERIENCE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    salary = models.IntegerField(default=1000, validators=[MinValueValidator(1000), MaxValueValidator(100000)])
    position = models.IntegerField(default=1)
    company = models.CharField(max_length=256)
    points = gismodel.PointField(default=Point(0.0,0.0))
    last_date = models.DateTimeField(default=return_date_time())
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')

    def save(self, *args, **kwargs):
        geolocator = Photon(user_agent="myGeocoder")
        location = geolocator.geocode(self.address)
        if location:
            self.points = Point(location.longitude, location.latitude)
        super(Job, self).save(*args, **kwargs)
