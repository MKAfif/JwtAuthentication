from django.contrib import admin
from django.urls import path
from app1 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', views.RegisterApi.as_view(), name='RegisterApi'),
    path('api/login/', views.LoginAPI.as_view(), name='LoginApi'),
    path('api/user_details/', views.User_details.as_view(),name='user_details'),
    path('api/delete_user/<int:user_id>/', views.UserDeleteView.as_view(), name='delete_user'),
    path('api/admin_login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('api/adduser/', views.AddUser.as_view(), name='addUser'),
    path('api/search/', views.AdminSearch.as_view(), name='admin-search'),
    
    
]
