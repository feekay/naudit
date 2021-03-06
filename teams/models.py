from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Q

from datetime import datetime
import uuid
import os

# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=16)
    gender = models.CharField(max_length=2, choices=(('m', "Male"), ('f', "Female")))
    member_type = models.CharField(max_length=2, choices=(('b', "B"), ('a', "A"), ('c', "C")))
    picture = models.ImageField(upload_to="profile_pictures", blank = False)
    cnic = models.CharField(max_length = 20)
    address = models.CharField(max_length =150)
    birth_date = models.DateField()

    def __unicode__(self):
        return self.user.username

#------------------------------------------------------------------------------#
class Company(models.Model):
    name = models.CharField(max_length=50)
    due_time = models.IntegerField()

    def __unicode__(self):
        return self.name

#------------------------------------------------------------------------------#
class Route(models.Model):
    route_image=models.FileField(upload_to= 'routes')
    route_date = models.DateField(unique=True)
    distance = models.IntegerField()
    expenses = models.IntegerField()

    def __unicode__(self):
        return str(self.route_date) +" "+ str(self.distance)

#------------------------------------------------------------------------------#
class Entry(models.Model):
    company = models.ForeignKey(Company ,null=False)
    job_id = models.IntegerField()
    address = models.CharField(max_length =150)
    price = models.IntegerField()
    start_date = models.DateField(default= datetime.now)
    end_date = models.DateField()
    route_date = models.DateField()
    description = models.TextField(max_length=1500)
    owner = models.ForeignKey(Member, null= False)
    b_owner = models.ForeignKey(Member, null= True, blank=True, related_name="bowner_set")
    c_owner = models.ForeignKey(Member, null= True, blank=True, related_name="cowner_set")
    route = models.ForeignKey(Route, null=True, blank=True)

    approved = models.BooleanField(default=False)   #Team B verfies A's work
    visited = models.BooleanField(default=False)    #Team B marks after getting it done
    cleared = models.BooleanField(default=False)    #Team C verfies B's work
    completed = models.BooleanField(default=False)  #C marks this after performing their job
    verified = models.BooleanField(default=False)   #Admin verifies C's work
    finalized = models.BooleanField(default=False)  #Admin performs this at the end
    finalize_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        #Specify constraints
        super(Entry, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return str(self.company) + str(self.job_id)

    class Meta:
        unique_together =(("company", "job_id"))
#------------------------------------------------------------------------------#        

class Question(models.Model):
    text = models.CharField(max_length =500)

    def __unicode__(self):
        return str(self.text)

#------------------------------------------------------------------------------#        
class Answer(models.Model):
    text = models.CharField(max_length =500)
    question = models.ForeignKey(Question)

    def __unicode__(self):
        str(text)

#------------------------------------------------------------------------------#        
class Attachment(models.Model):
    entry = models.ForeignKey(Entry)
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.FileField(upload_to= 'attachments')
    description = models.CharField(max_length = 500, null = True)
    comment = models.CharField(max_length =500, null =True)
    used = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.key) +"  "+ str(self.used)
#------------------------------------------------------------------------------#    
class Salary_based(models.Model):
    details = models.OneToOneField(Member)
    salary = models.IntegerField()

    def __unicode__(self):
        return str(self.details) +" "+ str(self.salary)
#------------------------------------------------------------------------------#
class Entry_based(models.Model):
    details = models.OneToOneField(Member)
    rate = models.IntegerField()
    
    def entry_count(self):
        return Entry.objects.filter(Q(owner= self.details)|Q(b_owner= self.details)|Q(c_owner= self.details)).count()

    def calculate_salary(self):
        return self.rate* self.entry_count()

    def __unicode__(self):
        return str(self.details) +" "+ str(self.rate)


#------------------------------------------------------------------------------#
class Message(models.Model):
    time = models.DateTimeField(default = datetime.now)
    text = models.CharField(max_length = 500)
    to = models.ManyToManyField(User, related_name = "reciever")
    frm = models.ForeignKey(User, related_name = "sender", null = False)

    def __unicode__(self):
        return str(self.text)
#------------------------------------------------------------------------------#
class Activity(models.Model):
    user =  models.CharField(max_length = 10)
    obj = models.CharField(max_length = 10, null=True)
    action = models.CharField(max_length = 20)
    time = models.DateTimeField(default = datetime.now)
    
