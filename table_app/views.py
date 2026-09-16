from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from json import loads

from .forms import CategoryForm, QuoteForm
from .models import Category, Quote


@method_decorator(csrf_exempt, 'dispatch')
class CategoryView(View):
    def get(self, request, pk=None):
        if pk is None:
            data = list(Category.objects.values('id', 'name'))
            return JsonResponse(data, safe=False)

        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return HttpResponseNotFound('Category not found')

        return JsonResponse({
            'id': category.pk,
            'name': category.name,
            'quotes': list(category.quotes.values('id', 'text')),
        })

    def post(self, request):
        new_data = loads(request.body)
        form = CategoryForm(new_data)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors.as_json())
        category = form.save()
        return JsonResponse({'id': category.pk, 'name': category.name}, status=201)


@method_decorator(csrf_exempt, 'dispatch')
class QuoteView(View):
    def get(self, request, pk=None):
        if pk is None:
            qs = Quote.objects.all()

            category_id = request.GET.get('category')
            if category_id:
                qs = qs.filter(category_id=category_id)

            data = [
                {
                    'id': q.pk,
                    'text': q.text,
                    'category': q.category_id,
                }
                for q in qs
            ]
            return JsonResponse(data, safe=False)

        try:
            quote = Quote.objects.get(pk=pk)
        except Quote.DoesNotExist:
            return HttpResponseNotFound('Quote not found')

        return JsonResponse({
            'id': quote.pk,
            'text': quote.text,
            'category': quote.category_id,
        })

    def post(self, request):
        new_data = loads(request.body)
        form = QuoteForm(new_data)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors.as_json())
        quote = form.save()
        return JsonResponse({'id': quote.pk, 'text': quote.text}, status=201)


class RandomQuoteView(View):
    def get(self, request):
        qs = Quote.objects.all()

        category_id = request.GET.get('category')
        if category_id:
            qs = qs.filter(category_id=category_id)

        quote = qs.order_by('?').first()
        if quote is None:
            return HttpResponseNotFound('No quotes')

        return JsonResponse({
            'id': quote.pk,
            'text': quote.text,
            'category': quote.category_id,
        })