from django.shortcuts import redirect, render
from django.urls import path
from django.http import HttpResponse
from . forms import UploadForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Bank, Transaction, Bills
from .forms import TransactionForm, BillForm, UploadForm
from decimal import Decimal


def Home(request):
    return render(request,"home.html")
                        
def About(request):
    return render(request, "about.html")

def bankinfo(request):
    return render(request, "bankinfo.html")


def dashboard(request):
    details = Bank.objects.filter(user=request.user)
    context={'details_t': details}
    return render(request, "dashboard.html",context)

@login_required
def payments(request):
    details = Bank.objects.filter(user=request.user)
    context = {'details_t': details}
    return render(request, "payments.html", context)

def editcards(request):
    details = Bank.objects.filter(user=request.user)
    context = {'details_t': details}
    return render(request, "editcards.html", context)

def depositdraw(request):
    details = Bank.objects.filter(user=request.user)
    context = {'details_t': details}
    return render(request, "depositdraw.html", context)

def cardhistory(request):
    details = Bank.objects.filter(user=request.user)
    context = {'details_t': details}
    return render(request, "cardhistory.html", context)

def funds(request):
    details = Bank.objects.filter(user=request.user)
    context = {'details_t': details}
    return render(request, "funds.html", context)




def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=user_name, password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return render(request, "login.html",{'form' : form}) 
    else:
        form= AuthenticationForm()

    return render(request, "login.html",{'form' : form})  


def signup_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save() 
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')




@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            bank_detail = form.save(commit=False)
            
            bank_detail.user = request.user

            bank_detail.save()
            form.save()
            return redirect('home')
    else:
        form = UploadForm()
    return render(request, "bankinfo.html", {'form': form})





@login_required
def editdetails(request, bank_id):
    # Retrieve the specific bank profile by ID
    user_bank = get_object_or_404(Bank, id=bank_id, user=request.user)

    if request.method == 'POST':
        form = UploadForm(request.POST, instance=user_bank)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = UploadForm(instance=user_bank)

    return render(request, 'editdetails.html', {'form': form})




@login_required
def addtransaction(request, bank_id):
    bank = Bank.objects.get(id=bank_id, user=request.user)  
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.bank = bank
            transaction.save()


            if transaction.transaction_type == 'deposit':
                bank.balance += transaction.amount
            elif transaction.transaction_type == 'withdrawal':
                bank.balance -= transaction.amount

            bank.save()  
            return redirect('dashboard') 
    else:
        form = TransactionForm()

    return render(request, 'addtransaction.html', {'form': form, 'bank': bank})





@login_required
def addbills(request, bank_id):
    bank = Bank.objects.get(id=bank_id, user=request.user)
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.bank = bank
            bill.save()


            if bill.bills_type in ['electricity', 'recharge','dth','rent','water','internet']:
                bank.balance -= bill.amount
                
            bank.save()  
            return redirect('dashboard')  
    else:
        form = BillForm()

    return render(request, 'addbills.html', {'form': form, 'bank': bank})




@login_required
def history(request, bank_id):
    bank = Bank.objects.get(id=bank_id, user=request.user)
    transactions = Transaction.objects.filter(bank=bank).order_by('-timestamp')
    allbills = Bills.objects.filter(bank=bank).order_by('-timestamp')  

    return render(request, 'history.html', {
        'bank': bank,
        'transactions': transactions,
        'allbills': allbills 
    })






@login_required
def transfer_money(request, bank_id):
    if request.method == 'POST':
        recipient_phone = request.POST.get('recipient_phone')
        amount = Decimal(request.POST.get('amount'))

        # Get the sender's bank account
        sender_bank = Bank.objects.get(id=bank_id, user=request.user)

        # Get the recipient's bank account
        recipient_bank = Bank.objects.get(PhoneNo=recipient_phone)

        if sender_bank.balance >= amount:
            sender_bank.balance -= amount
            recipient_bank.balance += amount
            sender_bank.save()
            recipient_bank.save()

            # Log transactions for both sender and recipient
            Transaction.objects.create(bank=sender_bank, transaction_type='Sent', amount=amount)
            Transaction.objects.create(bank=recipient_bank, transaction_type='Recieved', amount=amount)

            return redirect('dashboard')

    return render(request, 'transfer_money.html')

