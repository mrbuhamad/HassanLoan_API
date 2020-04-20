from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView



urlpatterns = [

    # #  -------------------  registration urls -------------------  #
    path('login/', TokenObtainPairView.as_view() , name='login'),

    # register url create a user with requierd feild : ['username','password','first_name','last_name','email',]
    path('register/', UserCreateAPIView.as_view(), name='register'),



    # #  --------------------  participants urls   ---------------------#

    path('participants/', ParticipantsListView.as_view(), name='part'),
    path('participants/create/', ParticipantCreateView.as_view(), name='part_create'),
    path('participants/update/<int:part_id>/', ParticipantUpdateView.as_view(), name='part_update'),
    path('participants/delete/<int:part_id>/', ParticipantDeleteView.as_view(), name='part_delete'),


    # #  --------------------  HoldAmount urls   ---------------------#

    path('participants/<int:part_id>/hold/', HoldAmountListView.as_view(), name='hold'),
    path('hold/create', HoldAmountCreateView.as_view(), name='hold-create'),
    path('hold/<int:hold_id>/update', HoldAmountUpdateView.as_view(), name='hold-update'),
    path('hold/<int:hold_id>/delete', HoldAmountDeleteView.as_view(), name='hold-delete'),


    # #  --------------------  Loan urls   ---------------------#

    path('participants/<int:part_id>/loans/', LoanListView.as_view(), name='loans'),
    path('loan/create', LoanCreateView.as_view(), name='loan-create'),
    path('loan/<int:loan_id>/update', LoanUpdateView.as_view(), name='loan-update'),
    path('loan/<int:loan_id>/delete', LoanDeleteView.as_view(), name='loan-delete'),

    # #  --------------------  Pyments urls   ---------------------#

	path('loan/<int:loan_id>/pyments/', PymentView.as_view(), name='pyments'),
    path('pyments/create', PymentCreateView.as_view(), name='pyment-create'),
    path('pyments/<int:pyment_id>/update', PymentUpdateView.as_view(), name='pyment-update'),
    path('pyments/<int:pyment_id>/delete', PymentDeleteView.as_view(), name='pyment-delete'),
    ]
