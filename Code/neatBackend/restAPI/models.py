import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

"""
Models are based off Database UML diagram found in the documentation
Users, Permissions and Groups are predefined Django authorization models

IMPORTANT: when inputting into database programmer should run a ClassName.clean() on the model.
to do data validation.

for CharFields max_length was often chosen as 255 because these fields do not need to go beyond that. Although, the
current database allows for longer fields, if in the future a change occurs this decision defends against problems
if such a decision arises.
"""
# TODO : since we may not want to delete any/some entries when a user opts out we may want to add a field to check if user opted out instead of cascading deletes.
# TODO : redo validations in this file, switched to datetime

class School(models.Model):
    #fields
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255) # TODO: What does a school ID actually look like? Is it unique even across school districts?

    class Meta:
        unique_together = ('name', 'identifier',)

        #add, change, delete already exist by default
        permissions = (
            ('view_school', 'View school'),
        )

    def __str__(self):
        return self.name


class SchoolRoster(models.Model):
    #FK
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='roster')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schools')

    #fields
    year = models.PositiveSmallIntegerField(default = timezone.now().year)
    
    class Meta:
        unique_together = ('school', 'user',)

        permissions = (
            ('view_schoolroster', 'View school roster'),
        )

    def __str__(self):
        return str(self.school) + " year " + str(self.year)


class Class(models.Model):
    #FK
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')

    #fields
    name = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    isPublic = models.BooleanField(default=False)

    class Meta:
        unique_together = ('school', 'identifier', 'name',)

        #add, change, delete already exist by default
        permissions = (
            ('view_class', 'View classes'),
        )

    def __str__(self):
        return self.name + " at " + str(self.school)


class ClassRoster(models.Model):
    #FK
    classFK = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='roster')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classes')

    class Meta:
        unique_together = ('classFK', 'user',)

        #add, change, delete already exist by default
        permissions = (
            ('view_classroster', 'View class roster'),
        )


class Assignment(models.Model):
    #FK
    classFK = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='assignments')

    #fields
    name = models.CharField(max_length=255)
    dueDate = models.DateTimeField()
    startDate = models.DateTimeField(default=timezone.now)
    isPublic = models.BooleanField(default=False)
    
    #permissions
    class Meta:
        unique_together = ('classFK', 'name',)

        #add, change, delete already exist by default
        permissions = (
            ('view_assignment', 'View assignments'),
        )

    def __str__(self):
        return self.name

class AssignmentRoster(models.Model):
    #FK
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='roster')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')

    class Meta:
        unique_together = ('assignment', 'user',)

        permissions = (
            ('view_assignmentroster', 'View assignment roster'),
        )

class Task(models.Model):
    #FK
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='tasks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    #fields
    name = models.CharField(max_length=255)
    isDone = models.BooleanField(default=False)
    isApproved = models.BooleanField(default=False)
    hoursPlanned = models.PositiveSmallIntegerField(null=True)
    hoursCompleted = models.PositiveSmallIntegerField(null=True)
    startDate = models.DateTimeField(default=timezone.now)
    endDate = models.DateTimeField(null=True)
    dueDate = models.DateTimeField(null=True)

    #weight
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    DIFFICULTY_CHOICES = (
        (LOW, 'low'),
        (MEDIUM, 'medium'),
        (HIGH, 'high'),
    )
    difficulty = models.CharField(max_length=6,
                                      choices=DIFFICULTY_CHOICES,
                                      default=MEDIUM)
    
    class Meta:

        unique_together = ('assignment', 'user', 'name')

        #add, change, delete already exist by default
        permissions = (
            ('view_task', 'View tasks'),
        )

    def __str__(self):
        return self.name

class Profile(models.Model):
    #FK
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    #fields
    grade = models.PositiveSmallIntegerField(null=True)
    age = models.PositiveSmallIntegerField(null=True)
    gender = models.CharField(max_length=50, null=True)
    
    #email verification
    verified = models.BooleanField(default=False)
    emailCode = models.CharField(max_length=40, null=True)
    #keyExpiration = models.DateTimeField(null=True)

    passwordCode = models.CharField(max_length=40, null=True)

    class Meta:
        #add, change, delete already exist by default
        permissions = (
            ('view_profile', 'View user profile'),
        )

    def __str__(self):
        return "User Info: \nGrade:"  + str(self.grade) + "\nAge: " + str(self.age) + "\nGender: " + self.gender \
               + "\nUser: " + "" if self.user is None else str(self.user)

