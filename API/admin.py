from django.contrib import admin
from .models import Loan, Pyments, Participants,Hold


admin.site.register(Loan)
admin.site.register(Pyments)
admin.site.register(Participants)
admin.site.register(Hold)

