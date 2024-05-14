from django.shortcuts import render,redirect
import smtplib
import random
import math
from .models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login,logout
from .models import Student,Course
from django.contrib.auth.decorators import login_required

# Create your views here.


def RegisterView(request):
    if request.method == 'POST':
        
        try:
            first_name = request.POST.get('fname','')
            last_name = request.POST.get('lname','')
            email = request.POST.get('email','')
            username = request.POST.get('username','')
            password1 = request.POST.get('password1','')
            
            email_check = User.objects.filter(email=email)
            user_check = User.objects.filter(username=username)
            if email_check.exists():
                messages.error(request,"Email Already Exists")
                print("Email Already Exists.")
                # return Response("Email Already Exists.")
            elif user_check.exists():
                print("User Already Exists.") 
            else:
                if email:
                    digits = '0123456789'
                    otp_val = ''
                    for i in range(6):
                        otp_val+=digits[math.floor(random.random() * 10)]

                    print(otp_val)

                    sender = 'rishigupta92173@gmail.com'
                    receiver = [email]
                    email_subject = "OTP for user verfication."
                    email_text = f"""
                                Use this OTP for login {otp_val}
                                """
                    message = "From: %s\r\n" % sender \
                              + "To: %s\r\n" % receiver \
                              + "Subject: %s\r\n" % email_subject \
                              + "\r\n" \
                              + email_text
                    smtp_obj = smtplib.SMTP('smtp.gmail.com',587)
                    password = 'kotr jqgc bwth uxbz'
                    smtp_obj.starttls()
                    smtp_obj.login(sender,password)
                    smtp_obj.sendmail(sender,receiver,message)
                    
                    password1 = make_password(password1)
                    User.objects.create(first_name=first_name,last_name=last_name,email=email,username=username,password=password1,otp=otp_val)
                    return redirect('/verify-otp/')
        except Exception as e:
            print(e)
    return render(request,'register.html')


def VerifyView(request):
    try:
        if request.method == 'POST':
            digit1 = request.POST.get('digit1','')
            digit2 = request.POST.get('digit2','')
            digit3 = request.POST.get('digit3','')
            digit4 = request.POST.get('digit4','')
            digit5 = request.POST.get('digit5','')
            digit6 = request.POST.get('digit6','')
            try:
                input_otp = int(digit1+digit2+digit3+digit4+digit5+digit6)
                check_otp = User.objects.filter(otp=input_otp)
                if check_otp.exists():
                    print('OTP Verified')
                    messages.success(request,'Verification Successful')
                    return redirect('/login/')
                else:
                    print('Incorrect OTP')
                    messages.error(request,"Incorrect OTP")
            except Exception as e:
                messages.error(request,"Please enter the otp")
        return render(request,'otp.html')
    
    except Exception as e:
        messages.error(request,"Please enter the otp")

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        print(user,"uuu")
        if user is not None:
            login(request,user)
            messages.success(request,'You are logged in successfuly')
            return redirect('/dashboard/')
        else:
            messages.error(request,'Invalid Details')
            print("invalid user")

    return render(request,'login.html')

def LogoutView(request):
    logout(request)
    messages.success(request,'User Logged Out!')
    return redirect('/login/')

@login_required(login_url='/login/')
def DashboardView(request):
    total_students = Student.objects.all().count()
    total_courses = Course.objects.all().count()
    data = {
        'students':total_students,
        'courses': total_courses,
    }
    return render(request,'dashboard.html',{'data':data})


def StudentsView(request):
    students = Student.objects.all().order_by('-id')
    return render(request,'students.html',{'students':students})

def StudentCreateView(request):
    if request.method == 'POST':
        name = request.POST.get('sname','')
        email = request.POST.get('semail','')
        phone = request.POST.get('sphone','')
        location = request.POST.get('slocation','')
        course = request.POST.get('scourse','')

        course_filter = Course.objects.filter(name=course).first()
        Student.objects.create(name=name,email=email,phone=phone,location=location,course=course_filter)

        messages.success(request,"New Student Created")
        return redirect('/create-student/')
    else:
        courses = Course.objects.all()
        return render(request,'student_create.html',{'courses':courses})

def StudentEditView(request,pk):
    if request.method == 'POST':
        name = request.POST.get('sname','')
        email = request.POST.get('semail','')
        phone = request.POST.get('sphone','')
        location = request.POST.get('slocation','')
        course = request.POST.get('scourse','')

        course_filter = Course.objects.filter(name=course).first()
        Student.objects.update(name=name,email=email,phone=phone,location=location,course=course_filter)
        messages.success(request,'Student Data Changed')
        return redirect(f'/edit-student/{pk}')
    else:
        student_data = Student.objects.filter(id=pk).first()
        print(student_data.course)
        return render(request,'student_edit.html',{'student':student_data})

def StudentDeleteView(request,pk):
    if request.method == 'POST':
        Student.objects.filter(id=pk).delete()
        messages.success(request,"Student Data Deleted")
        return redirect(f'/all-students/')
    else:
        return render(request,'student_delete.html')

def CoursesView(request):
    courses = Course.objects.all().order_by('-id')
    return render(request,'courses.html',{'courses':courses})

def CreateCourseView(request):
    if request.method == "POST":
        name = request.POST.get('course_name','')
        price = request.POST.get('course_price','')
        duration = request.POST.get('course_duration','')

        Course.objects.create(name=name,price=price,duration=duration)
        messages.success(request,'Course Added')
    return render(request,'course_add.html')

def EditCourseView(request,pk):
    if request.method == "POST":
        name = request.POST.get('course_name','')
        price = request.POST.get('course_price','')
        duration = request.POST.get('course_duration','')

        Course.objects.update(name=name,price=price,duration=duration)
        messages.success(request,'Course Changed Successfully')
        return redirect(f'/edit-course/{pk}')
    else:
        course_data = Course.objects.filter(id=pk).first()
        return render(request,'course_edit.html',{'data':course_data})

def DeleteCourseView(request,pk):
    if request.method == 'POST':
        Course.objects.filter(id=pk).delete()
        messages.success(request,'Course Deleted Successfully!')
        return redirect('/all-courses/')
    else:
        return render(request,'course_delete.html')