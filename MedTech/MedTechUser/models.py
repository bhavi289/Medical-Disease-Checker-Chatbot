from django.db import models

# Create your models here.


class AllFeelings(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    # permuterm = models.CharField(max_length=50, null=True, blank=True)
    disease = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.name) + " -- " + str(self.disease)


class AllBodyParts(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    permuterm = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.permuterm) + ' -- ' + str(self.name)


class SymptomsToDisease(models.Model):
    symptom = models.CharField(max_length=200, null=True, blank=True)
    body_part = models.CharField(max_length=50, null=True, blank=True)
    disease = models.CharField(max_length=100, null=True, blank=True)

class TempSymptomsToDisease(models.Model):
    symptom = models.CharField(max_length=200, null=True, blank=True)
    body_part = models.CharField(max_length=50, null=True, blank=True)
    disease = models.CharField(max_length=100, null=True, blank=True)

class TempxAllFeelings(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    # permuterm = models.CharField(max_length=50, null=True, blank=True)
    disease = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.name) + " -- " + str(self.disease)

class AskingSymptoms(models.Model):
    disease = models.CharField(max_length=100, null=True, blank=True)
    symptom = models.CharField(max_length=100, null=True, blank=True)

class TopDiseases(models.Model):
    disease = models.CharField(max_length=100, null=True, blank=True)

class Specialist(models.Model):
    disease = models.CharField(max_length=100, null=True, blank=True)
    doctor = models.CharField(max_length=100, null=True, blank=True)
    