from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("auctions/<str:list_id>/", login_required(views.ListView.as_view(), login_url='auctions:index'), name="view_list"),
    path("auctions/create/", login_required(views.CreateListView.as_view(), login_url='auctions:index'), name="create_list"),
    path("auctions/watchlist/", views.WatchListView.as_view(), name="watch_list"),
    path("auctions/listsbycategories/", views.ListsByCategoriesView.as_view(), name="lists_by_categories"),
]
