from django.db import models

# Create your models here.


class AllFeelings(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    permuterm = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.permuterm)+ " -- "+str(self.name)
class AllBodyParts(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    permuterm = models.CharField(max_length=20, null=True, blank=True)

class AllDiseases(models.Model):    
    name = models.CharField(max_length=20, null=True, blank=True)
    # permuterm = models.CharField(max_length=20, null=True, blank=True)

class AllSymptoms(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    permuterm = models.CharField(max_length=20, null=True, blank=True)

class FeelingsToDisease(models.Model):
    feeling = models.ForeignKey(AllFeelings,on_delete=models.CASCADE, null=True, blank=True)
    disease = models.ForeignKey(AllDiseases,on_delete=models.CASCADE, null=True, blank=True)

class SymptomsToDisease(models.Model):
    symptom = models.ForeignKey(AllSymptoms, on_delete=models.CASCADE, null=True, blank=True)
    disease = models.ForeignKey(AllDiseases,on_delete=models.CASCADE, null=True, blank=True)

class BodypartToSymptom(models.Model):
    body_part = models.ForeignKey(AllBodyParts, on_delete=models.CASCADE, null=True, blank=True)
    symptom_to_disease = models.ForeignKey(SymptomsToDisease, on_delete=models.CASCADE, null=True, blank=True)