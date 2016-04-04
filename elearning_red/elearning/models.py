from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import models




class Permission(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    pass

   
class Role(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    permissions = models.ManyToManyField(Permission)
 

   
class User(models.Model):
    username = models.CharField(max_length=25, blank=False, null=False)
    password = models.CharField(max_length=25, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    firstName = models.CharField(max_length=25)
    lastName = models.CharField(max_length=25)
    dob = models.DateField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    pass

class Tag(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    pass



class Programme(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    desc = models.TextField()
    avgRating = models.DecimalField(max_digits=5,decimal_places=2)
    tags = models.ManyToManyField(Tag)
    users = models.ManyToManyField(User)
    pass

  
class Course(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    desc = models.TextField()
    beginDate = models.DateField()
    duration = models.PositiveSmallIntegerField()
    author = models.TextField()
    tags = models.ManyToManyField(Tag)
    users = models.ManyToManyField(User)
    programmes = models.ManyToManyField(Programme)


    
class Section(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    desc = models.TextField()
    beginDate = models.DateField()
    index = models.PositiveSmallIntegerField(blank=False, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    #prevSection = models.ForeignKey(Section)


 
class Block(models.Model): # Generic block model
    name = models.CharField(max_length=40, blank=False, null=False)
    index = models.PositiveSmallIntegerField(blank=False, null=False)
    assessment = models.BooleanField()
    sections = models.ForeignKey(Section, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)




class Rating(models.Model):
    value = models.PositiveSmallIntegerField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    
