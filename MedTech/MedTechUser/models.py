from django.db import models

# Create your models here.


class AllFeelings(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    # permuterm = models.CharField(max_length=50, null=True, blank=True)
    disease = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
<<<<<<< HEAD
        return str(self.name) + " -- " + str(self.disease)

=======
        return str(self.permuterm)+ " -- "+str(self.name)
class AllBodyParts(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    permuterm = models.CharField(max_length=20, null=True, blank=True)

class AllDiseases(models.Model):    
    name = models.CharField(max_length=20, null=True, blank=True)
    # permuterm = models.CharField(max_length=20, null=True, blank=True)
>>>>>>> 2c08968d58fcee5af57c66e91a73f1122609a2b3

class AllBodyParts(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
<<<<<<< HEAD
    permuterm = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.permuterm) + ' -- ' + str(self.name)
=======
    permuterm = models.CharField(max_length=20, null=True, blank=True)
>>>>>>> 2c08968d58fcee5af57c66e91a73f1122609a2b3


class SymptomsToDisease(models.Model):
    symptom = models.CharField(max_length=200, null=True, blank=True)
    body_part = models.CharField(max_length=50, null=True, blank=True)
    disease = models.CharField(max_length=100, null=True, blank=True)



    