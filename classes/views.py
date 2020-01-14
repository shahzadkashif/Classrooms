from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Classroom, Student
from .forms import ClassroomForm, StudentForm
from .forms import SignupForm, SigninForm

def signup(request):
	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()

			login(request, user)
			return redirect("classroom-list")
	context = {
		"form":form,
	}
	return render(request, 'signup.html', context)

def signin(request):
	form = SigninForm()
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('classroom-list')
	context = {
		"form":form
	}
	return render(request, 'signin.html', context)

def signout(request):
	logout(request)
	return redirect("signin")

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	students = Student.objects.filter(classroom=classroom)
	context = {
		"classroom": classroom,
		"students": students,
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if request.user.is_anonymous:
		messages.error(request, "Please sign in to create a new class")
		return redirect('signin')
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST)
		if form.is_valid():
			classroom = form.save(commit=False)
			classroom.teacher = request.user
			classroom.save()
			messages.success(request, "Classroom Successfully Created!")
			return redirect('classroom-list')
	context = {
		"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if request.user == classroom.teacher:
		form = ClassroomForm(instance=classroom)
		if request.method == "POST":
			form = ClassroomForm(request.POST, instance=classroom)
			if form.is_valid():
				form.save()
				messages.success(request, "Successfully Edited!")
				return redirect('classroom-list')
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	Classroom.objects.get(id=classroom_id).delete()
	if request.user == classroom.teacher:
		messages.success(request, "Successfully Deleted!")
		return redirect('classroom-list')

def student_create(request, classroom_id):
	form = StudentForm()
	classroom = Classroom.objects.get(id=classroom_id)
	if request.user == classroom.teacher:
		if request.method == "POST":
			form = StudentForm(request.POST)
			if form.is_valid():
				student = form.save(commit=False)
				student.classroom = classroom
				student.save()
				messages.success(request, "Student Successfully Added!")
				return redirect(classroom.get_absolute_url())
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'create_student.html', context)

def student_update(request, classroom_id, student_id):
	student = Student.objects.get(id=student_id)
	classroom = Classroom.objects.get(id=classroom_id)
	if request.user == classroom.teacher:
		form = StudentForm(instance=student)
		if request.method == "POST":
			form = StudentForm(request.POST, instance=student)
			if form.is_valid():
				form.save()
				messages.success(request, "Student Successfully Edited!")
				return redirect(classroom.get_absolute_url())
	context = {
	"form": form,
	"student": student,
	"classroom": classroom,
	}
	return render(request, 'update_student.html', context)


def student_delete(request, classroom_id, student_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if request.user == classroom.teacher:
		Student.objects.get(id=student_id).delete()
		messages.success(request, "Student Successfully Deleted!")
		return redirect(classroom.get_absolute_url())
