from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request):
        return render(request, "auctions/index.html")


class CreateListView(View):

    def get(self, request):
        return render(request, 'auctions/create_list.html')


class WatchListView(View):

    def get(self, request):
        return render(request, 'auctions/watchlist.html')


class ListsByCategoriesView(View):

    def get(self, request):
        return render(request, 'auctions/lists_by_categories.html')
