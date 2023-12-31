from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from .models import Profile


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'
    queryset = Profile.objects.prefetch_related('images')
    context_object_name = 'about-me'


class UserListView(ListView):
    template_name = 'myauth/users-list.html'
    model = User
    context_object_name = "Users"

class UserDetailsView(DetailView):
    template_name = "myauth/user-details.html"
    model = User
    context_object_name = "user"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:users-list')

    def form_valid(self, form):
        user = form.save()
        response = super().form_valid(form)

        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class AvatarUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        if self.request.user.is_staff:
            return True
        self.object = self.get_object()
        if self.request.user.pk == self.object.user.pk:
            return True
        return False

    permission_required = 'myauth.change_profile'
    model = Profile
    fields = 'bio', 'avatar'
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "myauth:user-details",
            kwargs={"pk": self.object.user.pk},
        )


    def form_valid(self, form):
        user = form.save()
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            Profile.objects.get_or_create(
                user=self.object,
                image=image,
            )
        return response


def login_view(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/admin/')
    return render(request, 'myauth/login.html', {'error': 'Invalid login credentials'})


@login_required
def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy('myauth:login')


@user_passes_test(lambda user: user.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r}')


@permission_required('myaut.vieew_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Seccion set!')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')
