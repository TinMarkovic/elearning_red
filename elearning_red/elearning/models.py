from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from model_utils.managers import InheritanceManager
from json import loads
# Commented out for now. Didn't see them used anywhere:
#from django.db.models.signals import pre_save
#from django.utils.text import slugify
#from django.contrib.auth.models import models

class Permission(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    
    def __unicode__(self):
        return self.name
   
class Role(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    permissions = models.ManyToManyField(Permission, blank=True)
    
    def __unicode__(self):
        return self.name

class CustomUser(User):
    dob = models.DateField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    
    @cached_property
    def getRole(self):
        userRole = self.role.name;
        return userRole
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name


class Tag(models.Model):
    name = models.CharField(max_length=25, blank=False, null=False)
    
    def __unicode__(self):
        return self.name

class Programme(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    desc = models.TextField()
    avgRating = models.DecimalField(max_digits=5,decimal_places=2, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    users = models.ManyToManyField(CustomUser, blank=True)
    
    def __unicode__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    desc = models.TextField(blank=True, null=True)
    beginDate = models.DateField(blank=True, null=True)
    duration = models.PositiveSmallIntegerField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    users = models.ManyToManyField(CustomUser, blank=True)
    programmes = models.ManyToManyField(Programme, blank=True)
    avgRating = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    
    
    def __unicode__(self):
        return self.name
    
class Section(models.Model):
    name = models.CharField(max_length=40, blank=False, null=False)
    desc = models.TextField(blank=True, null=True)
    beginDate = models.DateField(blank=True, null=True)
    index = models.PositiveSmallIntegerField(blank=False, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return self.name
    #prevSection = models.ForeignKey(Section)
 
class Block(models.Model): # Generic block model
    name = models.CharField(max_length=40, blank=False, null=False)
    index = models.PositiveSmallIntegerField(blank=False, null=False)
    assessment = models.BooleanField(default=False)
    sections = models.ForeignKey(Section, on_delete=models.CASCADE)
    objects = InheritanceManager()
    def __unicode__(self):
        return self.name
    #prevBlock = models.ForeignKey(Block)

# Different blocks, all inheriting the Generic model

class HTMLBlock(Block):
    content = models.TextField(blank=False, null=False)

class VideoBlock(Block):
    url = models.URLField(max_length=250, blank=False, null=False)

class ImageBlock(Block):
    subtitle = models.CharField(max_length=40, blank=True, null=True)
    image = models.ImageField(upload_to="", blank=False, null=False)

class QuizBlock(Block):
    serialQuestions = models.TextField(blank=False, null=False)

class Rating(models.Model):
    value = models.PositiveSmallIntegerField(null=False, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    @classmethod
    def create(cls, value, user, course):
        rating = cls(value=value, user = CustomUser.objects.get(id=int(user.id)), course = course)
        return rating
    
class Progress(models.Model):
    serialAnswers = models.TextField(blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    
    def assess(self):
        answers = loads(loads(self.serialAnswers))
        questions = loads(loads(QuizBlock.objects.get(id=self.block.id).serialQuestions))
        result = []
        score = 0
        scoreDivisor = 0
        for q in range(len(questions)): 
            result.append( {"title" : answers[q]["title"], "points" : 0} )
            for a in questions[q]["correct"]:
                for b in answers[q]["answered"]:
                    if a.strip() == b.strip():
                        result[q]["points"] += 1
            if result[q]["points"] < len(answers[q]["answered"]):
                result[q]["points"] -= (len(answers[q]["answered"]) - result[q]["points"])*0.5
            if result[q]["points"] < 0:
                result[q]["points"] = 0
            
            else:
                result[q]["points"] = int(100 * float(result[q]["points"])/float(len(questions[q]["correct"])))
            score += result[q]["points"]
            scoreDivisor += 1
        score = int(score/scoreDivisor)
        return({"result" : result, "score" : score })   