from django.urls import path
from django.shortcuts import render, redirect
from .views import HomePageView, AboutPageView, DashboardPageView, StatsPageView, AnalysisPageView, SearchAnalysisPageView
from .views_api import DataWords, DataBubble, StatsScheduleAjax, DataSubmissions, DataSentencesSubmissions, DataSentencesComments, DataWordCloud, DataNetwork, DataNetworkSearch
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    path('dashboard/stats/', StatsPageView.as_view(), name='stats'),
    path('dashboard/analysis/<int:pk>/', AnalysisPageView.as_view(), name='analysis'),
    path('dashboard/search-analysis/', SearchAnalysisPageView.as_view(), name='search-analysis'),
    path('api/ajax/words/<int:pk>/', DataWords.as_view(), name = "data_words"),
    path('api/ajax/wordcloud/<int:pk>/', DataWordCloud.as_view(), name = "data_wordcloud"),
    path('api/ajax/bubble/<int:pk>/', DataBubble.as_view(), name = "data_bubble"),
    path('api/ajax/network/<int:pk>/', DataNetwork.as_view(), name = "data_network"),
    path('api/ajax/network-search/', DataNetworkSearch.as_view(), name = "data_network_search"),
    path('api/ajax/submissions/<int:pk>/', DataSubmissions.as_view(), name = "data_submissions"),
    path('api/ajax/sentences_submissions/<str:submission_id>/', DataSentencesSubmissions.as_view(), name = "data_sentences_submissions"),
    path('api/ajax/sentences_comments/<str:comment_id>/', DataSentencesComments.as_view(), name = "data_sentences_comments"),
    path('api/ajax/stats/<str:action>/', StatsScheduleAjax.as_view(), name = "stats_api"),
]
