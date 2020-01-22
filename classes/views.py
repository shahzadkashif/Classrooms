from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth import login, authenticate, logout

from .models import Classroom, Student
from .forms import ClassroomForm, SignupForm, SigninForm, StudentForm

def classroom_list(request):
    if request.user.is_anonymous:
        return redirect('signin')

    classrooms = Classroom.objects.all()
    context = {
        "classrooms": classrooms,
    }
    return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')

    classroom = Classroom.objects.get(id=classroom_id)
    students = classroom.students.all().order_by('name','exam_grade')

    context = {
        "classroom": classroom,
        "students": students
    }
    return render(request, 'classroom_detail.html', context)


def classroom_create(request):
    if request.user.is_anonymous:
        return redirect('signin')

    form = ClassroomForm()
    if request.method == "POST":
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.teacher = request.user
            classroom.save()

            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    }
    return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')

    classroom = Classroom.objects.get(id=classroom_id)

    if not(classroom.teacher == request.user):
        messages.success(request, "Onlt the Teacher of this class can update the information!!!")
        return redirect('classroom-detail', classroom_id)

    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-list')
        print (form.errors)

    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')

    classroom = Classroom.objects.get(id=classroom_id)

    if not(classroom.teacher == request.user):
        messages.success(request, "Only the Teacher of this classroom can  delete Student's Info!!!")
        return redirect('classroom-detail', classroom_id)

    Classroom.objects.get(id=classroom_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-list')


def student_add(request, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')

    classroom = Classroom.objects.get(id=classroom_id)

    if not(classroom.teacher == request.user):
        messages.success(request, "Only the Teacher of this classroom  can add a student(s)!!!")
        return redirect('classroom-detail', classroom_id)

    form = StudentForm()
    
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom = classroom
            student.save()
            return redirect('classroom-detail', classroom_id)
    context = {
        "form":form,
        "classroom": classroom,
    }
    return render(request, 'student_add.html', context)


def student_update(request, student_id, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')

    classroom = Classroom.objects.get(id=classroom_id)
    student = Student.objects.get(id=student_id)

    if not(classroom.teacher == request.user):
        messages.success(request, "Only The Teacher of this classroom can update student's information!!!")
        return redirect('classroom-detail', classroom_id)
    
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            print(form)
            return redirect('classroom-detail', classroom_id)

    context = {
        "form": form,
        "classroom": classroom,
        "student": student,

    }
    return render(request, 'student_update.html', context)


def student_delete(request, student_id, classroom_id):
    if request.user.is_anonymous:
        return redirect('signin')

    classroom = Classroom.objects.get(id=classroom_id)

    if not(classroom.teacher == request.user):
        messages.success(request, "Teacher of this classroom only can delete students!!!")
        return redirect('classroom-detail', classroom_id)

    else:
        Student.objects.get(id=student_id).delete()
        messages.success(request, "Successfully Deleted!")
        return redirect('classroom-detail', classroom_id)


def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form =  SignupForm(request.POST)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.set_password(user_obj.password)
            user_obj.save()

            login(request, user_obj)
            return redirect('classroom-list')

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def signin(request):
    form = SigninForm()
    if request.method == "POST":
        form =  SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user_obj = authenticate(username=username, password=password)
            if user_obj is not None:
                login(request, user_obj)
                return redirect('classroom-list')      

    context = {
        'form': form,
    }
    return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    return redirect('signin')








