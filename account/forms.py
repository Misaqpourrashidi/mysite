from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account


class RegistrationForm(UserCreationForm):
   
    class Meta:
        model = Account
        fields = ('phone_number', 'password1', 'password2')



class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('phone_number', 'password')

    def clean(self):
        if self.is_valid():
            phone_number = self.cleaned_data['phone_number']
            if Account.objects.filter(phone_number=phone_number).exists():
                pass
            else:
                raise forms.ValidationError('Account with this Phone Number does not exists.')
            password = self.cleaned_data['password']
            if not authenticate(phone_number=phone_number, password=password):
                raise forms.ValidationError("Password is Incorrect")



class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('phone_number', 'first_name', 'last_name', 'zip', 'street_address', 'email', 'username')


    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(phone_number=phone_number)
        except Account.DoesNotExist:
            return phone_number
        raise forms.ValidationError('phone number "%s" is already in use.' % phone_number)