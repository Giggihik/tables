from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryView.as_view()),
    path('categories/<int:pk>/', views.CategoryView.as_view()),

    path('quotes/', views.QuoteView.as_view()),
    path('quotes/random/', views.RandomQuoteView.as_view()),
    path('quotes/<int:pk>/', views.QuoteView.as_view()),
]