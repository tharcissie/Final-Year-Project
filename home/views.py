from core.forms import *
from django.db.models import Q
from django.forms import ModelForm
from django.urls import reverse_lazy
from core.models import Article, Comment, College, Subscriber, Announcement
from core.forms import SubscriberForm
from django.views.generic import ListView, DetailView, RedirectView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator
from django.core.mail import send_mail
from rootFolder.settings import EMAIL_HOST_USER




#################     function of rendering the homepage     ###################
def homepage(request):
    articles = Article.objects.all().order_by('-id')
    articles_likes  = Article.objects.all()
    announcements = Announcement.objects.all().order_by('-id')[:5]    
    subscriber_form = SubscriberForm(request.POST or None)
    if subscriber_form.is_valid():
        subscriber_form.save()
        
        subject = "Hello New Subscriber"
        message = 'Thank you for subscribing to our UR Blog !!!'
        send_mail(subject, message, EMAIL_HOST_USER,['byives21@gmail.com'])
        return redirect('homepage')

    else:
        subscriber_form = SubscriberForm()

    return render(request, 'home/homepage.html',{'articles':articles, 'form':subscriber_form,'articles_likes':articles_likes,'announcements':announcements})


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    articles = Article.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'articles':articles,
    }
    return render(request, 'home/homepage.html', context)



#################     function of article details and comment stuff     ###################
def article_details(request, pk, template_name='home/article_detail.html'):
    article = get_object_or_404(Article, pk=pk)
    comments = Comment.objects.filter(article=article , reply=None).order_by('id')

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
             return redirect('homepage')
    comment_form = CommentForm()
    context = { 'object':article, 'comments':comments, 'comment_form':comment_form }  
    return render(request, template_name, context)


#################     function of announcement details     ###################
def announcement_details(request, pk, template_name='home/announcement_details.html'):
    announcement = get_object_or_404(Announcement, pk=pk)
    context = {'announcement':announcement}  
    return render(request, template_name, context)


def announcement_detail(request, pk, template_name='accounts/articles_related/announcement_details.html'):
    announcement = get_object_or_404(Announcement, pk=pk)
    context = {'announcement':announcement}  
    return render(request, template_name, context)





    
class ArticleView(DetailView):
    model = Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['subject', 'message']



class ArticleLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print(pk)
        obj = get_object_or_404(Article, pk=pk)
        url_= obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_



class ArticleDislikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        print(pk)
        ob = get_object_or_404(Article, pk=pk)
        urll_= ob.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in ob.dislikes.all():
                ob.dislikes.remove(user)
            else:
                ob.dislikes.add(user)
        return urll_






    #################     function of rendering the homepage     ###################

# def home(request):
#     article = Article.objects.all().order_by('-id')
#     paginator = Paginator(article, 6) # < 3 is the number of items on each page
#     page = request.GET.get('page') # < Get the page number
#     article = paginator.get_page(page) # < New in 2.0!

  
#     subscriber_form = SubscriberForm(request.POST or None)
#     if subscriber_form.is_valid():
#         subscriber_form.save()
        
#         subject = "Hello New Subscriber"
#         message = 'Thank you for subscribing to our UR Blog !!!'
#         send_mail(subject, message, EMAIL_HOST_USER,['byives21@gmail.com']
        
#         )
#     else:
#         subscriber_form = SubscriberForm()
#     return render(request, 'home/home.html',{'article':article,'form':subscriber_form})