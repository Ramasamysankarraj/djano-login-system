from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages

from django.core.exceptions import ValidationError

from .models import Student


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    # If user is already logged in,
    # don't show the login page again.
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        # Check empty fields
        if not username or not password:

            return render(
                request,
                "accounts/login.html",
                {
                    "error": "Please enter both username and password."
                }
            )

        # Authenticate user
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Create login session
            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("dashboard")

        # Invalid username/password
        return render(
            request,
            "accounts/login.html",
            {
                "error": "Invalid username or password."
            }
        )

    return render(
        request,
        "accounts/login.html"
    )


# =========================================================
# REGISTER
# =========================================================

def register_view(request):

    # If already logged in,
    # don't allow user to register again.
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # -----------------------------------------
        # Check empty fields
        # -----------------------------------------

        if not username or not email or not password or not confirm_password:

            messages.error(
                request,
                "All fields are required."
            )

            return render(
                request,
                "accounts/register.html"
            )

        # -----------------------------------------
        # Check username length
        # -----------------------------------------

        if len(username) < 4:

            messages.error(
                request,
                "Username must contain at least 4 characters."
            )

            return render(
                request,
                "accounts/register.html"
            )

        # -----------------------------------------
        # Check username already exists
        # -----------------------------------------

        if User.objects.filter(username__iexact=username).exists():

            messages.error(
                request,
                "Username already exists. Please choose another."
            )

            return render(
                request,
                "accounts/register.html"
            )

        # -----------------------------------------
        # Check email already exists
        # -----------------------------------------

        if User.objects.filter(email__iexact=email).exists():

            messages.error(
                request,
                "An account with this email already exists."
            )

            return render(
                request,
                "accounts/register.html"
            )

        # -----------------------------------------
        # Check password confirmation
        # -----------------------------------------

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "accounts/register.html"
            )

        # -----------------------------------------
        # Validate password
        # -----------------------------------------

        try:

            validate_password(
                password
            )

        except ValidationError as e:

            for error in e.messages:

                messages.error(
                    request,
                    error
                )

            return render(
                request,
                "accounts/register.html"
            )

        # -----------------------------------------
        # Create user
        # -----------------------------------------

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")

    return render(
        request,
        "accounts/register.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    # Count total students
    student_count = Student.objects.count()

    return render(
        request,
        "accounts/dashboard.html",
        {
            "student_count": student_count
        }
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("login")


# =========================================================
# ADD STUDENT
# =========================================================

@login_required
def add_student(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        age = request.POST.get("age", "").strip()
        course = request.POST.get("course", "").strip()

        # -----------------------------------------
        # Validation
        # -----------------------------------------

        if not name or not email or not age or not course:

            messages.error(
                request,
                "All fields are required."
            )

            return render(
                request,
                "accounts/add_student.html"
            )

        # -----------------------------------------
        # Validate age
        # -----------------------------------------

        try:

            age = int(age)

            if age <= 0:
                raise ValueError

        except ValueError:

            messages.error(
                request,
                "Please enter a valid age."
            )

            return render(
                request,
                "accounts/add_student.html"
            )

        # -----------------------------------------
        # Create student
        # -----------------------------------------

        Student.objects.create(
            name=name,
            email=email,
            age=age,
            course=course
        )

        messages.success(
            request,
            "Student added successfully."
        )

        return redirect("student_list")

    return render(
        request,
        "accounts/add_student.html"
    )


# =========================================================
# STUDENT LIST
# =========================================================

@login_required
def student_list(request):

    students = Student.objects.all().order_by("-id")

    return render(
        request,
        "accounts/student_list.html",
        {
            "students": students
        }
    )


# =========================================================
# EDIT STUDENT
# =========================================================

@login_required
def edit_student(request, id):

    # Safely find student
    student = get_object_or_404(
        Student,
        id=id
    )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        age = request.POST.get("age", "").strip()
        course = request.POST.get("course", "").strip()

        # -----------------------------------------
        # Validation
        # -----------------------------------------

        if not name or not email or not age or not course:

            messages.error(
                request,
                "All fields are required."
            )

            return render(
                request,
                "accounts/edit_student.html",
                {
                    "student": student
                }
            )

        # -----------------------------------------
        # Validate age
        # -----------------------------------------

        try:

            age = int(age)

            if age <= 0:
                raise ValueError

        except ValueError:

            messages.error(
                request,
                "Please enter a valid age."
            )

            return render(
                request,
                "accounts/edit_student.html",
                {
                    "student": student
                }
            )

        # -----------------------------------------
        # Update student
        # -----------------------------------------

        student.name = name
        student.email = email
        student.age = age
        student.course = course

        student.save()

        messages.success(
            request,
            "Student updated successfully."
        )

        return redirect("student_list")

    return render(
        request,
        "accounts/edit_student.html",
        {
            "student": student
        }
    )


# =========================================================
# DELETE STUDENT
# =========================================================

@login_required
def delete_student(request, id):

    # Only allow POST request for deletion
    if request.method != "POST":

        messages.error(
            request,
            "Invalid delete request."
        )

        return redirect("student_list")

    # Safely find student
    student = get_object_or_404(
        Student,
        id=id
    )

    student.delete()

    messages.success(
        request,
        "Student deleted successfully."
    )

    return redirect("student_list")