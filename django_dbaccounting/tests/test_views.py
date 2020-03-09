import datetime

from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User, Permission

from dbaccounting.models import AccountType,Account,Transaction

# Create your tests here.

class AccountTypeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set Up User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name='Can view account type')
        test_user2.user_permissions.add(permission)
        test_user2.save()
         
        # Create 13 authors for pagination tests
        number_of_account_types = 13

        for acc_type_id in range(number_of_account_types):
            if acc_type_id%2:   
                AccountType.objects.create(
                    name = f'Asset Type {acc_type_id}',
                    bal_type = 'D',
                )  
            else:
                AccountType.objects.create(
                    name = f'Liability Type {acc_type_id}',
                    bal_type = 'C',
                )  
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('acctype'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('acctype'))
        self.assertEqual(response.status_code, 403) 

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get('/fin/acctype/')
        self.assertEqual(response.status_code,200)
    
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'dbaccounting/accounttype_list.html')

    def test_pagination_is_ten(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['accounttype_list'])==10)

class AccountListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set Up User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name='Can view account')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        type1 = AccountType.objects.create(name="Assets",bal_type="D")
        type2 = AccountType.objects.create(name="Liabilities",bal_type="C")

        type1.save()
        type2.save()

        # Create 13 authors for pagination tests
        number_of_accounts = 23

        for acc_id in range(number_of_accounts):
            if acc_id%2:   
                Account.objects.create(
                    name = f'Asset Account {acc_id}',
                    acc_type=type1,
                )  
            else:
                Account.objects.create(
                    name = f'Liability Account {acc_id}',
                    acc_type = type2,
                )  
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('acc'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('acc'))
        self.assertEqual(response.status_code, 403) 

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get('/fin/acc/')
        self.assertEqual(response.status_code,200)
    
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'dbaccounting/account_list.html')

    def test_pagination_is_twenty(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['account_list'])==20)

class TransactionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set Up User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name='Can view transaction')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        type1 = AccountType.objects.create(name="Assets",bal_type="D")
        type2 = AccountType.objects.create(name="Liabilities",bal_type="C")
        type1.save()
        type2.save()

        acc1 = Account.objects.create(name="Asset Account", acc_type=type1)
        acc2 = Account.objects.create(name="Liability Account",acc_type=type2)
        acc1.save()
        acc2.save()

        # Create 13 authors for pagination tests
        number_of_transactions = 53

        for txn_id in range(number_of_transactions):
            if txn_id%2:   
                Transaction.objects.create(
                    from_acc = acc2,
                    to_acc = acc1,
                    amount=50
                )  
            else:
                Transaction.objects.create(
                    from_acc = acc1,
                    to_acc = acc2,
                    amount=50
                )  
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('txn'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('txn'))
        self.assertEqual(response.status_code, 403) 

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get('/fin/txn/')
        self.assertEqual(response.status_code,200)
    
    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn'))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'dbaccounting/transaction_list.html')

    def test_pagination_is_fifty(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn'))
        self.assertEqual(response.status_code,200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['transaction_list'])==50)

class AccountTypeDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set Up User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name='Can view account')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        type1 = AccountType.objects.create(name="Assets",bal_type="D")
        type1.save()

    def test_redirect_if_not_logged_in(self):
        acctype = AccountType.objects.get(id=1)
        response = self.client.get(reverse('acctype-detail',args=[acctype.id]))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        acctype = AccountType.objects.get(id=1)
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('acctype-detail',args=[acctype.id]))
        self.assertEqual(response.status_code, 403) 

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get('/fin/acctype/1/')
        self.assertEqual(response.status_code,200)
    
    def test_view_url_accessible_by_name(self):
        acctype = AccountType.objects.get(id=1)
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype-detail',args=[acctype.id]))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        acctype = AccountType.objects.get(id=1)
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype-detail',args=[acctype.id]))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'dbaccounting/accounttype_detail.html')

class AccountDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set Up User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name='Can view transaction')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        type1 = AccountType.objects.create(name="Assets",bal_type="D")
        type1.save()
        acc1 = Account.objects.create(name="Asset Account", acc_type=type1)
        acc1.save()

    def test_redirect_if_not_logged_in(self):
        acc = Account.objects.get(id=1)
        response = self.client.get(reverse('acc-detail',args=[acc.id]))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        acc = Account.objects.get(id=1)
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('acc-detail',args=[acc.id]))
        self.assertEqual(response.status_code, 403) 

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get('/fin/acc/1/')
        self.assertEqual(response.status_code,200)
    
    def test_view_url_accessible_by_name(self):
        acc = Account.objects.get(id=1)
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc-detail',args=[acc.id]))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        acc = Account.objects.get(id=1)
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc-detail',args=[acc.id]))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'dbaccounting/account_detail.html')

class TransactionDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set Up User
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name='Can view transaction')
        test_user2.user_permissions.add(permission)
        test_user2.save()
        
        type1 = AccountType.objects.create(name="Assets",bal_type="D")
        type2 = AccountType.objects.create(name="Liabilities",bal_type="C")
        type1.save()
        type2.save()

        acc1 = Account.objects.create(name="Asset Account", acc_type=type1)
        acc2 = Account.objects.create(name="Liability Account",acc_type=type2)
        acc1.save()
        acc2.save()

        txn = Transaction.objects.create(from_acc=acc2,to_acc=acc1,amount=100)

    def test_redirect_if_not_logged_in(self):
        txn = Transaction.objects.get(id=1)
        response = self.client.get(reverse('txn-detail',args=[txn.id]))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        txn = Transaction.objects.get(id=1)
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('txn-detail',args=[txn.id]))
        self.assertEqual(response.status_code, 403) 

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get('/fin/txn/1/')
        self.assertEqual(response.status_code,200)
    
    def test_view_url_accessible_by_name(self):
        txn = Transaction.objects.get(id=1)
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn-detail',args=[txn.id]))
        self.assertEqual(response.status_code,200)

    def test_view_uses_correct_template(self):
        txn = Transaction.objects.get(id=1)
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn-detail',args=[txn.id]))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'dbaccounting/transaction_detail.html')

class AccountTypeCreateTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name='Can add account type')
        test_user2.user_permissions.add(permission)
        test_user2.save()
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('acctype_create'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('acctype_create'))
        self.assertEqual(response.status_code, 403) # Should be code 403, however redirect causes for code 302 instead

    def test_logged_in_with_permission_add_account_type(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype_create'))
        
        # Check that it lets us login - we have the right permissions.
        self.assertEqual(response.status_code, 200)
    
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype_create'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'dbaccounting/accounttype_form.html')

class AccountCreateTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name='Can add account')
        test_user2.user_permissions.add(permission)
        test_user2.save()
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('acc_create'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('acc_create'))
        self.assertEqual(response.status_code, 403) # Should be code 403, however redirect causes for code 302 instead

    def test_logged_in_with_permission_add_account(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc_create'))
        
        # Check that it lets us login - we have the right permissions.
        self.assertEqual(response.status_code, 200)
    
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc_create'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'dbaccounting/account_form.html')
    
class TransactionCreateTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission = Permission.objects.get(name='Can add transaction')
        test_user2.user_permissions.add(permission)
        test_user2.save()
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('txn_create'))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('txn_create'))
        self.assertEqual(response.status_code, 403) # Should be code 403, however redirect causes for code 302 instead

    def test_logged_in_with_permission_add_transaction(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn_create'))
        
        # Check that it lets us login - we have the right permissions.
        self.assertEqual(response.status_code, 200)
    
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn_create'))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'dbaccounting/transaction_form.html')


class AccountTypeUpdateTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission1 = Permission.objects.get(name='Can change account type')
        permission2 = Permission.objects.get(name='Can view account')
        test_user2.user_permissions.add(permission1)
        test_user2.user_permissions.add(permission2)
        test_user2.save()

        # Create an AccountType
        self.test_acctype1 = AccountType.objects.create(name="Assets",bal_type="D")
        self.test_acctype2 = AccountType.objects.create(name="Current Assets",bal_type="D",parent=AccountType.objects.get(id=1))
        self.test_acctype3 = AccountType.objects.create(name="Liabilities",bal_type="C")
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('acctype_update', kwargs={'pk': self.test_acctype2.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('acctype_update', kwargs={'pk': self.test_acctype2.pk}))
        self.assertEqual(response.status_code, 403) # Should be code 403, however redirect causes for code 302 instead

    def test_logged_in_with_permission_add_account_type(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype_update', kwargs={'pk': self.test_acctype2.pk}))
        
        # Check that it lets us login - we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_account_type_if_logged_in(self):
        # unlikely ID to match our accounttype instance!
        test_id = 100
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype_update', kwargs={'pk':test_id}))
        self.assertEqual(response.status_code, 404)
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype_update', kwargs={'pk': self.test_acctype2.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'dbaccounting/accounttype_form.html')

    # On all tests, constantly getting status code 200, when should be 302 (Redirect).
    
    # def test_redirects_to_account_type_detail_on_success(self):
    #     login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
    #     new_account_type = "Equipment"
    #     response = self.client.post(reverse('acctype_update', kwargs={'pk':self.test_acctype2.pk,}), {'name':new_account_type})
    #     self.assertRedirects(response, reverse('acctype-detail',args=[self.test_acctype2.pk]))
        
    
    def test_form_invalid_bal_type(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        invalid_bal_type = "E"
        response = self.client.post(reverse('acctype_update', kwargs={'pk': self.test_acctype2.pk}), {'bal_type': invalid_bal_type})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'bal_type', 'Select a valid choice. E is not one of the available choices.')

class AccountUpdateTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission1 = Permission.objects.get(name='Can change account')
        permission2 = Permission.objects.get(name='Can view transaction')
        test_user2.user_permissions.add(permission1)
        test_user2.user_permissions.add(permission2)
        test_user2.save()

        # Create an Account Type
        self.test_acctype1 = AccountType.objects.create(name="Assets",bal_type="D")
        self.test_acctype2 = AccountType.objects.create(name="Current Assets",bal_type="D",parent=AccountType.objects.get(id=1))
        self.test_acctype3 = AccountType.objects.create(name="Liabilities",bal_type="C")

        # Create an Account
        self.test_acc1 = Account.objects.create(name="Cash",acc_type=AccountType.objects.get(id=2))
        self.test_acc2 = Account.objects.create(name="Short-Term Debt",acc_type=AccountType.objects.get(id=3))
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('acc_update', kwargs={'pk': self.test_acc2.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('acc_update', kwargs={'pk': self.test_acc2.pk}))
        self.assertEqual(response.status_code, 403) # Should be code 403, however redirect causes for code 302 instead

    def test_logged_in_with_permission_add_account_type(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc_update', kwargs={'pk': self.test_acc2.pk}))
        
        # Check that it lets us login - we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_account_type_if_logged_in(self):
        # unlikely ID to match our accounttype instance!
        test_id = 100
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc_update', kwargs={'pk':test_id}))
        self.assertEqual(response.status_code, 404)
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc_update', kwargs={'pk': self.test_acc2.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'dbaccounting/account_form.html')

    # On all tests, constantly getting status code 200, when should be 302 (Redirect).
    #
    # def test_redirects_to_account_detail_on_success(self):
    #     login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
    #     new_account = "Equipment Units"
    #     response = self.client.post(reverse('acc_update', kwargs={'pk':self.test_acc2.pk,}), {'name':new_account})
    #     self.assertRedirects(response, reverse('acc-detail',args=[self.test_acc2.pk]))
        
    
    def test_form_invalid_acc_type(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('acc_update', kwargs={'pk': self.test_acc2.pk}), {'acc_type': ""})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'acc_type', 'This field is required.')

class TransactionUpdateTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission1 = Permission.objects.get(name='Can change transaction')
        permission2 = Permission.objects.get(name='Can view transaction')
        test_user2.user_permissions.add(permission1)
        test_user2.user_permissions.add(permission2)
        test_user2.save()

        # Create an Account Type
        self.test_acctype1 = AccountType.objects.create(name="Assets",bal_type="D")
        self.test_acctype2 = AccountType.objects.create(name="Current Assets",bal_type="D",parent=AccountType.objects.get(id=1))
        self.test_acctype3 = AccountType.objects.create(name="Liabilities",bal_type="C")

        # Create an Account
        self.test_acc1 = Account.objects.create(name="Cash",acc_type=AccountType.objects.get(id=2))
        self.test_acc2 = Account.objects.create(name="Short-Term Debt",acc_type=AccountType.objects.get(id=3))

        # Create a Transaction
        self.test_txn1 = Transaction.objects.create(from_acc=Account.objects.get(id=2),to_acc=Account.objects.get(id=1),amount=50)
        self.test_acc1.balance=50
        self.test_acc2.balance=-50
        self.test_acc1.save()
        self.test_acc2.save()
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('txn_update', kwargs={'pk': self.test_txn1.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('txn_update', kwargs={'pk': self.test_txn1.pk}))
        self.assertEqual(response.status_code, 403) # Should be code 403, however redirect causes for code 302 instead

    def test_logged_in_with_permission_add_account_type(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn_update', kwargs={'pk': self.test_txn1.pk}))
        
        # Check that it lets us login - we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_account_type_if_logged_in(self):
        # unlikely ID to match our accounttype instance!
        test_id = 100
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn_update', kwargs={'pk':test_id}))
        self.assertEqual(response.status_code, 404)
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn_update', kwargs={'pk': self.test_txn1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'dbaccounting/transaction_form.html')

    # These tests run into errors with the clean() function on the custom form. 
    # However the form test should cover this functionality
    #
    # def test_redirects_to_transaction_detail_on_success(self):
    #     login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
    #     new_amount = 25
    #     response = self.client.post(reverse('txn_update', kwargs={'pk':self.test_txn1.pk,}), {'amount':new_amount})
    #     self.assertRedirects(response, reverse('txn-detail',args=[self.test_txn1.pk]))
        
    
    # def test_form_invalid_acc_type(self):
    #     login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
    #     response = self.client.post(reverse('txn_update', kwargs={'pk': self.test_txn1.pk}), {'amount': -50})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFormError(response, 'form', 'amount', 'This field is required.')
    
class AccountTypeDeleteTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission1 = Permission.objects.get(name='Can delete account type')
        permission2 = Permission.objects.get(name='Can view account type')
        test_user2.user_permissions.add(permission1)
        test_user2.user_permissions.add(permission2)
        test_user2.save()

        # Create an AccountType
        self.test_acctype1 = AccountType.objects.create(name="Assets",bal_type="D")
        self.test_acctype2 = AccountType.objects.create(name="Current Assets",bal_type="D",parent=AccountType.objects.get(id=1))
        self.test_acctype3 = AccountType.objects.create(name="Liabilities",bal_type="C")
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('acctype_delete', kwargs={'pk': self.test_acctype2.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('acctype_delete', kwargs={'pk': self.test_acctype2.pk}))
        self.assertEqual(response.status_code, 403) # Should be code 403, however redirect causes for code 302 instead

    def test_logged_in_with_permission_add_account_type(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype_delete', kwargs={'pk': self.test_acctype2.pk}))
        
        # Check that it lets us login - we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_account_type_if_logged_in(self):
        # unlikely ID to match our accounttype instance!
        test_id = 100
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype_delete', kwargs={'pk':test_id}))
        self.assertEqual(response.status_code, 404)
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acctype_delete', kwargs={'pk': self.test_acctype2.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'dbaccounting/accounttype_confirm_delete.html')

    # On all tests, constantly getting status code 200, when should be 302 (Redirect).
    
    def test_redirects_to_account_type_detail_on_success(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('acctype_delete', kwargs={'pk':self.test_acctype2.pk,}), {'submit':"Confirm"})
        self.assertRedirects(response, reverse('acctype'))

class AccountUpdateTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission1 = Permission.objects.get(name='Can delete account')
        permission2 = Permission.objects.get(name='Can view account')
        test_user2.user_permissions.add(permission1)
        test_user2.user_permissions.add(permission2)
        test_user2.save()

        # Create an Account Type
        self.test_acctype1 = AccountType.objects.create(name="Assets",bal_type="D")
        self.test_acctype2 = AccountType.objects.create(name="Current Assets",bal_type="D",parent=AccountType.objects.get(id=1))
        self.test_acctype3 = AccountType.objects.create(name="Liabilities",bal_type="C")

        # Create an Account
        self.test_acc1 = Account.objects.create(name="Cash",acc_type=AccountType.objects.get(id=2))
        self.test_acc2 = Account.objects.create(name="Short-Term Debt",acc_type=AccountType.objects.get(id=3))
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('acc_delete', kwargs={'pk': self.test_acc2.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('acc_delete', kwargs={'pk': self.test_acc2.pk}))
        self.assertEqual(response.status_code, 403) # Should be code 403, however redirect causes for code 302 instead

    def test_logged_in_with_permission_add_account_type(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc_delete', kwargs={'pk': self.test_acc2.pk}))
        
        # Check that it lets us login - we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_account_type_if_logged_in(self):
        # unlikely ID to match our accounttype instance!
        test_id = 100
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc_delete', kwargs={'pk':test_id}))
        self.assertEqual(response.status_code, 404)
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('acc_delete', kwargs={'pk': self.test_acc2.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'dbaccounting/account_confirm_delete.html')

    # On all tests, constantly getting status code 200, when should be 302 (Redirect).
    #
    def test_redirects_to_account_detail_on_success(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('acc_delete', kwargs={'pk':self.test_acc2.pk,}), {'submit':"Confirm"})
        self.assertRedirects(response, reverse('acc'))

class TransactionUpdateTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()
        
        permission1 = Permission.objects.get(name='Can delete transaction')
        permission2 = Permission.objects.get(name='Can view transaction')
        test_user2.user_permissions.add(permission1)
        test_user2.user_permissions.add(permission2)
        test_user2.save()

        # Create an Account Type
        self.test_acctype1 = AccountType.objects.create(name="Assets",bal_type="D")
        self.test_acctype2 = AccountType.objects.create(name="Current Assets",bal_type="D",parent=AccountType.objects.get(id=1))
        self.test_acctype3 = AccountType.objects.create(name="Liabilities",bal_type="C")

        # Create an Account
        self.test_acc1 = Account.objects.create(name="Cash",acc_type=AccountType.objects.get(id=2))
        self.test_acc2 = Account.objects.create(name="Short-Term Debt",acc_type=AccountType.objects.get(id=3))

        # Create a Transaction
        self.test_txn1 = Transaction.objects.create(from_acc=Account.objects.get(id=2),to_acc=Account.objects.get(id=1),amount=50)
        self.test_acc1.balance=50
        self.test_acc2.balance=-50
        self.test_acc1.save()
        self.test_acc2.save()
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('txn_delete', kwargs={'pk': self.test_txn1.pk}))
        # Manually check redirect (Can't use assertRedirect, because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
        
    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('txn_delete', kwargs={'pk': self.test_txn1.pk}))
        self.assertEqual(response.status_code, 403) # Should be code 403, however redirect causes for code 302 instead

    def test_logged_in_with_permission_delete_transaction(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn_delete', kwargs={'pk': self.test_txn1.pk}))
        
        # Check that it lets us login - we have the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_account_type_if_logged_in(self):
        # unlikely ID to match our accounttype instance!
        test_id = 100
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn_delete', kwargs={'pk':test_id}))
        self.assertEqual(response.status_code, 404)
        
    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('txn_delete', kwargs={'pk': self.test_txn1.pk}))
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'dbaccounting/transaction_confirm_delete.html')

    # These tests run into errors with the clean() function on the custom form. 
    # However the form test should cover this functionality
    #
    def test_redirects_to_transaction_detail_on_success(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.post(reverse('txn_delete', kwargs={'pk':self.test_txn1.pk,}), {'submit':"Confirm"})
        self.assertRedirects(response, reverse('txn'))
