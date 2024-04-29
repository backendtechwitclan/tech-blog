from django.contrib import admin
from .models import User, Category, Blog, Comment


# Register your models here.


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Comment)