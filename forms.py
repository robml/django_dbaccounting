import datetime

from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from dbaccounting.models import Account, Transaction

class TransactionForm(ModelForm):

    class Meta:
        model = Transaction
        fields = '__all__'
        exclude=['updating','edited']

    def clean(self):
        from_acc_data = self.cleaned_data['from_acc']
        amount_data = self.cleaned_data['amount']
        to_acc_data = self.cleaned_data['to_acc']

        if amount_data<0:
            raise ValidationError(_('Invalid Amount - Must be greater than or equal to 0'))

        if from_acc_data.acc_type.bal_type == 'D':        
            # Check if from_acc has sufficient balance
            if from_acc_data.balance < amount_data:
                raise ValidationError(_('Invalid From Account - Insufficient Funds'))

        if to_acc_data.acc_type.bal_type == 'C':        
            # Check if from_acc has sufficient balance
            if to_acc_data.balance + amount_data > 0:
                raise ValidationError(_('Invalid To Account - Excess Funds'))
        
        ModelForm.clean(self)
    