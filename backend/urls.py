from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(),name='Index'),
    path('login', views.Login.as_view(),name='Login'),
    path('signup', views.SignUp.as_view(),name='SignUp'),
    path('dashboard', views.Dashboard.as_view(),name='Dashboard'),
    path('add-airticle', views.AddAirticle.as_view(), name='AddAirticle'),
    path('logout', views.Logout.as_view(), name='Logout'),
    path('search', views.UserSearch.as_view(), name='search'),
    path('user-posts', views.UserPosts.as_view(), name='user-posts'),
]
