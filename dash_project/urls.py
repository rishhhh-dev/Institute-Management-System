"""
URL configuration for dash_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dash_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.RegisterView,name='regsiter_user'),
    path('login/',views.LoginView,name='login_user'),
    path('logout/',views.LogoutView,name='logout'),
    path('verify-otp/',views.VerifyView,name='otp-verify'),
    path('dashboard/',views.DashboardView,name='dashboard'),
    path('students/',views.StudentsView,name='all-students'),
    path('create-student/',views.StudentCreateView,name='create-student'),
    path('edit-student/<int:pk>/',views.StudentEditView,name='edit-student'),
    path('delete-student/<int:pk>/',views.StudentDeleteView,name='delete-student'),
    path('courses/',views.CoursesView,name='all-courses'),
    path('create-course/',views.CreateCourseView,name='create-course'),
    path('edit-course/<int:pk>',views.EditCourseView,name='edit-course'),
    path('delete-course/<int:pk>',views.DeleteCourseView,name='delete-course'),
]+static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
