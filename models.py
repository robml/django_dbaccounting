from django.db import models
from django.urls import reverse

# Create your models here.

class AccountType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    
    BALANCE_CHOICES = (
        ('C','Credit'),
        ('D','Debit'),
    )

    bal_type = models.CharField(choices=BALANCE_CHOICES, max_length=1,
        help_text="Indicate whether the account type is a credit or debit", verbose_name = "balance type")
    
    parent = models.ForeignKey('AccountType',on_delete=models.CASCADE,help_text = "Is this a subcategory (e.g. Current Assets)",null=True,blank=True)
    
    class Meta:
        ordering = ['-bal_type','name']
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('acctype-detail',args=[str(self.id)])
    
    def __str__(self):
        return f'{self.name}'

class Account(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=64, unique=True)
    acc_type = models.ForeignKey(AccountType,on_delete=models.CASCADE,verbose_name="account type")
    balance = models.FloatField(default=0,null=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('acc-detail',args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'

class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    from_acc = models.ForeignKey(Account,on_delete=models.CASCADE, related_name = 'from_account', verbose_name = "from account")
    to_acc = models.ForeignKey(Account,on_delete=models.CASCADE, related_name = 'to_account', verbose_name = "to account")
    amount = models.FloatField()
    note = models.TextField(max_length = 256, blank=True,null=True)
    updating = models.ForeignKey('Transaction',on_delete=models.SET_NULL,blank=True,null=True)
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('txn-detail',args=[str(self.id)])

    def __str__(self):
        return f'TXN on {self.date} from {self.from_acc} to {self.to_acc} for {self.amount} AED'
