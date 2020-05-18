from rest_framework.generics import (
CreateAPIView,
ListAPIView,
RetrieveAPIView,
RetrieveUpdateAPIView,
DestroyAPIView)
from datetime import datetime, timedelta
from rest_framework_simplejwt.views import TokenObtainPairView



#  Models
from .models import *

# Serializers
from .serializers import *

class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer



# --------- Particapants views -------------#


class ParticipantsListView(ListAPIView):
	queryset = Participants.objects.all()
	serializer_class = ParticipantsListSerializer



class ParticipantCreateView(CreateAPIView):
	serializer_class=ParticipantsSerializer



class ParticipantUpdateView(RetrieveUpdateAPIView):
	queryset = Participants.objects.all()
	serializer_class = ParticipantsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'part_id'



class ParticipantDeleteView(DestroyAPIView):
	queryset = Participants.objects.all()
	serializer_class = ParticipantsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'part_id'


# --------- Hold views -------------#


class HoldAmountListView(RetrieveAPIView):
	queryset = Participants.objects.all()
	serializer_class = HoldAmountListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'part_id'


class HoldAmountCreateView(CreateAPIView):
	serializer_class=HoldAmountSerializer



class HoldAmountUpdateView(RetrieveUpdateAPIView):
	queryset = Hold.objects.all()
	serializer_class = HoldAmountSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'hold_id'



class HoldAmountDeleteView(DestroyAPIView):
	queryset = Hold.objects.all()
	serializer_class = HoldAmountSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'hold_id'


# --------- Loan views -------------#

class ActivLoanView(ListAPIView):
	queryset = Loan.objects.filter(status=False)
	serializer_class = LoanListSerializer

class LoanListView(RetrieveAPIView):
	queryset = Participants.objects.all()
	serializer_class = LoanDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'part_id'


class LoanCreateView(CreateAPIView):
	serializer_class=LoanSerializer



class LoanUpdateView(RetrieveUpdateAPIView):
	queryset = Loan.objects.all()
	serializer_class = LoanSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'loan_id'



class LoanDeleteView(DestroyAPIView):
	queryset = Loan.objects.all()
	serializer_class = LoanSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'loan_id'



# --------- Pyments views -------------#


class PymentView(RetrieveAPIView):
	queryset = Loan.objects.all()
	serializer_class = PymentsDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'loan_id'


class PymentCreateView(CreateAPIView):
	serializer_class=PymentsListSerializer


class PymentUpdateView(RetrieveUpdateAPIView):
	queryset = Pyments.objects.all()
	serializer_class = PymentsListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'pyment_id'


class PymentDeleteView(DestroyAPIView):
	queryset = Pyments.objects.all()
	serializer_class = PymentsListSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'pyment_id'


#  --------- cashfliw views -------------#

class CashFlowListView(ListAPIView):
	queryset = CashFlow.objects.all().order_by('date','id')
	serializer_class = CashFlowSerializer
