
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from collegeapp.models import teachers
from collegeapp.models import course
from collegeapp.models import student
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import course, teachers
import re



# Create your views here.
def loginpage(request):
    return render(request, 'login.html')

def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff == 1:
                 login(request,user)
                 return redirect('home')
            else:
            # request.session["uid"]=user.id
             auth.login(request,user)
             messages.info(request,f'welcome {username}')
             return redirect('teacherhome')
        else:
            messages.info(request,"invalid username or password")
            return redirect('loginpage')
    return render(request,'login.html')


def home(request):
    return render(request, 'home.html')
def teacherhome(request):
    return render(request, 'teacher_home.html')
def addcourse1(request):
    return render(request, 'add_course.html')
def addcourse(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_fee = request.POST.get('fee')

        if course_name and course_fee:
            course.objects.create(
                course_name=course_name,
                fee=course_fee
            )
            messages.success(request, "Course added successfully")
        else:
            messages.error(request, "All fields are required")

        return redirect('addcourse1')

def add_student(request):
    courses = course.objects.all()
    return render(request, 'add_student.html', {'course': courses})


def add_studentdb(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        age = request.POST.get('age')
        date = request.POST.get('date')
        sel = request.POST.get('sel')

        if not all([full_name, address, age, date, sel]):
            messages.error(request, "All fields are required")
            return redirect('add_student')

        selected_course = course.objects.get(id=sel)

        student_obj = student.objects.create(
            full_name=full_name,
            address=address,
            age=age,
            joining_date=date,
            course=selected_course
        )

        messages.success(request, "Student added successfully")
        return redirect('add_student')

def showstudents(request):
    students = student.objects.all()
    return render(request, 'show_students.html', {'student': students})


def editstudents(request, pk):
    stud = get_object_or_404(student, id=pk)
    courses = course.objects.all()

    return render(request, 'edit_students.html', {
        'stud': stud,
        'course': courses
    })

def editdb(request, pk):
    stud = get_object_or_404(student, id=pk)

    if request.method == 'POST':
        stud.full_name = request.POST.get('full_name')
        stud.address = request.POST.get('address')
        stud.age = request.POST.get('age')
        stud.joining_date = request.POST.get('date')

        sel = request.POST.get('sel')
        stud.course = get_object_or_404(course, id=sel)

        stud.save()
        return redirect('showstudents')

    return redirect('showstudents')




def delete(request, pk):
    stud = get_object_or_404(student, id=pk)
    stud.delete()
    return redirect('showstudents')

def signup(request):
    return render(request, 'signup.html')



def signup1(request):
    courses = course.objects.all()   # Fetch courses
    context = {'course': courses}

    if request.method == 'POST':
        # Get form data
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        age = request.POST.get('age', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        password = request.POST.get('password', '')
        cpassword = request.POST.get('cpassword', '')
        sel = request.POST.get('sel')
        image = request.FILES.get('file')

        errors = []

        # PASSWORD MATCH
        if password != cpassword:
            errors.append("Passwords do not match.")

        # USERNAME UNIQUE
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")

        # EMAIL UNIQUE
        if User.objects.filter(email=email).exists():
            errors.append("Email already exists.")

        # PHONE VALIDATION
        if not re.fullmatch(r'[6-9]\d{9}', contact_number):
            errors.append("Enter a valid 10-digit Indian phone number starting with 6-9.")

        # AGE VALIDATION
        if not age.isdigit() or int(age) <= 0:
            errors.append("Enter a valid age.")

        # COURSE SELECTED
        if not sel:
            errors.append("Please select a course.")

        # IF THERE ARE ERRORS, SHOW FORM AGAIN
        if errors:
            context.update(request.POST)  # Keep user-entered data
            context['errors'] = errors
            return render(request, 'signup.html', context)

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fname,
            last_name=lname
        )

        # CREATE TEACHER
        selected_course = course.objects.get(id=sel)
        teachers.objects.create(
            user=user,
            address=address,
            age=int(age),
            contact_number=contact_number,
            image=image,
            course=selected_course
        )

        messages.success(request, "Registration successful")
        return redirect('loginpage')

    return render(request, 'signup.html', context)



def delete1(request, pk):
    t = get_object_or_404(teachers, id=pk)
    t.delete()
    return redirect('view_teachers')

# def profile(request):
#     teacher, created = teachers.objects.get_or_create(
#         user=request.user
#     )
#     return render(request, 'profile.html', {'users': teacher})
@login_required
def profile(request):
    teacher, created = teachers.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'teacher': teacher})






@login_required




def edit_teacher(request):
    teacher, created = teachers.objects.get_or_create(user=request.user)
    all_courses = course.objects.all()  # send all courses to template

    if request.method == 'POST':
        # GET FORM DATA
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        age = request.POST.get('age') or None
        contact_number = request.POST.get('contact_number')
        sel = request.POST.get('sel')

        # ===== PHONE VALIDATION =====
        if not re.fullmatch(r'[6-9]\d{9}', contact_number):
            messages.error(request, "Enter a valid 10-digit Indian phone number starting with 6-9")
            return redirect('edit_teacher')

        # ===== EMAIL VALIDATION =====
        if User.objects.exclude(id=request.user.id).filter(email=email).exists():
            messages.error(request, "This email is already in use")
            return redirect('edit_teacher')

        # ===== USER UPDATE =====
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.username = username
        request.user.email = email
        request.user.save()

        # ===== TEACHER UPDATE =====
        teacher.address = address
        teacher.age = age
        teacher.contact_number = contact_number

        if sel:
            teacher.course = course.objects.get(id=sel)

        if 'file' in request.FILES:
            teacher.image = request.FILES['file']

        teacher.save()

        messages.success(request, "Profile updated successfully")
        return redirect('edit_teacher')

    return render(request, 'edit_teacher.html', {
        'teacher': teacher,
        'course': all_courses
    })


@login_required(login_url='loginpage')
def logout_user(request):
    logout(request)
    return redirect('loginpage') 
@login_required
def view_teachers(request):
    all_teachers = teachers.objects.select_related('user').all()
    return render(request, 'show_teachers.html', {
        'teachers': all_teachers
    })