from core.forms import *
from django.db.models import Q
from django.forms import ModelForm
from django.urls import reverse_lazy
from core.models import Article, Comment, College, Subscriber, 
from core.forms import SubscriberForm
from django.views.generic import ListView, DetailView, RedirectView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import send_mail
from rootFolder.settings import EMAIL_HOST_USER





