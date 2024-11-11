from rest_framework import viewsets
from .models import Account, Transaction, Business
from .serializers import AccountSerializer, TransactionSerializer, BusinessSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
#TASK4 Add manager_list and user_account actions   
    @action(detail=False, permission_classes=[IsAdminUser])
    def manager_list(self, request):
        # Allows managers to list all accounts within the bank
        accounts = Account.objects.all()
        serializer = self.get_serializer(accounts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='user_account')
    def user_account(self, request, pk=None):
        # Allows users to view their own account details
        account = self.get_object()
        serializer = self.get_serializer(account)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def current_balance(self, request, pk=None):
        # Calculate the current balance based on transactions history
        account = self.get_object()
        balance = account.starting_balance
        transactions = Transaction.objects.filter(from_account=account)
        
        for txn in transactions:
            if txn.transaction_type == "deposit":
                balance += txn.amount
            elif txn.transaction_type in ["withdrawal", "payment"]:
                balance -= txn.amount
            elif txn.transaction_type == "collect_roundup":
                balance += txn.amount  # Assuming RoundUps are credited back as deposits

        return Response({'current_balance': balance})    
#ENDTASK4    
from django.db.models import Sum
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
#TASK4 Add manager_list and user_account actions   

    @action(detail=False, methods=['get'], url_path='account/(?P<account_id>[^/.]+)')
    def account_transactions(self, request, account_id=None):
        # View all transactions related to a specific account
        transactions = Transaction.objects.filter(from_account_id=account_id)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='spending-summary/(?P<account_id>[^/.]+)')
    def spending_summary(self, request, account_id=None):
        # Summarize spending by category for a given account
        transactions = Transaction.objects.filter(from_account_id=account_id, transaction_type="payment")
        # Summarize spending by business category
        spending_summary = Transaction.objects.filter(
            from_account_id=account_id,  # Filter by the specific account if needed
            transaction_type="payment"  # Filter by transaction type if needed
        ).values('business__category').annotate(total=Sum('amount'))        
        return Response(spending_summary)
#ENDTASK4    

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]
