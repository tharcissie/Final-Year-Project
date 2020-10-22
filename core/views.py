from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, RedirectView
from django.utils.decorators import method_decorator
from .models import Article, Comment, College,Announcement
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.forms import ModelForm
from django.utils import timezone
from .forms import *
from django.core.paginator import Paginator
from django.core.mail import send_mail
from rootFolder.settings import EMAIL_HOST_USER
from django.db.models import Q
from taggit.models import Tag

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response





#################     function of rendering the homepage     ###################
# def homepage(request):
#     articles_likes  = Article.objects.all()
#     subscriber_form = SubscriberForm(request.POST or None)
#     if subscriber_form.is_valid():
#         subscriber_form.save()
        
#         subject = "Hello New Subscriber"
#         message = 'Thank you for subscribing to our UR Blog !!!'
#         send_mail(subject, message, EMAIL_HOST_USER,['byives21@gmail.com'])
#         return redirect('homepage')

#     else:
#         subscriber_form = SubscriberForm()

#     return render(request, 'home/homepage.html',{'articles':articles, 'form':subscriber_form,'articles_likes':articles_likes,'announcements':announcements})

def homepage(request):
    articles = Article.objects.all().order_by('-id')
    cstArticles_count = Article.objects.filter(college__name='CST').count()
    cmhsArticles_count = Article.objects.filter(college__name='CMHS').count()
    cbeArticles_count = Article.objects.filter(college__name='CBE').count()
    ceArticles_count = Article.objects.filter(college__name='CE').count()
    casstArticles_count = Article.objects.filter(college__name='CASS').count()
    cavmArticles_count = Article.objects.filter(college__name='CAVM').count()

    announcements = Announcement.objects.all().order_by('-id')[:5]    

    context = {
        'articles':articles,
        'cstArticles_count':cstArticles_count,
        'cmhsArticles_count':cmhsArticles_count,
        'cbeArticles_count':cbeArticles_count,
        'ceArticles_count':ceArticles_count,
        'casstArticles_count':casstArticles_count,
        'cavmArticles_count':cavmArticles_count,

        'announcements':announcements

    }
    return render(request, 'core/homepage.html', context)





























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
def announcement_detail(request, pk, template_name='home/announcement_details.html'):
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



















#####################     dealing with search features       ######################
class SearchResult(ListView):
    model = Article
    template_name = 'core/search_results.html'


    def get_context_data(self, *args, **kwargs):
        context = super(SearchResult, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            lookups = Q(subject__icontains = query) | Q(message__icontains=query)
            return Article.objects.filter(lookups).distinct()
        return Article.objects.all()

    # def get_queryset(self):
    #     search = self.request.GET.get('query')
       
    #     object_list = Article.objects.filter(

    #         Q(subject__icontains=search) | Q(message__icontains=search)
    #     )
    #     return object_list


def cst(request):
    articles_cst = Article.objects.filter(college__name='CST').order_by('-id')
    return render(request,'core/college_articles.html',{'articles_cst':articles_cst})

def cbe(request):
    articles_cbe = Article.objects.filter(college__name='CBE').order_by('-id')
    return render(request,'core/college_articles.html',{'articles_cbe':articles_cbe})

def cmhs(request):
    articles_cmhs = Article.objects.filter(college__name='CMHS').order_by('-id')
    return render(request,'core/college_articles.html',{'articles_cmhs':articles_cmhs})

def ce(request):
    articles_ce = Article.objects.filter(college__name='CE').order_by('-id')
    return render(request,'core/college_articles.html',{'articles_ce':articles_ce})

def cass(request):
    articles_cass = Article.objects.filter(college__name='CASS').order_by('-id')
    return render(request,'core/college_articles.html',{'articles_cass':articles_cass})

def cavm(request):
    articles_cavm = Article.objects.filter(college__name='CAVM').order_by('-id')
    return render(request,'core/college_articles.html',{'articles_cavm':articles_cavm})


################################## section of like view  ##################################
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
        return  url_


##############################################  section of dislike view  ###############################
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


################ function for finding subscribers and  create bew article    ################
def subscriber():
    subscribers_list = []

    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        subscribers_list.append(subscriber.email)

    return subscribers_list




def new_article(request):
    subject = "Hello Subscriber"
    message = 'A new article from your choice has been created, be the first to read it and share your feedback'
    send_mail(subject, message, EMAIL_HOST_USER,subscriber())

    template_name = 'core/new.html'
    return render (request, template_name)

class ChartData(APIView):
    authenticatication_classes=[]
    permision_classes=[]

    def get(self, request, format=None):
        cst =  Article.objects.filter(college__name='CST').count()
        cbe =  Article.objects.filter(college__name='CBE').count()
        cmhs =  Article.objects.filter(college__name='CMHS').count()
        ce =  Article.objects.filter(college__name='CE').count()
        cass =  Article.objects.filter(college__name='CASS').count()
        cavm =  Article.objects.filter(college__name='CAVM').count()
        labels = ["CST","CBE","CMHS","CE","CASS","CAVM"]
        default_items = [cst, cbe, cmhs, ce, cass, cavm]
        data = {
            "labels":labels,
            "default":default_items

        }
        return Response(data)

class ChartData_(APIView):
    authenticatication_classes=[]
    permision_classes=[]

    def get(self, request, format=None):
        cst =  Subscriber.objects.filter(article_category__name='CST').count()
        cbe = Subscriber.objects.filter(article_category__name='CBE').count()
        cmhs =  Subscriber.objects.filter(article_category__name='CMHS').count()
        ce =  Subscriber.objects.filter(article_category__name='CE').count()
        cass =  Subscriber.objects.filter(article_category__name='CASS').count()
        cavm =  Subscriber.objects.filter(article_category__name='CAVM').count()
        labels = ["CST","CBE","CMHS","CE","CASS","CAVM"]
        default_items = [cst, cbe, cmhs, ce, cass, cavm]
        data = {
            "label":labels,
            "defaultdata":default_items

        }
        return Response(data)        

