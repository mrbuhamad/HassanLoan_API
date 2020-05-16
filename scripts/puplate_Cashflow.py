from API.models import *

def run():

    pyments = Pyments.objects.all()
    hold=Hold.objects.all()

    for i in pyments:
        CashFlow.objects.create(amount=i.pyment,pyment=i,date=i.date,reasoning="loan pyment")

    for i in hold:
        if i.part_hold_amount>0:
            CashFlow.objects.create(amount=i.part_hold_amount,hold=i,date=i.date,reasoning="capital increase")
        elif i.part_hold_amount<0:
            CashFlow.objects.create(amount=i.part_hold_amount,hold=i,date=i.date,reasoning="capital withdraw")
