from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from homepage.models import Recipe

from homepage.models import Author

# from homepage.forms import RecipeForm, AuthorForm, LoginForm, SignupForm
from homepage.forms import RecipeForm, AuthorForm, LoginForm

# Create your views here.


def index(request):
    html = "index.html"
    my_recipes = Recipe.objects.all()
    return render(request, html, {"recipes": my_recipes, "welcome_name": "Box"})


def post_detail(request, post_id):
    html = "post_detail.html"
    my_recipe = Recipe.objects.filter(id=post_id).first()
    return render(request, html, {"post": my_recipe})


def author_details(request, post_id):
    html = "author_details.html"
    my_author = Author.objects.filter(id=post_id).first()
    my_recipe = Recipe.objects.filter(author=my_author.id)
    return render(request, html, {"post": my_author, "recipes": my_recipe})


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
                author=request.user.author
            )
            return HttpResponseRedirect(reverse("homepage"))

    form = RecipeForm()
    return render(request, "basic_form.html", {"form": form})


@login_required
def author_view_form(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        form.save()
        if form.is_valid():
            data = form.cleaned_data
            new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
            login(request, new_user)
            return HttpResponseRedirect(reverse("homepage"))
        # return HttpResponseRedirect(reverse("homepage"))

    form = AuthorForm()
    return render(request, "basic_form.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get("username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))

    form = LoginForm()
    return render(request, "basic_form.html", {"form": form})


# def signup_view(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             new_user = User.objects.create_user(username=data.get("username"), password=data.get("password"))
#             login(request, new_user)
#             return HttpResponseRedirect(reverse("homepage"))
#
#     form = SignupForm()
#     return render(request, "basic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))

