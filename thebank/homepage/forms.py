from django import forms
from .models import Bank, Transaction, Bills

class UploadForm(forms.ModelForm):
    name= forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'}),
        required=True
    )
    
    cardname= forms.CharField(
    widget=forms.TextInput(attrs={'class':'form-control'}),
    required=True
    )
    
    Email= forms.EmailField(
    widget=forms.TextInput(attrs={'class':'form-control'}),
    required=True
    )

    PhoneNo= forms.DecimalField(
        widget=forms.TextInput (attrs={'class':'form-control','maxlength': '10'}),
        required=True
    )
        
    CardNumber= forms.DecimalField(
        widget=forms.TextInput(attrs={'class':'form-control','maxlength': '16'}),
        required=True
    )
    
    CVV= forms.DecimalField(
        widget=forms.TextInput(attrs={'class':'form-control','maxlength': '4'}),
        required=True
    )

    BankName= forms.CharField(
    widget=forms.TextInput(attrs={'class':'form-control'}),
    required=True
    )

    Address= forms.CharField(
    widget=forms.TextInput(attrs={'class':'form-control'}),
    required=True
    )
    
    IFSC= forms.CharField(
    widget=forms.TextInput(attrs={'class':'form-control','maxlength': '8'}),
    required=True
    )
    
    
    class Meta:
        model = Bank
        fields = ['name','cardname', 'Email', 'PhoneNo','CardNumber','BankName','Address','CVV','IFSC']
        
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount']
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        

class BillForm(forms.ModelForm):
    class Meta:
        model = Bills
        fields = ['bills_type', 'amount']
        widgets = {
            'bills_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class TransferForm(forms.Form):
    recipient_card_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=True
    )
