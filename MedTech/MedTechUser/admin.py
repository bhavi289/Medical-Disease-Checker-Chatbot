from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AllFeelings),
admin.site.register(AllBodyParts),
admin.site.register(SymptomsToDisease),
admin.site.register(TempSymptomsToDisease)
admin.site.register(TempxAllFeelings)
admin.site.register(TopDiseases)
admin.site.register(Specialist)