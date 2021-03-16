from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("create/", login_required(views.CreateListView.as_view(), login_url='auctions:index'), name="create_list"),
    path("watchlist/", views.WatchListView.as_view(), name="watch_list"),
    path("listsbycategories/", views.ListsByCategoriesView.as_view(), name="lists_by_categories"),
]
