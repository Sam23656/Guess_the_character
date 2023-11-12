from django.urls import path

from Character.views import *

urlpatterns = [
    path('', show_index_page, name='index'),
    path('login/', LoginViewPage.as_view(), name='login'),
    path('logout/', log_out, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/<int:pk>/', AccountView.as_view(), name='account'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('change_profile/<int:pk>/', ChangeProfileView.as_view(), name='change_profile'),
    path('create_question/', CreateQuestionView.as_view(), name='create_question'),
    path('tests/', TestPageView.as_view(), name='test'),
]
