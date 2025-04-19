from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User

class SignUpForm(UserCreationForm):
    """
    Form for user registration with enhanced fields.
    """
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text=_('Required. Enter a valid email address.')
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        help_text=_('Required. Enter your first name.')
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        help_text=_('Required. Enter your last name.')
    )
    phone_number = forms.CharField(
        max_length=17,
        required=False,
        help_text=_('Optional. Enter your phone number.')
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text=_('Optional. Select your date of birth.')
    )
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        required=True,
        help_text=_('Select your account type.')
    )
    receive_newsletter = forms.BooleanField(
        required=False,
        initial=True,
        help_text=_('Receive updates and newsletters from us.')
    )
    
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'phone_number', 'date_of_birth', 'user_type',
            'receive_newsletter', 'password1', 'password2'
        )
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # Make all fields use the Bootstrap form-control class
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        # Checkbox fields should not have the form-control class
        if 'receive_newsletter' in self.fields:
            self.fields['receive_newsletter'].widget.attrs['class'] = 'form-check-input'

class LoginForm(AuthenticationForm):
    """
    Form for user login with enhanced styling.
    """
    username = forms.CharField(
        label=_('Username or Email'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileUpdateForm(UserChangeForm):
    """
    Form for updating user profile information.
    """
    password = None  # Remove password field from the form
    
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'phone_number', 'bio', 'profile_picture', 'date_of_birth',
            'address_line1', 'address_line2', 'city', 'state',
            'postal_code', 'country', 'website', 'instagram',
            'twitter', 'facebook', 'linkedin', 'receive_newsletter'
        )
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # Make all fields use the Bootstrap form-control class
        for field_name, field in self.fields.items():
            if field_name != 'profile_picture' and field_name != 'receive_newsletter':
                field.widget.attrs['class'] = 'form-control'
        # Checkbox fields should not have the form-control class
        if 'receive_newsletter' in self.fields:
            self.fields['receive_newsletter'].widget.attrs['class'] = 'form-check-input'