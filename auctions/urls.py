from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("auctions/create/", login_required(views.CreateListView.as_view(), login_url='auctions:index'),
         name="create_list"),
    path("auctions/watchlist/", views.WatchListView.as_view(), name="watch_list"),
    path("auctions/categories/", login_required(views.CategoriesView.as_view(), login_url='auctions:index'),
         name="categories"),
    path("auctions/listsbycategory/<str:category_id>",
         login_required(views.ListsByCategoryView.as_view(),  login_url='auctions:index'), name="lists_by_category"),
    path("auctions/<str:list_id>/", login_required(views.ListView.as_view(), login_url='auctions:index'),
         name="view_list"),
]
