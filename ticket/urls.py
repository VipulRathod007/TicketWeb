from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('book/', book, name='book'),
    path('find/', find, name='find-ticket'),
    path('show/', show, name='show-ticket'),
    path('report/', report, name='report'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
