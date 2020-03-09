from django.test import TestCase
from django.db import IntegrityError

from dbaccounting.models import AccountType,Account,Transaction
# Create your tests here.

class AccountTypeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AccountType.objects.create(name = "Assets",bal_type = "D")
        AccountType.objects.create(name = "Current Assets", bal_type = "D", parent=AccountType.objects.get(id=1))
    
    def test_name_label(self):
        acc_type = AccountType.objects.get(id=1)
        field_label = acc_type._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
    
    def test_bal_type_label(self):
        acc_type = AccountType.objects.get(id=1)
        field_label = acc_type._meta.get_field('bal_type').verbose_name
        self.assertEquals(field_label, 'balance type')
    
    def test_parent_label(self):
        acc_type = AccountType.objects.get(id=1)
        field_label = acc_type._meta.get_field('parent').verbose_name
        self.assertEquals(field_label, 'parent')
    
    def test_name_max_length(self):
        acc_type = AccountType.objects.get(id=1)
        max_length = acc_type._meta.get_field('name').max_length
        self.assertEquals(max_length,64)
    
    def test_bal_type_max_length(self):
        acc_type = AccountType.objects.get(id=1)
        max_length = acc_type._meta.get_field('bal_type').max_length
        self.assertEquals(max_length,1)
    
    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            AccountType.objects.create(name="Assets",bal_type="C")
    
    def test_parent_instance(self):
        acc_type = AccountType.objects.get(id=2)
        parent = acc_type.parent
        self.assertEquals(parent,AccountType.objects.get(id=1))

    def test_meta(self):
        acc_type = AccountType.objects.get(id=1)
        order = acc_type._meta.ordering
        self.assertEquals(order,['-bal_type','name'])
    
    def test_object_name(self):
        acc_type = AccountType.objects.get(id=1)
        expected_object_name = f'{acc_type.name}'
        self.assertEquals(expected_object_name,str(acc_type))
    
    def test_get_absolute_url(self):
        acc_type = AccountType.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(acc_type.get_absolute_url(), '/fin/acctype/1/')

class AccountTest(TestCase):
    def setUp(self):
        acc_type1 = AccountType.objects.create(name = "Assets",bal_type = "D")
        Account.objects.create(name="Cash",acc_type=acc_type1)
    
    def test_name_label(self):
        acc = Account.objects.get(id=1)
        field_label = acc._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
    
    def test_acc_type_label(self):
        acc = Account.objects.get(id=1)
        field_label = acc._meta.get_field('acc_type').verbose_name
        self.assertEquals(field_label, 'account type')
    
    def test_name_max_length(self):
        acc = Account.objects.get(id=1)
        max_length = acc._meta.get_field('name').max_length
        self.assertEquals(max_length,64)
    
    def test_default_value(self):
        acc = Account.objects.get(id=1)
        bal = acc._meta.get_field('balance').default
        self.assertEqual(bal,0)
    
    def test_unique_name(self):
        acc_type1 = AccountType.objects.get(id=1)
        with self.assertRaises(IntegrityError):
            Account.objects.create(name="Cash",acc_type=acc_type1)
    
    def test_bal_type(self):
        acc=Account.objects.get(id=1)
        bal_type = acc.acc_type.bal_type
        self.assertEqual(bal_type,'D')

    def test_object_name(self):
        acc = Account.objects.get(id=1)
        expected_object_name = f'{acc.name}'
        self.assertEquals(expected_object_name,str(acc))
    
    def test_get_absolute_url(self):
        acc = Account.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(acc.get_absolute_url(), '/fin/acc/1/')

    def test_meta(self):
        acc = Account.objects.get(id=1)
        order = acc._meta.ordering
        self.assertEquals(order,['name'])

    def test_delete_cascade(self):
        AccountType.objects.get(id=1).delete()
        self.assertEqual(len(Account.objects.all()),0)
    
    
class TransactionTest(TestCase):
    def setUp(self):
        acc_type1 = AccountType.objects.create(name = "Assets",bal_type = "D")
        acc_type2 = AccountType.objects.create(name = "Liabilities",bal_type = "C")
        acc1 = Account.objects.create(name="Cash",acc_type=acc_type1)
        acc2 = Account.objects.create(name="Short-Term Debt",acc_type = acc_type2)
        txn1 = Transaction.objects.create(from_acc = acc2, to_acc = acc1, amount = 100, note="Loan from cousin")
        txn2 = Transaction.objects.create(from_acc = acc2, to_acc = acc1, amount = 50, note = 'update', updating = txn1)
    
    def test_date_label(self):
        txn = Transaction.objects.get(id=1)
        field_label = txn._meta.get_field('date').verbose_name
        self.assertEquals(field_label, 'date')
    
    def test_from_acc_label(self):
        txn = Transaction.objects.get(id=1)
        field_label = txn._meta.get_field('from_acc').verbose_name
        self.assertEquals(field_label, 'from account')
    
    def test_to_acc_label(self):
        txn = Transaction.objects.get(id=1)
        field_label = txn._meta.get_field('to_acc').verbose_name
        self.assertEquals(field_label, 'to account')
    
    def test_amount_label(self):
        txn = Transaction.objects.get(id=1)
        field_label = txn._meta.get_field('amount').verbose_name
        self.assertEquals(field_label, 'amount')
    
    def test_note_label(self):
        txn = Transaction.objects.get(id=1)
        field_label = txn._meta.get_field('note').verbose_name
        self.assertEquals(field_label, 'note')
    
    def test_updating_label(self):
        txn = Transaction.objects.get(id=1)
        field_label = txn._meta.get_field('updating').verbose_name
        self.assertEquals(field_label, 'updating')
    
    def test_edited_label(self):
        txn = Transaction.objects.get(id=1)
        field_label = txn._meta.get_field('edited').verbose_name
        self.assertEquals(field_label, 'edited')
    
    def test_note_max_length(self):
        txn = Transaction.objects.get(id=1)
        max_length = txn._meta.get_field('note').max_length
        self.assertEquals(max_length,256)

    def test_object_name(self):
        txn = Transaction.objects.get(id=1)
        expected_object_name = f'TXN on {txn.date} from {txn.from_acc} to {txn.to_acc} for {txn.amount} AED'
        self.assertEquals(expected_object_name,str(txn))
    
    def test_get_absolute_url(self):
        txn = Transaction.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(txn.get_absolute_url(), '/fin/txn/1/')

    def test_meta(self):
        txn = Transaction.objects.get(id=1)
        order = txn._meta.ordering
        self.assertEquals(order,['date'])

    def test_updating(self):
        txn = Transaction.objects.get(id=2)
        prev = txn.updating
        self.assertEquals(prev,Transaction.objects.get(id=1))

    def test_edited_default(self):
        txn = Transaction.objects.get(id=1)
        self.assertEquals(txn.edited,False)

    def test_delete_cascade(self):
        AccountType.objects.get(id=1).delete()
        self.assertEqual(len(Transaction.objects.all()),0)
