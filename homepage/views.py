from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.contrib.admin.views.decorators import staff_member_required
# from django.contrib import messages

from homepage.models import Recipe, Author

from homepage.forms import RecipeForm, AuthorForm, LoginForm
from django import forms

# Create your views here.


def index(request):
    html = "index.html"
    my_recipes = Recipe.objects.all()
    return render(request, html, {"recipes": my_recipes, "welcome_name": "Box"})


def post_detail(request, post_id):
    html = "post_detail.html"
    my_recipe = Recipe.objects.filter(id=post_id).first()
    user = Author.objects.all()
    if request.user.is_authenticated:
        user = Author.objects.filter(user=request.user).first()
        favorites = user.favorites.all()
    else:
        favorites = []
    return render(request, html, {"post": my_recipe, 'favorites': favorites, 'user': user})


def author_details(request, post_id):
    html = "author_details.html"
    my_author = Author.objects.filter(id=post_id).first()
    my_recipe = Recipe.objects.filter(author=my_author.id)
    favorites = Recipe.objects.filter(id__in=my_author.favorites.all())
    return render(request, html, {"post": my_author, "recipes": my_recipe, 'favorites': favorites})


@login_required
def recipe_view_form(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                title=data.get('title'),
                body=data.get('body'),
                instructions=data.get('instructions'),
                time_required=data.get('time_required'),
                author=data.get('author')
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = RecipeForm()
    return render(request, "basic_form.html", {"form": form})


# @staff_member_required()
@login_required
def author_view_form(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = AuthorForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_user = User.objects.create_user(username=data.get(
                    "username"), password=data.get("password"))
                Author.objects.create(name=data.get("username"), user=new_user)
                # login(request, new_user)
                return HttpResponseRedirect(reverse("homepage"))
    else:
        return HttpResponse('Do not have proper credentials, return to homepage')
    form = AuthorForm()
    return render(request, "basic_form.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))

    form = LoginForm()
    return render(request, "basic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


def add_favorite_view(request, post_id):
    current_user = Author.objects.get(user=request.user)
    fav_recipe = Recipe.objects.filter(id=post_id).first()
    current_user.favorites.add(fav_recipe)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_favorite_view(request, post_id):
    current_user = Author.objects.get(user=request.user)
    fav_recipe = Recipe.objects.filter(id=post_id).first()
    current_user.favorites.remove(fav_recipe)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_recipe_view(request, post_id):
    recipe = Recipe.objects.get(id=post_id)

    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe.title = data['title']
            recipe.body = data['body']
            recipe.instructions = data['instructions']
            recipe.time_required = data['time_required']
            recipe.author = data['author']
            recipe.save()
        return HttpResponseRedirect(reverse('post_detail', args=[recipe.id]))

    data = {
        'title': recipe.title,
        'body': recipe.body,
        'instructions': recipe.instructions,
        'time_required': recipe.time_required,
        'author': recipe.author,
    }
    form = RecipeForm(initial=data)
    if not request.user.is_staff:
        form.fields['author'] = forms.ModelChoiceField(
            queryset=Author.objects.filter(name=request.user.author))
    return render(request, 'basic_form.html', {'form': form})
