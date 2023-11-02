from django.urls import path

from Character.views import *

urlpatterns = [
    path('', show_index_page, name='index'),
    path('login/', LoginViewPage.as_view(), name='login'),
]
