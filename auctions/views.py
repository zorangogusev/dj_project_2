from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from auctions import forms as auctions_forms
from .models import List, Category


class IndexView(View):

    def get(self, request):
        lists = List.objects.all().filter(active=True).order_by('-created_at')

        for list in lists:
            list.watched = True if request.user in list.watchers.all() else False

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

    def get(self, request, list_id=None):
        lists = request.user.watched_listings.all()

        context = {
            'lists': lists
        }
        return render(request, 'auctions/watchlist.html', context)

    def post(self, request):
        lists_watched = List.objects.get(id=request.POST.get('list_id'))

        if request.user in lists_watched.watchers.all():
            lists_watched.watchers.remove(request.user)
            # print('request.user is: ', request.user)
        else:
            lists_watched.watchers.add(request.user)
        return redirect(reverse('auctions:index'))


class CategoriesView(View):

    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories
        }
        return render(request, 'auctions/categories_page.html', context)


class ListsByCategoryView(View):

    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Exception as e:
            assert e
            return redirect(reverse('auctions:index'))

        lists = List.objects.filter(category_id=category_id)
        context = {
            'category': category,
            'lists': lists
        }
        return render(request, 'auctions/lists_by_categories.html', context)
