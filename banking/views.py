from rest_framework import viewsets
from .models import Account, Transaction, Business
from .serializers import AccountSerializer, TransactionSerializer, BusinessSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models #TASK 2 Technicakl fix errors -NameError: name 'models' is not defined

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def roundups(self, request, pk=None):
        account = self.get_object()
        roundups = Transaction.objects.filter(from_account=account, transaction_type='payment')
        savings = sum([round(roundup.amount - int(roundup.amount)) for roundup in roundups])
        return Response({'savings': savings})

    @action(detail=True, methods=['get'])
    def spending_trends(self, request, pk=None):
        account = self.get_object()
        payments = Transaction.objects.filter(from_account=account, transaction_type='payment')
        trends = payments.values('to_account__name').annotate(total=models.Sum('amount'))
        return Response(trends)
    

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
