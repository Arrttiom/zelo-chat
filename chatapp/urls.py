from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.Home, name='home'),
    path("register/", views.UserRegister, name='register'),
    path('login/', views.LoginUser, name='login'),
    path('search/', views.SearchUser, name='search_user'),
    path('chat/<int:user_id>/', views.ChatView, name='chat'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
