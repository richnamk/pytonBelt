from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from ..login.models import User
from .models import Quote

def current_user(request):
    return User.objects.get(id=request.session['user_id'])


def flash_errors(request, errors):
    for error in errors:
        messages.error(request, error)

def index(request):

    if 'user_id' not in request.session:
        return redirect('/')

    user = current_user(request)

    context = {
        'user': user, 
        'quotes': Quote.objects.all().exclude(favorited_by = user),
        'favorites': user.favorites.all()
    }
    return render(request, 'quotes/index.html', context)

def show_user(request, userid):

    user = User.objects.get(id = userid)

    context = {

        'user': user,

        'quotes': Quote.objects.filter(posted_by = user),

        'count': Quote.objects.filter(posted_by = user).count()
        }
    return render(request, 'quotes/user.html', context)

def create(request):
    if request.method == "POST":
        errors = Quote.objects.validate(request.POST)

        if not errors:
            user = current_user(request)
            Quote.objects.create_quote(request.POST, request.session["user_id"])

        flash_errors(request, errors)
    return redirect('/quotes')

def add_favorite(request,quote_id):

    user = User.objects.get(id=request.session["user_id"])

    favorite = Quote.objects.get(id=quote_id)

    user.favorites.add(favorite)

    return redirect('/quotes')


def delete_favorite(request,quote_id):
    user = User.objects.get(id=request.session["user_id"])
    favorite = Quote.objects.get(id=quote_id)
    user.favorites.remove(favorite)
    return redirect('/quotes')

