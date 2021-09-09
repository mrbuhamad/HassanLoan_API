from API.models import *

def run():

    pyments = Pyments.objects.all()
    hold=Hold.objects.all()
    loan=Loan.objects.all()
    cashFlow=CashFlow.objects.all()

    for i in cashFlow:
        i.delete()

    for i in pyments:
        CashFlow.objects.create(amount=i.pyment,pyment=i,date=i.date,reasoning="loan pyment")

    for i in loan:
        CashFlow.objects.create(amount=-i.loan_amount,loan=i,date=i.date,reasoning="loan")
       
    for i in hold:
        if not i.reasoning=="throu loan":
            if i.part_hold_amount>0:
                CashFlow.objects.create(amount=i.part_hold_amount,hold=i,date=i.date,reasoning="capital increase")
            elif i.part_hold_amount<0:
                CashFlow.objects.create(amount=i.part_hold_amount,hold=i,date=i.date,reasoning="capital withdraw")

