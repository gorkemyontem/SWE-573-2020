from django.urls import path
from django.shortcuts import render, redirect
from .views import HomePageView, AboutPageView, DashboardPageView, StatsPageView, AnalysisPageView
from .views_api import DataWords, DataBubble, StatsScheduleAjax

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    path('dashboard/stats/', StatsPageView.as_view(), name='stats'),
    path('dashboard/analysis/<int:pk>/', AnalysisPageView.as_view(), name='analysis'),
    path('api/ajax/words/<int:pk>/', DataWords.as_view(), name = "data_words"),
    path('api/ajax/bubble/<int:pk>/', DataBubble.as_view(), name = "data_bubble"),
    path('api/ajax/stats/<str:action>/', StatsScheduleAjax.as_view(), name = "stats_api"),
]
