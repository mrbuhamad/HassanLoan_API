from django.contrib import admin
from .models import Loan, Pyments, Participants,Hold



class LoanInstanceInline(admin.TabularInline):
    model = Loan

class PartAdmin(admin.ModelAdmin):
    inlines = [LoanInstanceInline]

admin.site.register(Participants, PartAdmin )
admin.site.register(Loan)
admin.site.register(Pyments)
admin.site.register(Hold)


