from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError 
from django.contrib.auth.forms import PasswordResetForm

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        )
    )
    address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address",
                "class": "form-control"
            }
        )
    )
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone Number",
                "class": "form-control"
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        )
    )
    
    is_admin = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
    is_technician = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
    is_customer_care = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
    is_employee = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
    is_supervisor = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'address', 'phone_number', 'is_admin', 'is_technician', 'is_customer_care', 'is_employee', 'is_supervisor')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        if commit:
            user.save()
        return user





class EmailValidationOnForgotPassword(PasswordResetForm):
       def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email does not exist in our system.")
        return email
    


class UserUpdateForm(forms.ModelForm):
    
     first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        )
    )
     last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        )
    )
     address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address",
                "class": "form-control"
            }
        )
    )
     phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone Number",
                "class": "form-control"
            }
        )
    )

     username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
    )
     email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        )
    )
     
     is_admin = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
     is_technician = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
     is_customer_care = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
     is_employee = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
     is_supervisor = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())


     class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'is_admin', 'is_technician', 'is_customer_care', 'is_superuser']

     def save(self, commit=True):
         user = super().save(commit=False)
         user.full_name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
         if commit:
            user.save()
         return user
     
     

class UserProfileForm(forms.ModelForm):
    
     first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        )
    )
     last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        )
    )
     address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address",
                "class": "form-control"
            }
        )
    )
     phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone Number",
                "class": "form-control"
            }
        )
    )

     username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
    )
     email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        )
    )
     
     profile_photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control-file"  
            }
        )
    )
     
    


     class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'phone_number', 'email', 'profile_photo']

     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the 'username' field from the form
        self.fields.pop('username')
        
     def save(self, commit=True):
         user = super().save(commit=False)
         user.full_name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
         if commit:
            user.save()
         return user


from django.contrib.auth.forms import PasswordChangeForm

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})


