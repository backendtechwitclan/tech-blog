from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, CreateView, DetailView, ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.urls import reverse
from .forms import ContactForm, LoginForm, BlogForm, RegisterForm
from .models import Blog, Category, User

# Create your views here.

class IndexView(View):
    def get(self,request):
        # getting the blogs and ordering them in descending order of the date created
        # sql equivalent : SELECT * FROM blog ORDER BY date_created DESC
        blogs = Blog.objects.all().order_by("-date_created") 
        context = {
            'recent_blogs': blogs
        }
        return render(request,"index.html", context)

class CreateBlogView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = "blog_create.html"
    fields = ["title","category","content","image"] # Changed it from __all__
    success_url = "/"
    login_url = "/login/" # set this to tell the mixin where the login url is 
    def form_valid(self, form):
        # If the form does not have any error
        # create an unsaved copy of the form as a model and set the author as the current logged in author
        obj = form.save(commit=False) # creating an unsaved copy
        obj.author = self.request.user # setting the author to the current logged in user
        obj.save() # saving the copy to the database
        messages.success(self.request,"Blog Created")
        return super().form_valid(form)

class SecondCreateBlogView(LoginRequiredMixin, View):
    """
    The second implementation of creating a blog
    """
    def get(self,request):
        # get an instance of the Blog form and send it to the template
        form = BlogForm()
        return render(request,"blog_create.html",{'form':form})
    def post(self,request):
        # pass in the request.POST to the Form and also the request.FILES if there is any file
        # request.FILES is for getting the file data send via the request
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            # If the form does not have any error
            # create an unsaved copy of the form as a model and set the author as the current logged in author
            obj = form.save(commit=False) # creating an unsaved copy
            obj.author = self.request.user # setting the author to the current logged in user
            obj.save() # saving the copy to the database
            messages.success(self.request,"Blog Created")

            # redirect to the details view url of the newly created blog
            return redirect(reverse("blog_details",{'pk':obj.pk}))
        
        # if the form has errors
        return render(request,"blog_create.html",{'form':form})
    
class ThirdCreateBlogView(LoginRequiredMixin, FormView):
    """
    The third implementation of creating a blog
    """
    form_class = BlogForm
    template_name = "blog_create.html"
    success_url = "/"
    login_url = "/login/"
    def form_valid(self, form):
        # If the form does not have any error
        # create an unsaved copy of the form as a model and set the author as the current logged in author
        obj = form.save(commit=False) # creating an unsaved copy
        obj.author = self.request.user # setting the author to the current logged in user
        obj.save() # saving the copy to the database
        messages.success(self.request,"Blog Created")
        return super().form_valid(form)


class DetailBlogView(View):
    """
    The first implementation of viewing a blog
    """
    def get(self,request, pk):
        try:
            # get the blog with the unique primary key gotten from the url
            # an error is raised if a blog with the primary key does not exist
            blog = Blog.objects.get(pk = pk)
        except Blog.DoesNotExist:
            # handle the blog does not exist error if it is raised
            messages.error(self.request,"Blog not found") 
            return redirect("/")
        
        # Get the comments of the blog
        # this is how querying in foreign key relationship is done
        comments = blog.comment_set.all() # get all the comments under this blog
        context = {
            "object":blog,
            "comments": comments
        }
        return render(request,"blogs_detail.html", context)
    
class SecondDetailBlogView(DetailView):
    """
    The second implementation of viewing a blog
    """
    model = Blog
    template_name = "blog_details.html"
    def get_context_data(self, **kwargs):
        # Get the context data been sent to the response
        context = super().get_context_data(**kwargs)
        # get the current blog object. The one gotten from the primary key
        blog = self.get_object()

        # Get the comments of the blog
        # this is how querying in foreign key relationship is done
        comments = blog.comment_set.all() # get all the comments under this blog

        # set the comments to the context
        context['comments'] = comments

        return context # return the modified context

    

class ListBlogView(ListView):
    """
    The first implementation of listing all the blogs in the application
    """
    model = Blog
    template_name = "blogs.html"
    def get_context_data(self, **kwargs: Any):
        # Get the context data been sent to the response
        context = super().get_context_data(**kwargs)
        # get all the categories
        categories = Category.objects.all()
        # set it to the current context
        context["categories"] = categories
        return context # return the modified context
    def get_queryset(self):
        return Blog.objects.all().order_by("-date_created")
class SecondListBlogView(View):
    """
    The second implementation of listing all the blogs in the application
    """
    def get(self,request):
        blogs = Blog.objects.all().order_by("-date_created")
        all_categories = Category.objects.all() # get all the categories
        context = {
            "object_list": blogs,
            "categories": all_categories
        }
        return render(request,"blogs.html",context)
    

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = "/"
    def form_valid(self, form):
        user = User()
        user.email = form.cleaned_data["email"]
        user.set_password(form.cleaned_data["password"])
        user.save()
        login(self.request,user)
        messages.success(self.request,"User registered successfully")
        return super().form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    success_url = "/"
    
    def get_form_kwargs(self):
        ## Get the argument being passed to the Login Form
        # i.e LoginForm(**kwargs). we are getting it before it is passed to the LoginForm
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request # pass in the current request to the form
        return kwargs # return the modified keyword arguments
    def form_valid(self, form):
        # If the form does not have any error
        user = form.get_user()
        login(self.request, user) # Login the authenticated user gotten from the login form
        messages.success(self.request, "Login Successful")
        return super().form_valid(form)
    

class LogoutView(View):
    def get(self,request):
        logout(request) # logout the user from the request. the user id is saved as a session
        messages.success(request,"Logout Successful")
        return redirect("/")



class ContactView(View):
    def get(self,request):
        form = ContactForm()
        return render(request,"contact.html",{"form":form})
    def post(self,request):
        # Get the sent data from request.POST and pass it to the Contact Form
        contact_form  = ContactForm(request.POST) # the form created in forms.py
        if contact_form.is_valid():
            contact_form.send_contact_mail(contact_form.cleaned_data)
            messages.success(request,"Message sent successfully")
            return render(request,"contact.html")
        messages.error(request,"Form Invalid")
        return render(request,"contact.html")