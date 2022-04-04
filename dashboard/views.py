from django.core.checks import messages
from django.shortcuts import redirect, render
import requests
from django.contrib.auth import authenticate, login, logout

from .models import *
from .forms import *
from django.contrib import messages

from youtubesearchpython import VideosSearch

# Create your views here.


def home(request):
    return render(request, 'dashboard/home.html')


def notes(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = NotesForm(request.POST)
            if form.is_valid():
                notes = Notes(
                    user=request.user, title=request.POST['title'], description=request.POST['description'])
                notes.save()
            messages.success(
                request, f"Notes added succesfully by {request.user.username}!")
        else:
            form = NotesForm()
    else:
        return redirect("register")

    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)


def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


def detail(request, pk=None):
    note = Notes.objects.get(id=pk)
    context = {'note': note}
    return render(request, 'dashboard/notes_detail.html', context)


def homework(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            subject = request.POST.get("subject")
            title = request.POST.get("title")
            description = request.POST.get("description")
            due = request.POST.get("due")
            is_finished = request.POST.get("is_finished")
            if is_finished == 'on':
                finished = True
            else:
                finished = False
            print(subject, title, description, due, is_finished)
            homework = Homework(user=request.user, subject=subject, title=title,
                                description=description, due=due, is_finished=finished)
            homework.save()
            messages.success(
                request, f"Homework added succesfully by {request.user.username}!")
    else:
        return redirect("register")

    homeworks = Homework.objects.filter(user=request.user)

    if len(homeworks) == 0:
        homework_dones = True
    else:
        homework_dones = False
    context = {'homeworks': homeworks,
               'homework_dones': homework_dones, }
    return render(request, 'dashboard/homework.html', context)


def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()

    return redirect("homework")


def youtube(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnails': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'viewcount': i['viewCount']['short'],
                'publishedTime': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list,
            }

        return render(request, 'dashboard/youtube.html', context)

    else:
        form = DashboardForm()
    form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)


def todo(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = TodoForm(request.POST)
            if form.is_valid():
                if request.POST['is_finished'] == 'on':
                    finished = True
                else:
                    finished = False

                todos = Todo(user=request.user,
                             title=request.POST['title'], is_finished=finished)
                todos.save()
            messages.success(
                request, f"Todos added succesfully by {request.user.username}!")
        else:
            form = TodoForm()
    else:
        return redirect("register")

    todos = Todo.objects.filter(user=request.user)

    context = {
        'todos': todos,
        'form': form,
    }
    return render(request, 'dashboard/todo.html', context)


def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()

    return redirect("todo")


def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect("todo")


def books(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)
        text = request.POST['text']

    else:
        form = DashboardForm()

    context = {
        'form': form, }

    return render(request, 'dashboard/books.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!!")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'dashboard/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login")
