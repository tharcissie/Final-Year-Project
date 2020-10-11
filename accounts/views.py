from core.models import Article, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth.forms import PasswordChangeForm
from core.forms import CommentForm
from django.core.mail import send_mail
from rootFolder.settings import EMAIL_HOST_USER
from core.models import *
from .filters import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import  update_session_auth_hash



def testing(request):    

    labels = []
    data = []

    queryset = Subscriber.objects.all()
    for sub in queryset:
        labels.append(sub.article_category)
        data.append(sub.email)

    return render(request, 'base_account.html', {
        'labels': labels,
        'data': data,
    })
  
#####################     function for rendering signup form on page    ######################
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('my_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


#####################     function for count user articles  ############
@login_required
# def dashboard(request):
#     total_articles = Article.objects.filter(author=request.user).count()
#     articles_likes  = Article.objects.filter(author=request.user)
#     notifications = Article.objects.all().order_by('-id')[:4]
#     total_Articles = Article.objects.all().count()
#     subscribers = Subscriber.objects.all().count()
#     announcements = Announcement.objects.all().count()
#     total_users = User.objects.all().count()
#     chart = College.objects.all()



#     template_name = 'accounts/articles_related/my_dashboard.html'
#     context = {'total_articles':total_articles,'articles_likes':articles_likes,'announcements':announcements,'subscribers':subscribers,'notifications':notifications,'total_Articles':total_Articles,'total_users':total_users,'chart':chart}
#     return render(request, template_name,context)

def dashboard(request):
    total_articles = Article.objects.filter(author=request.user).count()
    articles_likes  = Article.objects.filter(author=request.user)
    chart = College.objects.all()

    articles = Article.objects.all()
    latest = Article.objects.all().order_by('-id')[:5]


    total_Articles = Article.objects.all().count()
    subscribers = Subscriber.objects.all().count()
    announcements = Announcement.objects.all().count()
    total_users = User.objects.all().count()




    template_name = 'account/dashboard.html'
    context = {
        'total_articles':total_articles,
        'articles_likes':articles_likes,
        'chart':chart,

        'articles':articles,
        'latest':latest,


        'announcements':announcements,
        'subscribers':subscribers,
        'total_Articles':total_Articles,
        'total_users':total_users

        }
    return render(request, template_name,context)

#####################     function for create article ############


def subscriber():
    subscribers_list = []

    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        subscribers_list.append(subscriber.email)

    return subscribers_list

@login_required
def article_create(request):
    form = ArticleForm(request.POST or None ,files=request.FILES)
    if form.is_valid():
        form.save()
        subject = "Hello Subscriber"
        message = 'A new article from your choice has been created, be the first to read it and share your feedback'
        send_mail(subject, message, EMAIL_HOST_USER,subscriber())
        return redirect('my_dashboard')

    
    template_name='accounts/articles_related/create_article.html'
    return render(request, template_name, {'form':form})


#################  function for view user articles  ############
@login_required
def my_articles(request):
    my_articles = Article.objects.filter(author=request.user)

    template_name = 'accounts/articles_related/my_articles.html'
    context = {'my_articles':my_articles}
    return render(request, template_name, context)

#####################     function for edit article ############
@login_required
def edit_article(request, pk):
    article1 = Article.objects.get(pk=pk)
    form1 = ArticleForm(request.POST or None, instance=article1)
    if form1.is_valid():
        form1.save()
        return redirect('my_articles')
    template_name='accounts/articles_related/create_article.html'
    return render(request, template_name, {'form':form1})




###################   function for article details ############
def article_detail(request, pk, template_name='accounts/articles_related/article_details.html'):
    article = get_object_or_404(Article, pk=pk)
    # article = Article.objects.get(pk=pk)
    comments = Comment.objects.filter(article=article , reply=None).order_by('-id')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
             content = request.POST.get('content')
             reply_id = request.POST.get('comment_id')
             comment_qs = None
             if reply_id:
                 comment_qs = Comment.objects.get(id=reply_id)
             comment = Comment.objects.create(article=article, user=request.user, content=content, reply=comment_qs)
             comment.save() 
             return redirect('my_articles')
    comment_form = CommentForm()
    context = { 'object':article, 'comments':comments, 'comment_form':comment_form}  
    return render(request, template_name, context)









@login_required
def all_announcements(request):
    all_announcements = Announcement.objects.all()
    return render(request, 'accounts/all_annoncements.html',{'all_announcements':all_announcements})


@login_required
def published_articles(request):
    all_articles = Article.objects.all()
    articles_filter = ArticleFilter(request.GET, queryset=all_articles)
    return render(request, 'accounts/all_published_articles.html',{'all_articles':articles_filter})



@login_required
def all_subscribers(request):
    subscribers = Subscriber.objects.all()
    subscribers_filter = SubscriberFilter(request.GET, queryset=subscribers)
    return render(request, 'accounts/all_subscribers.html',{'subscribers':subscribers_filter})


def all_users(request):
    all_users = User.objects.all()
    return render(request, 'accounts/all_users.html',{'all_users':all_users})




def users(request):
    users = User.objects.all()
    return render(request, 'account/users.html',{'users':users})


def subscribers(request):
    subscribers = Subscriber.objects.all()
    # subscribers_filter = SubscriberFilter(request.GET, queryset=subscribers)
    return render(request, 'account/subscribers.html',{'subscribers':subscribers})


def cstArticles(request):
    cst = Article.objects.filter(college__name='CST')
    latest = Article.objects.filter(college__name='CST').order_by('-id')[:5]
    return render(request,'account/cst.html',{'cst':cst,'latest':latest})


def cbeArticles(request):
    cbe = Article.objects.filter(college__name='CBE')
    latest = Article.objects.filter(college__name='CBE').order_by('-id')[:5]
    return render(request,'account/cbe.html',{'cbe':cbe,'latest':latest})


def ceArticles(request):
    ce = Article.objects.filter(college__name='CE')
    latest = Article.objects.filter(college__name='CE').order_by('-id')[:5]
    return render(request,'account/ce.html',{'ce':ce,'latest':latest})


def cmhsArticles(request):
    cmhs = Article.objects.filter(college__name='CMHS')
    latest = Article.objects.filter(college__name='CMHS').order_by('-id')[:5]
    return render(request,'account/cmhs.html',{'cmhs':cmhs,'latest':latest})


def cavmArticles(request):
    cavm = Article.objects.filter(college__name='CAVM')
    latest = Article.objects.filter(college__name='CAVM').order_by('-id')[:5]
    return render(request,'account/cavm.html',{'cavm':cavm,'latest':latest})


def cassArticles(request):
    cass = Article.objects.filter(college__name='CASS')
    latest = Article.objects.filter(college__name='CASS').order_by('-id')[:5]
    return render(request,'account/cass.html',{'cass':cass,'latest':latest})


def articleDetails(request, pk):
    article = get_object_or_404(Article, pk=pk)
    latest = Article.objects.all().order_by('-id')[:8]
    return render(request,'account/article_details.html',{'article':article,'latest':latest})


###################   function for delete article ############
@login_required
def delete_article(request, pk):
    article= get_object_or_404(Article, pk=pk)    
    if request.method=='POST':
        article.delete()
        return redirect('dashboard')
    template_name='account/confirm_delete_article.html'
    return render(request, template_name, {'object':article})


##################  function for creating new announcement  #########
@login_required
def new_announcement(request):
    form = AnnouncementCreateForm(request.POST)
    if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, 'account/new_announcement.html',{'form':form})


##################  function for retrieving all announcements  #########
def announcements(request):
    announcements = Announcement.objects.all()
    return render(request, 'account/announcements.html',{'announcements':announcements})


##################  function for changing user password  #########
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your Password has been updated successfully !")
            return redirect('dashboard')
        else:
            messages.success(request, "Your Password did not match")
            return redirect('change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'account/change_password.html', {'form': form})


#################   function for updating user profile inforamtion and profile picture   ##################
@login_required
def update_profile(request):

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if p_form.is_valid():
            p_form.save()
            return redirect('update_profile')
    p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'account/update_profile.html',{'p_form':p_form})
