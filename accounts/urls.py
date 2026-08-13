from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
    path("add-student/", views.add_student, name="add_student"),
      path("register/", views.register_view, name="register"),
    path("students/", views.student_list, name="student_list"),
    path("edit-student/<int:id>/", views.edit_student, name="edit_student"),
    path("delete-student/<int:id>/", views.delete_student, name="delete_student"),
    path(
    "api/students/",
    views.student_api,
    name="student_api"
),
path(
    "api/students/<int:id>/",
    views.student_detail_api,
    name="student_detail_api"
),
]
