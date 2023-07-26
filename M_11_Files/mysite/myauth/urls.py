from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    AboutMeView,
    UserListView,
    UserDetailsView,
    RegisterView,
    AvatarUpdateView,
    )

app_name = "myauth"

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True,
        ),
         name='login',
         ),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('user/<int:pk>/', UserDetailsView.as_view(), name='user-details'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('users-list/', UserListView.as_view(), name='users-list'),
    path('about-me/<int:pk>/profile-update/', AvatarUpdateView.as_view(), name='profile-update'),
    path('register/', RegisterView.as_view(), name='register'),
    path('cookie/get/', get_cookie_view, name='cookie-get'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),
    path('session/set/', set_session_view, name='session-set'),
    path('session/get/', get_session_view, name='session-get'),
]
