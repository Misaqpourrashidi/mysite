from django import forms
from account.models import Account, City, State



PAYMENT_CHOICES = (
	('S', 'Stripe'),
	('P', 'PayPal'),
)

class CheckoutForm(forms.Form):
	first_name 				= forms.CharField(widget=forms.TextInput(attrs={

			'class': 'form-control',
		}))

	last_name 				= forms.CharField(widget=forms.TextInput(attrs={

			'class': 'form-control',
		}))

	email 				= forms.EmailField(widget=forms.TextInput(attrs={

			'class': 'form-control',
		}))

	street_address 			= forms.CharField(widget=forms.TextInput(attrs={
			'placeholder': '1234 Main St',
			'class': 'form-control',
		}))


	zip						= forms.CharField(widget=forms.TextInput(attrs={
				'class': 'form-control',
			}))


	payment_option			= forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)





class CheckOutUpdateForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ('phone_number', 'email', 'first_name', 'last_name', 'zip', 'street_address', 'state', 'city')


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['city'].queryset = City.objects.none()

		if 'state' in self.data:
			try:
				state_id = int(self.data.get('state'))
				self.fields['city'].queryset = City.objects.filter(state_id=state_id).order_by('name')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['city'].queryset = self.instance.state.city_set.order_by('name')



class SentForm(forms.Form):
	ref_code = forms.CharField()


class ReceivedForm(forms.Form):
	ref_code = forms.CharField()