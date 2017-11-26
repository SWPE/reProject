from django.shortcuts import render, redirect
import os
import hashlib
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required

def index(request):
    authtoken = False
    permtoken = False
    if request.user.is_authenticated():
        authtoken = True 
    context = {"people":Person.objects.all(), "authtoken":authtoken, "permtoken":permtoken}
    return render(request, "app/index.html", context)

def lectures(request):
    authtoken = False
    permtoken = False
    if request.user.is_authenticated() and request.user.has_perm("app.change_lecture"):
        permtoken = True
    if request.user.is_authenticated():
        authtoken = True
    if request.method == "GET":
        context = {"lectures":Lecture.objects.all(), "files":CustomFile.objects.all(), "authtoken":authtoken, "permtoken":permtoken}
        return render(request, "app/lectures.html", context)
    if request.method == "POST":
        Lecture.objects.create(
                subject = request.POST["subject"],
                description = request.POST["description"],
                hash = makeHash(request.POST["subject"])
                )
        CustomFile.objects.create(
                file_name = request.FILES["lecture"].name,
                file_source = handle_file(request.FILES["lecture"], request.FILES["lecture"].name, "lectures"),
                hash = makeHash(request.POST["subject"])
                )
        return redirect("/lectures/")
def homework(request):
    authtoken = False
    permtoken = False
    if request.user.is_authenticated() and request.user.has_perm("app.change_homework"):
        permtoken = True       
    if request.user.is_authenticated():
        authtoken = True 
    if request.method == "GET":
        context = {"homeworks":Homework.objects.all(), "files":CustomFile.objects.all(), "authtoken":authtoken, "permtoken":permtoken}
        return render(request, "app/homework.html", context)
    if request.method == "POST":
        import datetime
        hashkey = datetime.datetime.now()
        Homework.objects.create(
                    subject = request.POST["subject"],
                    issue_date = request.POST["whenGiven"],
                    submission_date = request.POST["whenPass"],
                    task_text = request.POST["description"],
                    hash = makeHash(request.POST["subject"], hashkey)
                )
        for f in request.FILES.getlist("homework"):
            CustomFile.objects.create(      
                    file_name = normalizeName(f.name),
                    file_source = handle_file(f, normalizeName(f.name), "homeworks"),
                    hash = makeHash(request.POST["subject"], hashkey)
                )
        return redirect("/homework/")
def info(request):
    authtoken = False
    permtoken = False
    if request.user.is_authenticated() and request.user.has_perm("app.change_importantinfo"):
        permtoken = True       
    if request.user.is_authenticated():
        authtoken = True 
    if request.method == "GET":
        context = {"info":ImportantInfo.objects.all(), "files":CustomFile.objects.all(), "authtoken":authtoken, "permtoken":permtoken}
        return render(request, "app/info.html", context)
    if request.method == "POST":
        import datetime 
        hashkey = datetime.datetime.now()
        ImportantInfo.objects.create(
                    title = request.POST["title"],
                    info = request.POST["info"],
                    date = hashkey,
                    hash = makeHash(request.POST["title"], hashkey)
                )
        for f in request.FILES.getlist("data"):
            CustomFile.objects.create(
                        file_name = normalizeName(f.name),
                        file_source = handle_file(f,normalizeName(f.name),"info"),
                        hash = makeHash(request.POST["title"], hashkey)
                    )
        return redirect("/info/")

def meetings(request):
    authtoken = False
    permtoken = False
    if request.user.is_authenticated() and request.user.groups.filter(name="members").exists():
        permtoken = True       
    if request.user.is_authenticated():
        authtoken = True 
    context = {"meeting":Meeting.objects.all(), "people":Person.objects.all(), "authtoken":authtoken, "permtoken":permtoken}
    return render(request, "app/meetings.html", context)
def download(request, dirname, filename):
    path = "app/media/%s/%s" % (dirname, filename) 
    file_path = path
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/force-download")
        response['Content-Disposition'] = 'attachment; filename=' + filename
        return response

def registration(request):
    if request.method == "GET":
        return render(request,"app/registration.html", {})
    if request.method == "POST":
        User.objects.create_user(request.POST["nickname"], request.POST["email"], makeHash(request.POST["password"]))
        g = Group.objects.get(name="user")
        for user in User.objects.filter(username=request.POST["nickname"]):
            g.user_set.add(user)
        return redirect("/registration/")
def signin(request):
    if request.method == "GET":
        return render(request, "app/signin.html", {})
    if request.method == "POST":
        user = authenticate(username=request.POST["nickname"], password=makeHash(request.POST["password"]))
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("")
            else:
                return HttpResponse("Not active")
        else:
            return HttpResponse("Not authorized")


def signout(request):
   logout(request)
   return redirect("/")



def handle_file(file, name, storage):
    for data in file.chunks():
        with open("app/media/%s/%s" % (storage, name), "ab") as f:
            f.write(data)
    return "/downloads/%s/%s" % (storage, name)

def makeHash(sth, hashkey=""):
    import hashlib
    if hashkey:
        return hashlib.sha256(b"%s%s" % (sth.encode("utf-8"), hashkey.__str__().encode("utf-8"))).hexdigest()
    return hashlib.sha256(b"%s" % sth.encode("utf-8")).hexdigest()
def normalizeName(name):
    sep = "_"
    return sep.join(name.split(" "))
