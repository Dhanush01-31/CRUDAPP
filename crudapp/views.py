from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from .models import Student
# email validate package
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .tasks import send_welcome_email


# Create your views here.
# def First_view(request):
#     return HttpResponse('This is my first Django view. I am learning django.')

# Home View 
def Home_view(request):
    return render(request, 'home.html')

# Login View
def Login_view(request):
    # redirects user to dashboard if user already loggedin
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        username = str(request.POST.get('username')).lower().strip()
        password = str(request.POST.get('password')).lower().strip()

        # email Validation
        if not username:
            messages.error(request,'Email field is missing')
            return redirect('login')

        # password validation
        if not password:
            messages.error(request,'Password is required')
            return redirect

        # Authentication process
        try:
            if '@' in username:
                user_object = User.objects.get(email__iexact = username)
            else:
                user_object = username
            
            user = authenticate(request, username = user_object,password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Sucessfull')
                return redirect('dashboard')
            else:
                messages.error(request,'Invalid username or password')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User Does Not Exist')
            return redirect('login')
        
    return render(request, 'login.html')

# Register_view
def Register_view(request):
    if request.method == "POST":
        firstname = str(request.POST.get('firstname')).lower().strip()
        lastname = str(request.POST.get('lastname')).lower().strip()
        email = str(request.POST.get('email')).lower().strip()
        password = str(request.POST.get('password')).lower().strip()
        confirm_password = str(request.POST.get('confirm_password')).lower().strip()

        # First name validation
        if not firstname:
            messages.error(request,'The firstname is mandatory for registration')
            return redirect('register')

        # Lastname validation
        if not lastname:
            messages.error(request,'Lastname is mandatory for registration')
            return redirect('register')
        
        # email validation
        if not email:
            messages.error(request,'Email is mandatory for regitration')
            return redirect('register')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email")
            return redirect('register')
        
        # password validation
        if not password:
            messages.error(request,'Password is mandatory for registration')
            return redirect('register')
        
        # confirm password validation
        if not confirm_password:
            messages.error(request,'Confirm password is mandatory for registration')
            return redirect('register')

        # password length check.
        if len(password) < 8 or len(confirm_password) < 8 :
            messages.error(request, 'The password should be greater than 8 characters')
            return redirect('register')

        # password and confirm_password not matching
        if password != confirm_password:
            messages.error(request,"Password aren't match eachother try again ")
            return redirect('register')


        # Checking email already exist or not
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request,'Email already exists try with another email')
            return redirect('register')

        # checking the username already exists or not
        if User.objects.filter(username__iexact=email.split('@')[0]).exists():
            messages.error(request,'Username already exists try with another username')
            return redirect('register')

        username = str(email.split('@')[0]).lower()

        Name=firstname+" "+lastname 

        usermail=email

        User.objects.create_user(first_name=firstname,last_name=lastname,email=email,password=password,username=username)
        
        messages.success(request, "Registration Successfully Done!")

        email_sent = send_welcome_email(request, username=username, password=password, Name=Name, usermail=usermail)
        if email_sent:
            messages.success(request, "A welcome email has been sent to your inbox.")
        else:
            messages.warning(request, "However, the welcome email could not be sent. Please check email settings.")

        return redirect('login')
    else:
        return render(request, 'register.html')


# Dashboard View
@login_required(login_url='login')
def Dashboard_view(request):
    students = Student.objects.all()
    context = {'students':students}
    return render(request, 'dashboard.html',context)

# Logout view
@login_required(login_url='login')
def Logout_view(request):
    logout(request)
    messages.success(request,'Logout Successfully')
    return redirect('login')


# Create View.
@login_required(login_url='login')
def Create_View(request):
    if request.method == "POST":
        name = str(request.POST.get('name')).strip().lower()
        age = request.POST.get('age')
        email = str(request.POST.get('email')).strip().lower()

        if not name:
            messages.error(request,"Fill the name field.")
            return redirect('dashboard')

        if not age:
            messages.error(request,"Fill the age field")
            return redirect('dashboard')
        
        if not email:
            messages.error(request,"Fill the email field")

        # Email not exists validation.
        if Student.objects.filter(email__iexact=email).exists():
            messages.error(request,"Email Already Exists")
            return redirect('dashboard')

        Student.objects.create(name=name,age=age,email=email)

        messages.success(request,"Student created successfully")
        return redirect('dashboard')

    return render(request,"dashbaord.html")

# Update View
@login_required(login_url='login')
def Update_view(request,student_id):
    try:
        student = get_object_or_404(Student,pk=student_id)
    except Student.DoesNotExist:
        print("Student Does not exist")
        return redirect('dashboard')

    if request.method == "POST":
        student.name = str(request.POST.get('name')).strip().lower()
        student.age = request.POST.get('age')
        student.email = str(request.POST.get('email')).strip().lower()

        student.save()
        messages.success(request,"Student data Updated Successfully")
        return redirect('dashboard')
    
    return redirect('dashboard')

# delete_view
def Delete_view(request,id):
    try:
        student = get_object_or_404(Student,pk=id)
    except Student.DoesNotExist:
        messages.error(request,"Student Does not Exist")
        return redirect('dashboard')
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student Deleted successfully")
        return redirect('dashboard')

    return redirect('dashboard')