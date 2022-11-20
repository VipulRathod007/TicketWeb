from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('book/', book, name='book'),
    path('report/', report, name='report'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
