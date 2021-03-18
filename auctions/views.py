from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View

from auctions import forms as auctions_forms
from .models import List, Category, ListComment, Bid
from .util import check_bid


class IndexView(View):

    def get(self, request):
        lists = List.objects.all().order_by('-created_at')

        for list in lists:
            list.watched = True if request.user in list.watchers.all() else False

        context = {
            'lists': lists
        }

        return render(request, "auctions/index.html", context)


class ListView(View):
    def get(self, request, list_id):
        try:
            list = List.objects.get(pk=list_id)
        except Exception as e:
            assert e
            return redirect(reverse('auctions:index'))

        list.watched = True if request.user in list.watchers.all() else False
        comment_form = auctions_forms.ListCommentForm
        comments = ListComment.objects.filter(list_id=list_id).order_by('-created_at')
        offer_bid_form = auctions_forms.BidForm()
        message = request.GET.get('message') if request.GET.getlist('message') else None

        context = {
            'list': list,
            'comment_form': comment_form,
            'comments': comments,
            'offer_bid_form': offer_bid_form,
            'message': message
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
        # need refactor
        form = auctions_forms.ListForm(request.POST, request.FILES)

        if not form.is_valid():
            print(form.errors)
            form = auctions_forms.ListForm(request.POST)
            context = {
                'form': form,
                'message': 'error'
            }
            return render(request, 'auctions/create_list.html', context)

        new_list = form.save(commit=False)
        new_list.owner = request.user
        new_list.save()

        return redirect(reverse('auctions:index'))


class WatchListView(View):

    def get(self, request):
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


class OfferBidView(View):
    def post(self, request, list_id):
        print(request.POST)
        list = List.objects.get(id=list_id)

        if not check_bid(request.POST.get('price'), list):
            return redirect(reverse('auctions:view_list', args=[list_id]) + '?message=Please enter bigger offer than '
                                                                            'start price and actual price ')
        # need refactor
        form = auctions_forms.BidForm(request.POST)
        new_bid = form.save(commit=False)
        new_bid.list = list
        new_bid.user = request.user
        new_bid.save()
        list.current_bid = request.POST.get('price')
        list.save()

        return redirect(reverse('auctions:view_list', args=[list_id]))


class CloseListView(View):
    def post(self, request):
        try:
            list = List.objects.get(id=request.POST.get('list_id'))
        except Exception as e:
            assert e
            return redirect(reverse('auctions:index'))

        if request.user != list.owner:
            print('not owner')
            return redirect(reverse('auctions:index'))

        print('here')
        print(request.POST)

        list.active = False
        list.new_owner = Bid.objects.filter(list=list).last().user
        list.save()

        return redirect(reverse('auctions:view_list', args=[request.POST.get('list_id')]))
