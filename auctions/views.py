from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from auctions import forms as auctions_forms
from .models import List


class IndexView(View):

    def get(self, request):
        lists = List.objects.all().filter(active=True).order_by('-created_at')
        context = {
            'lists': lists
        }

        return render(request, "auctions/index.html", context)


class ListView(View):
    def get(self, request, list_id):
        try:
            list = List.objects.filter(active=True).get(pk=list_id)
        except Exception as e:
            assert e
            return redirect(reverse('auctions:index'))

        context = {
            'list': list
        }
        return render(request, 'auctions/view_list.html', context)


class CreateListView(View):
    def get(self, request):

        user = request.user
        form = auctions_forms.ListForm()
        context = {
            'form': form
        }
        return render(request, 'auctions/create_list.html', context)

    def post(self, request):
        form = auctions_forms.ListForm(request.POST, request.FILES)

        if form.is_valid():
            print('form is valid')
            form.save()
        return redirect(reverse('auctions:index'))


class WatchListView(View):

    def get(self, request):
        return render(request, 'auctions/watchlist.html')


class ListsByCategoriesView(View):

    def get(self, request):
        return render(request, 'auctions/lists_by_categories.html')
