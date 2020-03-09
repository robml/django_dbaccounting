import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.http import HttpResponseRedirect

from dbaccounting.models import AccountType,Account,Transaction
from dbaccounting.forms import TransactionForm
# Create your views here.

# View related objects
class AccountLedger:
    """An organized collection of an AccountType, its child AccountTypes, related Accounts, and total balances"""
    def __init__(self,acc_type):
        self.acc_type = acc_type
        self.sub_type = AccountType.objects.filter(parent=acc_type)
        self.accs = Account.objects.filter(acc_type=acc_type)
        self.total = sum((acc.balance for acc in self.accs)) if self.accs else 0

        self.sub_accs = {}
        if self.sub_type:    
            for sub in self.sub_type:
                self.sub_accs[sub] = AccountLedger(sub)

        self.subtotal = sum((self.sub_accs[sub].total for sub in self.sub_type)) if len(self.sub_type)>0 else 0
        self.total+=self.subtotal

# View Implementations Below

# Account Types
class AccountTypeDetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required=("dbaccounting.view_account",)
    model = AccountType

class AccountTypeListView(PermissionRequiredMixin,generic.ListView):
    permission_required=("dbaccounting.view_accounttype",)
    model = AccountType
    paginate_by = 10

class AccountTypeCreate(PermissionRequiredMixin,CreateView):
    permission_required=("dbaccounting.add_accounttype",)
    model = AccountType
    fields = '__all__'
    
class AccountTypeUpdate(PermissionRequiredMixin,UpdateView):
    permission_required=("dbaccounting.change_accounttype",)
    model = AccountType
    fields = '__all__'

class AccountTypeDelete(PermissionRequiredMixin,DeleteView):
    permission_required=("dbaccounting.delete_accounttype",)
    model = AccountType
    success_url = reverse_lazy('acctype')

# Accounts
class AccountDetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required=("dbaccounting.view_transaction",)
    model = Account

class AccountListView(PermissionRequiredMixin,generic.ListView):
    permission_required=("dbaccounting.view_account",)
    model = Account
    paginate_by = 20

class AccountCreate(PermissionRequiredMixin,CreateView):
    permission_required=("dbaccounting.add_account",)
    model = Account
    fields = '__all__'
    
class AccountUpdate(PermissionRequiredMixin,UpdateView):
    permission_required=("dbaccounting.change_account",)
    model = Account
    fields = ['name','acc_type','balance']
    success_url = reverse_lazy('acc')

class AccountDelete(PermissionRequiredMixin,DeleteView):
    permission_required=("dbaccounting.delete_account",)
    model = Account
    success_url = reverse_lazy('acc')

# Transactions
class TransactionDetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required=("dbaccounting.view_transaction",)
    model = Transaction

class TransactionListView(PermissionRequiredMixin,generic.ListView):
    permission_required=("dbaccounting.view_transaction",)
    model = Transaction
    paginate_by = 50

class TransactionDelete(PermissionRequiredMixin,DeleteView):
    permission_required=("dbaccounting.delete_transaction",)
    model = Transaction
    success_url = reverse_lazy('txn')

    @transaction.atomic
    def delete(self,request,pk):
        txn = get_object_or_404(Transaction,pk=pk)
        txn.from_acc.balance+=txn.amount
        txn.to_acc.balance-=txn.amount
        txn.from_acc.save()
        txn.to_acc.save()

        if txn.updating:
            prev = txn.updating
            prev.edited = False
            prev.from_acc.balance-=prev.amount
            prev.to_acc.balance+=prev.amount
            prev.from_acc.save()
            prev.to_acc.save()
            prev.save()

        txn.delete()
        
        return HttpResponseRedirect(reverse_lazy('txn'))


@transaction.atomic
@login_required
@permission_required('dbaccounting.add_transaction',raise_exception=True)
def transaction_create(request):
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = TransactionForm(request.POST)

        #Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            from_acc = get_object_or_404(Account,pk=form.cleaned_data['from_acc'].pk)
            to_acc = get_object_or_404(Account,pk=form.cleaned_data['to_acc'].pk)
            amount = form.cleaned_data['amount']
            from_acc.balance -= amount
            to_acc.balance += amount
            from_acc.save()
            to_acc.save()
            note = form.cleaned_data['note']

            Transaction.objects.create(from_acc = from_acc,to_acc = to_acc,amount = amount, note=note)

            # redirect to a new URL
            return HttpResponseRedirect(reverse('txn'))
        
    # If this is a GET (or any other method) create the default form.
    else:
        form = TransactionForm()

    context = {
        'form': form,
    }

    return render(request,'dbaccounting/transaction_form.html',context)

@transaction.atomic
@login_required
@permission_required('dbaccounting.change_transaction',raise_exception=True)
def transaction_update(request,pk):
    orig_txn = get_object_or_404(Transaction,pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = TransactionForm(request.POST)
 
        #Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            from_acc = get_object_or_404(Account,pk=form.cleaned_data['from_acc'].pk)
            to_acc = get_object_or_404(Account,pk=form.cleaned_data['to_acc'].pk)
            amount = form.cleaned_data['amount']

            if from_acc!=orig_txn.from_acc:
                orig_txn.from_acc.balance += orig_txn.amount
                from_acc.balance -= orig_txn.amount
            
            if to_acc!=orig_txn.to_acc:
                orig_txn.to_acc.balance -= orig_txn.amount
                to_acc.balance += orig_txn.amount
            
            if amount!=orig_txn.amount:
                diff = amount-orig_txn.amount
                from_acc.balance-=diff
                to_acc.balance+=diff

            orig_txn.from_acc.save()
            orig_txn.to_acc.save()

            from_acc.save()
            to_acc.save()
            
            orig_txn.edited=True
            orig_txn.save()

            note = form.cleaned_data['note']

            Transaction.objects.create(from_acc = from_acc,to_acc = to_acc,amount = amount, note=note, updating=orig_txn)

            # redirect to a new URL
            return HttpResponseRedirect(reverse('txn'))
        
    # If this is a GET (or any other method) create the default form.
    else:
        form = TransactionForm(instance = orig_txn)

    context = {
        'form': form,
    }

    return render(request,'dbaccounting/transaction_form.html',context)

# Balance Sheet (Work in Progress)

@permission_required(('dbaccounting.view_account','dbaccounting.view_accounttype'))
def balance_sheet(request):
    date = str(datetime.date.today())
    main_acc_types = AccountType.objects.filter(parent__isnull=True)

    acc_types = AccountType.objects.all()
    accs = Account.objects.all()

    context = {
        'acc_types': acc_types,
        'accs': accs,
        'date':date,
    }
    
    return render(request,'balance_sheet.html',context=context)

# Index/Main Menu
@login_required
@permission_required(('dbaccounting.view_transaction'), raise_exception=True)
def index(request):
    acc_types = AccountType.objects.all().count()
    accs = Account.objects.all().count()
    txns = Transaction.objects.all().count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits']=num_visits+1

    context = {
        'acc_types': acc_types,
        'accs': accs,
        'txns': txns,
        'num_visits':num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)