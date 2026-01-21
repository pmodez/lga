from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from lga_app.models import Article, Category, Comment
from lga_app.forms import UpdateUserForm, ArticleForm, CommentForm


def home(request):
    return render(request, 'home.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            #messages.success(request, 'Vous êtes connecté !')
            return redirect('home')
        else:
            #messages.error(request, 'Email OU Mot de passe incorect')
            return redirect('login')
    else:
        return render(request,  "login.html", {})

    # REGISTER
def logout_user(request):
    logout(request)
    #messages.success(request, "Vous avez été deconnecté.")
    return redirect('home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, user_form.instance)
            messages.success(request, "Votre compte utilisateur a été modifié")
            return redirect('update_info')

        return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "Vous devez être connecté pour accéder à cette page.")
        return redirect('login')


def article_detail(request, pk):

    filter_segment = { }

    categories = Category.objects.all()


    context = {'categories': categories}

    if request.user.is_authenticated:

        comment_form = CommentForm(request.POST,pk)

        if request.method=='POST' and comment_form.is_valid():

            cd = comment_form.cleaned_data

            text = cd['text']

            comment = Comment(text=text, author=request.user, article_id=pk)
            comment.save()
            comment_form = CommentForm()

        comments = Comment.objects.filter(article=pk)
        #article_form = ArticleForm(request.POST or None, request.FILES or None)

        context = {'comment_form': comment_form, 'article': Article.objects.get(pk=pk), 'categories': categories, 'comments': comments}

        return render(request, "article.html",context)
    else:
        return render(request, "home.html",context)

def article_update(request, pk):

    filter_segment = { }

    categories = Category.objects.all()

    context = {'categories': categories}

    if request.user.is_authenticated:

        article = Article.objects.get(pk=pk)
        article_form = ArticleForm(request.POST or None, instance=article)

        if article_form.is_valid():
            print("in FORM VALID")
            article_form.save()
            context = {'article_form': article_form, 'article': article, 'categories': categories}
            return render(request, "article_update.html",context)

        else:
            context = {'article_form': article_form, 'article': article, 'categories': categories}
            return render(request, "article_update.html", context)

def article_delete(request, pk):

    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('home_articles')


def comment_delete(request, pk):

    categories = Category.objects.all()
    comment = Comment.objects.get(pk=pk)
    article = Article.objects.get(pk=comment.article_id)

    comment.delete()
    context = {'article': article, 'categories': categories}
    return render(request, "article.html", context)

def comment_update(request, pk):

    filter_segment = { }

    categories = Category.objects.all()

    context = {'categories': categories}

    if request.user.is_authenticated:

        comment = Comment.objects.get(pk=pk)
        comment_form = CommentForm(request.POST or None, instance=comment)

        if comment_form.is_valid():
            print("in COMMENT FORM VALID")
            cd = comment_form.cleaned_data

            print("in FORM VALID",cd)
            #comment_form.save()
            context = {'comment_form': comment_form, 'comment': comment, 'categories': categories}
            return render(request, "comment_update.html",context)

        else:
            context = {'comment_form': comment_form, 'comment': comment, 'categories': categories}
            return render(request, "comment_update.html", context)


def home_articles(request):
    print("HOME")
    filter_segment = { }
    if request.user.is_authenticated:

        if request.method == "POST":
            category = request.POST.get('category',False)
            print("POST",category)
            if category:
                filter_segment['category'] = category

        articles = Article.objects.filter(**filter_segment).order_by('-date_posted')

        categories = Category.objects.all()

        context = {'articles': articles, 'categories': categories}
        return render(request, 'home_articles.html', context)

    context = {}
    return render(request, 'home.html', context)

def post_article(request):

    print("in post_ARTICLE")
    if request.user.is_authenticated:
        user = request.user.id
        form = ArticleForm()

        if request.method == "POST":
            print("in POST")
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                articles = Article.objects.all().order_by('-date_posted')
                categories = Category.objects.all()

                context = {'form': form, 'categories': categories, 'articles': articles, 'user':user}
                return render(request, 'home_articles.html', context)


    context = {'form': form}
    return render(request, 'post_article.html', context)

def custom_upload_function(request):
    pass