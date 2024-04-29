from typing import Any
from django import forms
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import Blog, Comment, User

class ContactForm(forms.Form):
    name = forms.CharField(max_length = 200)
    email = forms.EmailField()
    subject = forms.CharField(max_length= 200)
    message = forms.CharField()

    def send_contact_mail(self, data):
        send_mail(
            f"Site Message - {data['subject']}", # email subject
            f"Sender Email: {data['email']}\nSender Name: {data['name']}\nSender Message: {data['message']}", # email content
            "from@example.com", # sender mail
            ["from@example"], # reciever email
            fail_silently=False,
        )

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    def __init__(self, request,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request  = request
        self.user = None
    def clean(self):
        self.user = authenticate(self.request, email = self.cleaned_data['email'], password = self.cleaned_data['password'])
        if not self.user:
            raise forms.ValidationError("Invalid Credentials")
        return self.cleaned_data
    def get_user(self):
        return self.user

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    confirm_password = forms.CharField()
    def clean(self):
        if User.objects.filter(email = self.cleaned_data['email']).exists():
            self.add_error("email","User with email already exists")
        try:
            validate_password(self.cleaned_data["password"])
        except forms.ValidationError as err:
            self.add_error("password",err)
        if self.cleaned_data['password'] != self.cleaned_data["confirm_password"]:
            self.add_error('confirm_password',"password does not match")

# class RegisterModelForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ["email, password"]

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title","category","content","image"]
    
