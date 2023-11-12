from django.contrib import admin

from Character.models import *

# Register your models here.
admin.site.register([Question, User, Like, Journal])
