from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Bank(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cardname = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    PhoneNo = models.CharField(max_length=10,unique=True)  
    CardNumber = models.CharField(max_length=16,unique=True)  
    CVV = models.CharField(max_length=4)  #
    BankName = models.CharField(max_length=100, default='a')
    Address = models.CharField(max_length=100, default='a')
    IFSC = models.CharField(max_length=8, default='a')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    updated = models.DateTimeField(auto_now=True)  
    created = models.DateTimeField(auto_now_add=True)
    

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)  # Each transaction is linked to a specific bank
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically records the date and time of the transaction

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
    
    
    
class Bills(models.Model):
    BILLS_TYPE_CHOICES = [
        ('electricity', 'Electricity'),
        ('recharge', 'Recharge'),
        ('dth', 'DTH'),
        ('rent', 'Rent'),
        ('water', 'Water'),
        ('internet', 'Internet'),
    ]

    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)  
    bills_type = models.CharField(max_length=100, choices=BILLS_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bills_type} - {self.amount}"