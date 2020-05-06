from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import date
from django.db.models import Sum

# Models
from .models import *

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username','password','first_name','last_name','email',]

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		email=validated_data['email']
		new_user = User(username=username,first_name=first_name,last_name=last_name,email=email)
		new_user.set_password(password)
		new_user.save()
		return validated_data



# --------- Participant Serializer -------------#

class ParticipantsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Participants
		fields = "__all__"


class ParticipantsListSerializer(serializers.ModelSerializer):
	part_hold_amount=serializers.SerializerMethodField()
	part_profit_amount=serializers.SerializerMethodField()
	settled_loans=serializers.SerializerMethodField()
	active_loans=serializers.SerializerMethodField()
	error=serializers.SerializerMethodField()


	class Meta:
		model = Participants
		fields = ['id','name','part_hold_amount','part_profit_amount','settled_loans','active_loans',"error"]

	def get_part_hold_amount(self,obj):
		part_hold_amount=obj.hold.all().aggregate(Sum('part_hold_amount'))['part_hold_amount__sum']
		if part_hold_amount==None:
			part_hold_amount=0
		return part_hold_amount

	def get_part_profit_amount(self,obj):
		part_profit_amount=obj.loan.all().aggregate(Sum('profit_amount'))['profit_amount__sum']
		if part_profit_amount==None:
			return 0
		return part_profit_amount

	def get_settled_loans(self,obj):
		loans=obj.loan.filter(status=True).count()
		return loans

	def get_active_loans(self,obj):
		loans=obj.loan.filter(status=False).count()
		return loans

	def get_error(self,obj):
		loans_set=obj.loan.all()
		error=False
		for loan in loans_set:
			totla_loan_amount=loan.totla_loan_amount
			paid_amount=loan.pyments.all().aggregate(Sum('pyment'))['pyment__sum']
			if paid_amount!=None:
				if totla_loan_amount<paid_amount:
					error=True
		return error
			


# --------- Hold Serializer -------------#

class HoldAmountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Hold
		fields = "__all__"

class HoldAmountListSerializer(serializers.ModelSerializer):
	hold_amounts=serializers.SerializerMethodField()

	class Meta:
		model = Participants
		fields = ['id','name','hold_amounts']

	def get_hold_amounts(self,obj):
		hold_amount=Hold.objects.filter(participant=obj.id)
		return HoldAmountSerializer(hold_amount, many=True).data





# --------- Loan Serializer -------------#



class LoanListSerializer(serializers.ModelSerializer):
	status=serializers.SerializerMethodField()
	
	class Meta:
		model = Loan
		fields = ['id','participant','loan_amount','hold_amount','profit_amount','date',"status",'totla_loan_amount','paid_amount']

	def get_status(self,obj):
		totla_loan_amount=obj.totla_loan_amount
		paid_amount=obj.pyments.all().aggregate(Sum('pyment'))['pyment__sum']
		if paid_amount!=None:
			if totla_loan_amount==paid_amount:
				return "Settled"
			elif totla_loan_amount<paid_amount:
				return "error paid_amount more than totla_loan_amount "
			else:
				return "Active"
		else:
			return "Active"


class LoanDetailSerializer(serializers.ModelSerializer):
	loans=serializers.SerializerMethodField()

	class Meta:
		model = Participants
		fields = ['id','name','loans']

	def get_loans(self,obj):
		Loans=Loan.objects.filter(participant=obj.id)
		return LoanListSerializer(Loans, many=True).data

class LoanSerializer(serializers.ModelSerializer):
	class Meta:
		model = Loan
		exclude  = ['totla_loan_amount','paid_amount','status']


# --------- Pyments Serializer -------------#
		




class PymentsListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pyments
		fields = "__all__"



class PymentsDetailSerializer(serializers.ModelSerializer):
	pyments=serializers.SerializerMethodField()

	class Meta:
		model = Loan
		fields = ['id','participant','loan_amount','pyments']

	def get_pyments(self,obj):
		pyments=Pyments.objects.filter(loan=obj.id)
		return PymentsListSerializer(pyments, many=True).data