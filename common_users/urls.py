from django.urls import path
from .views import  MyTokenObtainPairView,admin_dashboard,moderator_dashboard,user_dashboard,signup_view


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path("user/register/",userRegister,name="user_regestration"),
    # path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('moderator_dashboard/', moderator_dashboard, name='moderator_dashboard'),
    path('user_dashboard/', user_dashboard, name='user_dashboard'),
]