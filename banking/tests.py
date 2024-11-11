#TASK3 tests implementation
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account, Transaction, Business
from django.contrib.auth.models import User
from decimal import Decimal

class BankingAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user and get a JWT token for authentication
        self.user = User.objects.create_user(username="testuser", password="password")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Set up test data
        self.account = Account.objects.create(
            id="3ac94f73-ee6a-473a-ad35-c36164229144",
            name="Test User",
            starting_balance=Decimal('1000.00'),
            round_up_enabled=True
        )

        self.business = Business.objects.create(
            id="kfc",
            name="KFC",
            category="Food",
            sanctioned=False
        )

        self.transaction = Transaction.objects.create(
            transaction_type="payment",
            amount=Decimal('25.50'),
            from_account=self.account,
            to_account=self.account
        )

    def test_get_account_list(self):
        # Test retrieving the list of accounts
        url = reverse('account-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_account_detail(self):
        # Test retrieving a specific account
        url = reverse('account-detail', args=[self.account.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test User")

    def test_create_transaction(self):
        # Test creating a transaction
        url = reverse('transaction-list')
        data = {
            "transaction_type": "withdrawal",
            "amount": "100.00",
            "from_account": str(self.account.id),
            "to_account": None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

    def test_get_business_list(self):
        # Test retrieving the list of businesses
        url = reverse('business-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_roundup_feature(self):
        # Test the RoundUp feature for an account
        url = reverse('account-roundups', args=[self.account.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('savings', response.data)
        # Assuming one transaction of 25.50, round up amount would be 0.50

    def test_spending_trends(self):
        # Test the Spending Trends feature
        url = reverse('account-spending-trends', args=[self.account.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['total'],Decimal('25.5'))

    def test_update_business_sanction_status(self):
        # Test updating the sanction status of a business
        url = reverse('business-detail', args=[self.business.id])
        data = {
            "sanctioned": True
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.business.refresh_from_db()
        self.assertTrue(self.business.sanctioned)
