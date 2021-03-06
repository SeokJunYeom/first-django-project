from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect, QueryDict
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Character
from .forms import CharacterForm
import os

# Create your views here.

month_dic = {
    "January" : '1',
    "February" : '2',
    "March" : '3',
    "April" : '4',
    "May" : '5',
    "June" : '6',
    "July" : '7',
    "August" : '8',
    "September" : '9',
    "October" : '10',
    "November" : '11',
    "December" : '12'
}

def gochiusa(request):
    if request.method == "POST":
        if not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_URL)

        else:
            character_pk = request.POST.get("pk")
            character = Character.objects.get(pk = character_pk)

            os.remove("media/" + character.image.name )
            character.delete()

            return HttpResponseRedirect("/")

    if not request.user.is_authenticated():
        user = ""

    else:
        user = request.user

    characters = Character.objects.all().order_by("name")
    context = {"characters" : characters, "user" : user}

    return render(request, "gochius.html", context)

def character(request, name):
    character = Character.objects.get(name = name)
    
    return render(request, "character.html", {"character" : character})

@login_required
def character_post(request):
    if request.method == "POST":
        birth = request.POST.get("birth").split(',')[0]
        request.POST = request.POST.copy()
        request.POST["birth"] = stdBirth(birth)

        form = CharacterForm(request.POST, request.FILES)

        if form.is_valid():
            new_form = form.save(commit = False)
            new_form.user = request.user
            new_form.save()

            return HttpResponseRedirect("../../")

    return render(request, 'post.html', {})

def stdBirth(birth):
    month = month_dic[birth.split(' ')[1]]
    day = birth.split(' ')[0]

    return month + '/' + day
