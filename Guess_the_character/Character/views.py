import random
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import logout
from Character.forms import CustomAuthenticationForm, RegisterForm, PasswordChangeForm, ChangeProfileForm, \
    CreateQuestionForm
from Character.mixins import TestMixin
from Character.models import User, Question, Like
from django.core.cache import cache
from django.urls import reverse


# Create your views here.

def show_index_page(request):
    return render(request, 'Character/index.html')


class LoginViewPage(LoginView):
    template_name = 'Character/login.html'
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        if 'test_results' in cache:
            test_results = cache.get('test_results')
            user.Passed_Tests += test_results.get('passed_tests', 0)
            user.Correct_Answers += test_results.get('correct_answers', 0)
            user.Wrong_Answers += test_results.get('wrong_answers', 0)
            cache.delete('test_results')
        user.save()

        return response


class RegisterView(CreateView):
    model = User
    template_name = 'Character/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')


class AccountView(DetailView):
    model = User
    template_name = 'Character/account.html'
    context_object_name = 'user'
    pk_url_kwarg = 'pk'


def log_out(request):
    logout(request)
    return redirect('index')


class ChangePasswordView(PasswordChangeView):
    template_name = 'Character/change_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')


class ChangeProfileView(UpdateView):
    model = User
    template_name = 'Character/change_profile.html'
    form_class = ChangeProfileForm
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'pk'


class CreateQuestionView(CreateView):
    model = Question
    template_name = 'Character/create_question.html'
    form_class = CreateQuestionForm
    success_url = reverse_lazy('index')


test = []


class TestPageView(TestMixin, TemplateView):
    template_name = 'Character/test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        questions = list(Question.objects.all())
        global test

        if len(questions) < 10:
            test = questions
            random.shuffle(test)
        else:
            test = random.sample(questions, 10)

        context['test'] = test

        return context

    def post(self, request, *args, **kwargs):
        if 'like' in request.POST:
            self.process_like(request)

        return self.process_answers(request)

    def process_like(self, request):
        if request.user.is_authenticated:
            question_id = request.POST.get('like')
            question = get_object_or_404(Question, id=question_id)
            like, created = Like.objects.get_or_create(user=request.user, question=question)

            if not created:
                question.likes_count -= 1
                like.delete()

            question.save()

    def process_answers(self, request):
        right_answers = 0
        wrong_answers = 0
        perfect_test = False

        global test
        print(test)
        for question in test:
            if question.right_answer == request.POST.get(f"answers_{question.id}"):
                right_answers += 1
            else:
                wrong_answers += 1

        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            user.Passed_Tests += 1
            user.Correct_Answers += right_answers
            user.Wrong_Answers += wrong_answers

            if len(test) == 10:
                if right_answers >= 7:
                    user.Perfect_Tests += 1
                    perfect_test = True
            else:
                if right_answers >= len(test) // 2:
                    user.Perfect_Tests += 1
                    perfect_test = True

            test_results = {
                'right_answers': right_answers,
                'wrong_answers': wrong_answers,
                'perfect_test': perfect_test,
            }
            cache.set(f'test_results_{user.username}', test_results)
            user.save()

        else:
            test_results = {
                'right_answers': right_answers,
                'wrong_answers': wrong_answers,
                'perfect_test': right_answers == len(test),
            }
            cache.set(f'test_results', test_results)
        print(test)
        next_question_url = reverse('test') + f'?question_id={",".join(str(elem.id) for elem in test)}'
        return redirect(next_question_url)
