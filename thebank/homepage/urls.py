from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('login', views.login_page, name="login"),
    path('signup', views.signup_user, name="signup"),
    path('logout', views.logout_user, name="logout"),
    path('upload', views.upload, name="upload"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('payments', views.payments, name='payments'),
    path('editcards', views.editcards, name='editcards'),
    path('depositdraw', views.depositdraw, name='depositdraw'),
    path('funds', views.funds, name='funds'),
    path('cardhistory', views.cardhistory, name='cardhistory'),
    path('editdetails/<int:bank_id>/', views.editdetails, name='editdetails'),
    path('add-transaction/<int:bank_id>/', views.addtransaction, name='add_transaction'),
    path('add-bills/<int:bank_id>/', views.addbills, name='add_bills'),
    path('transaction-history/<int:bank_id>/', views.history, name='transaction_history'),
    path('transfer-money/<int:bank_id>/', views.transfer_money, name='transfer_money'),
]
