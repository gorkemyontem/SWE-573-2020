from django.urls import path
from django.shortcuts import render, redirect
from .views import HomePageView, AboutPageView, DashboardPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
]
