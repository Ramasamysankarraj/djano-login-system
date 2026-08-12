from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student


def login_view(request):

    # If already logged in, go directly to dashboard
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "accounts/login.html")


@login_required
def dashboard(request):

    student_count = Student.objects.count()

    return render(
        request,
        "accounts/dashboard.html",
        {"student_count": student_count}
    )

def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def add_student(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        age = request.POST.get("age")
        course = request.POST.get("course")

        Student.objects.create(
            name=name,
            email=email,
            age=age,
            course=course
        )

        return redirect("student_list")

    return render(request, "accounts/add_student.html")


@login_required
def student_list(request):

    students = Student.objects.all()

    return render(
        request,
        "accounts/student_list.html",
        {"students": students}
    )


@login_required
def edit_student(request, id):

    student = Student.objects.get(id=id)

    if request.method == "POST":

        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.age = request.POST.get("age")
        student.course = request.POST.get("course")

        student.save()

        return redirect("student_list")

    return render(
        request,
        "accounts/edit_student.html",
        {"student": student}
    )


@login_required
def delete_student(request, id):

    student = Student.objects.get(id=id)
    student.delete()

    return redirect("student_list")