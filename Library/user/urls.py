from django.urls import path
from user.views import signup, login_user, logout_user


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]