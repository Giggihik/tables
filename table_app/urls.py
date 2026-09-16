from django.views.decorators.csrf import csrf_exempt
from . import views, path

urlpatterns = [
    path('categories/', csrf_exempt(views.CategoryView.as_view())),
    path('categories/<int:pk>/', csrf_exempt(views.CategoryView.as_view())),

    path('quotes/', csrf_exempt(views.QuoteView.as_view())),
    path('quotes/random/', views.RandomQuoteView.as_view()),
    path('quotes/<int:pk>/', csrf_exempt(views.QuoteView.as_view())),
]