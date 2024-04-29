from django.urls import path
from core import views

urlpatterns = [
    path("",views.IndexView.as_view(), name="index"),
    path("contact/",views.ContactView.as_view(), name="contact"),
    path("register/",views.RegisterView.as_view(), name="register"),
    path("login/",views.LoginView.as_view(), name="login"),
    path("logout/",views.LogoutView.as_view(), name="logout"),

    path("blogs/",views.ListBlogView.as_view(),name= "blogs"),
    path("blogs/create/",views.CreateBlogView.as_view(), name="blog_create"),
    path("blogs/<int:pk>/",views.DetailBlogView.as_view(), name="blog_details"),
]