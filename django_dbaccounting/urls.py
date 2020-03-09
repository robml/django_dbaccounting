from django.urls import path

from . import views

# Create urls here

urlpatterns = [
    path('', views.index, name='index'),
    path('report/', views.index, name='report'),
    path('balance-sheet/', views.index, name='balance-sheet'),
    path('income/', views.index, name='income'),
    path('cashflow/', views.index, name='cashflow'),
    path('retained/', views.index, name='retained'),
    path('debt/', views.index, name='debt'),
    path('forecast/', views.index, name='forecast'),
    path('acctype/', views.AccountTypeListView.as_view(), name='acctype'),
    path('acctype/<int:pk>/', views.AccountTypeDetailView.as_view(), name='acctype-detail'),
    path('acctype/create/',views.AccountTypeCreate.as_view(),name='acctype_create'),
    path('acctype/<int:pk>/update/',views.AccountTypeUpdate.as_view(),name='acctype_update'),
    path('acctype/<int:pk>/delete/',views.AccountTypeDelete.as_view(),name='acctype_delete'),
    path('acc/', views.AccountListView.as_view(), name='acc'),
    path('acc/<int:pk>/', views.AccountDetailView.as_view(), name='acc-detail'),
    path('acc/create/',views.AccountCreate.as_view(),name='acc_create'),
    path('acc/<int:pk>/update/',views.AccountUpdate.as_view(),name='acc_update'),
    path('acc/<int:pk>/delete/',views.AccountDelete.as_view(),name='acc_delete'),
    path('txn/', views.TransactionListView.as_view(), name='txn'),
    path('txn/<int:pk>/',  views.TransactionDetailView.as_view(), name='txn-detail'),
    path('txn/create/',views.transaction_create,name='txn_create'),
    path('txn/<int:pk>/update/',views.transaction_update,name='txn_update'),
    path('txn/<int:pk>/delete/',views.TransactionDelete.as_view(),name='txn_delete'),

]