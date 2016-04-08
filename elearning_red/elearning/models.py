from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import models
from django.contrib.auth.models import User

class Permission(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    
    def __unicode__(self):
        return self.name
   
class Role(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    permissions = models.ManyToManyField(Permission)
    
    def __unicode__(self):
        return self.name

class CustomUser(User):
    dob = models.DateField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    
    def __unicode__(self):
        return self.name

class Programme(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    desc = models.TextField()
    avgRating = models.DecimalField(max_digits=5,decimal_places=2)
    tags = models.ManyToManyField(Tag)
    users = models.ManyToManyField(CustomUser)
    
    def __unicode__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    desc = models.TextField()
    beginDate = models.DateField()
    duration = models.PositiveSmallIntegerField()
    author = models.TextField()
    tags = models.ManyToManyField(Tag)
    users = models.ManyToManyField(CustomUser)
    programmes = models.ManyToManyField(Programme)
    
    def __unicode__(self):
        return self.name
    
class Section(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    desc = models.TextField()
    beginDate = models.DateField()
    index = models.PositiveSmallIntegerField(blank=False, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.name
    #prevSection = models.ForeignKey(Section)
 
class Block(models.Model): # Generic block model
    name = models.CharField(max_length=40, blank=False, null=False)
    index = models.PositiveSmallIntegerField(blank=False, null=False)
    assessment = models.BooleanField()
    sections = models.ForeignKey(Section, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.name
    #prevBlock = models.ForeignKey(Block)

# Different blocks, all inheriting the Generic model

class HTMLBlock(Block):
    content = models.TextField(blank=False, null=False)

class VideoBlock(Block):
    youtube = models.CharField(max_length=200, blank=False, null=False)

"""
class ImageBlock(Block):
    image = models.ImageField(blank=False, null=False)
"""

class QuizBlock(Block):
    serialQuestions = models.TextField(blank=False, null=False)

class Progress(models.Model):
    serialAnswers = models.TextField(blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

class Rating(models.Model):
    value = models.PositiveSmallIntegerField(null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)