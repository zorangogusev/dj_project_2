from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from auctions import forms as auctions_forms
from .models import List, Category, ListComment


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

        list.watched = True if request.user in list.watchers.all() else False
        comment_form = auctions_forms.ListCommentForm
        comments = ListComment.objects.filter(list_id=list_id).order_by('-created_at')

        context = {
            'list': list,
            'comment_form': comment_form,
            'comments': comments
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
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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


class AddCommentView(View):
    def post(self, request, list_id):
        # need refactor...
        list = List.objects.get(id=list_id)
        form = auctions_forms.ListCommentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.list = list
            new_form.save()

        return redirect(reverse('auctions:view_list', args=[list_id]))
