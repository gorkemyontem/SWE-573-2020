from django.urls import path
from django.shortcuts import render, redirect
from .views import HomePageView, AboutPageView, DashboardPageView, SchedulerPageView, StatsPageView, AnalysisPageView
from .views_api import postFriend

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    path('dashboard/stats/', StatsPageView.as_view(), name='stats'),
    path('dashboard/analysis/<int:pk>/', AnalysisPageView.as_view(), name='analysis'),
    path('post/ajax/friend', postFriend, name = "post_friend"),
    path('scheduler/', SchedulerPageView.as_view(), name='scheduler')
]
