
from django.db import models
from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver


class Participants(models.Model):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name


class Loan(models.Model):
	participant = models.ForeignKey(Participants, on_delete=models.CASCADE, blank=True, null=True,related_name='loan' )
	loan_amount = models.IntegerField(default=0)
	hold_amount = models.IntegerField(default=0)
	profit_amount = models.IntegerField(default=0)
	date=models.DateField(blank=True, null=True)

	#-----recived from get_total_amount signal-----#
	totla_loan_amount=models.IntegerField(default=0)

	#-----recived from get_paid_amount signal------#
	paid_amount=models.IntegerField(default=0)

	#-----recived from get_paid_amount signal------#
	status=models.BooleanField(default=False)
	
	def __str__(self):
		return f"{self.participant.name} - loan is :{self.id}"



class Hold(models.Model):
	participant = models.ForeignKey(Participants, on_delete=models.CASCADE, blank=True, null=True,related_name='hold')
	loan = models.ForeignKey(Loan, on_delete=models.CASCADE,null=True,related_name='hold')
	part_hold_amount = models.IntegerField(default=0)
	date=models.DateField()
	choices = (("capital increase", "capital increase"), ("capital withdraw", "capital withdraw"), ("throu loan", "throu loan"))
	reasoning = models.CharField(max_length=120,choices=choices,default="capital increase")


class Pyments(models.Model):
	loan=models.ForeignKey(Loan, on_delete=models.CASCADE,related_name='pyments')
	pyment=models.IntegerField()
	date=models.DateField()

	def __str__(self):
		return f" payment :{self.id} - {self.date}"



#-------------- singnel to popelate Loan.total_amount ------------- #
@receiver(pre_save, sender=Loan)
def get_total_amount(instance, *args, **kwargs):
	instance.totla_loan_amount=instance.loan_amount+instance.hold_amount+instance.profit_amount


#-------------- singnel to popelate Loan.paid_amount (add when created) ------------- #
@receiver(pre_save, sender=Pyments)
def get_paid_amount_Add(instance, *args, **kwargs):
	if created:
		instance.loan.paid_amount += instance.pyment
		instance.loan.save()

#-------------- singnel to popelate Loan.paid_amount (subtract when deleted) -------- #
@receiver(pre_delete, sender=Pyments)
def get_paid_amount_sabtract(instance, *args, **kwargs):
	instance.loan.paid_amount -= instance.pyment
	instance.loan.save()


#-------------- singnel to popelate Loan.paid_amount (subtract when deleted) -------- #
@receiver(pre_save, sender=Pyments)
def get_pyments_status(instance, *args, **kwargs):
	loan_obj=instance.loan
	if instance.loan.paid_amount == instance.loan.totla_loan_amount:
		instance.loan.status=True
		instance.loan.save()


#-------------- singnel to popelate Hold.reasoning (subtract when deleted) -------- #
@receiver(post_save, sender=Loan)
def get_Hold_amount(instance, *args, **kwargs):
	participant=instance.participant
	loan=instance
	part_hold_amount=instance.hold_amount
	date=instance.date
	reasoning="throu loan"
	Hold.objects.create(participant=participant,loan=loan,part_hold_amount=part_hold_amount,date=date,reasoning=reasoning)
