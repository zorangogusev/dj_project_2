from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("auctions/create/", login_required(views.CreateAdListingView.as_view(), login_url='auctions:index'),
         name="create_ad_listing"),
    path("auctions/watchlist/", login_required(views.WatchAdListingView.as_view(), login_url='auctions:index'),
         name="watch_ad_listing"),
    path("auctions/categories/", login_required(views.CategoriesView.as_view(), login_url='auctions:index'),
         name="categories"),
    path("auctions/closelist/", login_required(views.CloseAdListingView.as_view(), login_url='auctions:index'),
         name="close_ad_listing"),
    path("auctions/adlistingsbycategory/<str:category_id>",
         login_required(views.AdListingsByCategoryView.as_view(),  login_url='auctions:index'),
         name="ad_listings_by_category"),
    path("auctions/<str:ad_listing_id>/", login_required(views.AdListingView.as_view(), login_url='auctions:index'),
         name="view_ad_listing"),
    path("auctions/addcomment/<str:ad_listing_id>/", login_required(views.AddCommentView.as_view(), login_url='auctions:index'),
         name="add_comment"),
    path("auctions/offerbid/<str:ad_listing_id>/", login_required(views.OfferBidView.as_view(), login_url='auctions:index'),
         name="offer_bid"),
]
