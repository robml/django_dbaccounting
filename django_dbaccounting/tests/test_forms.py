import datetime

from django.test import TestCase
from django.utils import timezone

from dbaccounting.forms import TransactionForm
from dbaccounting.models import AccountType,Account,Transaction

# Create your tests here.

class TransactionFormTest(TestCase):
    def setUp(self):
        acc_type1 = AccountType.objects.create(name = "Assets",bal_type = "D")
        acc_type2 = AccountType.objects.create(name = "Liabilities",bal_type = "C")
        acc1 = Account.objects.create(name="Short-Term Debt",acc_type=acc_type2)
        acc2 = Account.objects.create(name="Cash",acc_type = acc_type1)
        txn1 = Transaction.objects.create(from_acc = acc1, to_acc = acc2, amount = 100, note="Loan from cousin")    

    # Test Labels
    def test_transaction_from_acc_label(self):
        form = TransactionForm()
        self.assertEquals(form.fields['from_acc'].label, 'From account')

    def test_transaction_to_acc_label(self):
        form = TransactionForm()
        self.assertEquals(form.fields['to_acc'].label, 'To account')

    def test_transaction_amount_label(self):
        form = TransactionForm()
        self.assertEquals(form.fields['amount'].label, 'Amount')
    
    def test_transaction_note_label(self):
        form = TransactionForm()
        self.assertEquals(form.fields['note'].label, 'Note')
    
    # Test Empty Fields
    def test_empty_from_acc(self):
        acc2 = Account.objects.get(id=2)
        with self.assertRaisesMessage(KeyError,'from_acc'):
            form = TransactionForm(data={'to_acc':acc2,'amount':50})
            form.is_valid()
    
    def test_empty_to_acc(self):
        acc1 = Account.objects.get(id=1)
        with self.assertRaisesMessage(KeyError,'to_acc'):
            form = TransactionForm(data={'from_acc':acc1,'amount':50})
            form.is_valid()
    
    def test_empty_amount(self):
        acc1 = Account.objects.get(id=1)
        acc2 = Account.objects.get(id=2)
        with self.assertRaisesMessage(KeyError,'amount'):
            form = TransactionForm(data={'from_acc':acc1,'to_acc':acc2})
            form.is_valid()
    
    # Test Incorrectly Entered Fields
    def test_negative_amount(self):
        acc1 = Account.objects.get(id=1)
        acc2 = Account.objects.get(id=2)
        form = TransactionForm(data={'from_acc':acc1,'to_acc':acc2,'amount':-50})
        self.assertFalse(form.is_valid())
    
    def test_note_over_max_length(self):
        acc1 = Account.objects.get(id=1)
        acc2 = Account.objects.get(id=2)
        note = "test"*300
        form = TransactionForm(data={'from_acc':acc1,'to_acc':acc2,'amount':50,'note':note})
        self.assertFalse(form.is_valid())
    
    # Test a normal form
    def test_transaction_form(self):
        acc1 = Account.objects.get(id=1)
        acc2 = Account.objects.get(id=2)
        form = TransactionForm(data={'from_acc':acc1,'to_acc':acc2,'amount':50,'note':"test"})
        self.assertTrue(form.is_valid())