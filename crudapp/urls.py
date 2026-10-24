from django.urls import path
from .views import *

urlpatterns=[
    path('',Home_view,name='home'),
    path('login/',Login_view,name='login'),
    path('logout/',Logout_view,name='logout'),
    path('register/',Register_view,name="register"),
    path('dashboard/',Dashboard_view,name="dashboard"),
    path("add_student",Create_View,name="add_student"),
    path('update_student/<int:student_id>',Update_view,name='update_student'),
    path('delete_student/<int:id>',Delete_view,name='delete_student'),
]