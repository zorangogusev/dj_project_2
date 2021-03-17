from django.test import SimpleTestCase
from django.urls import reverse, resolve
from auctions import views


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('auctions:index')
        self.assertTrue(resolve(url).func.view_class, views.IndexView)

    def test_create_list_url_resolves(self):
        url = reverse('auctions:create_list')
        self.assertTrue(resolve(url).func.view_class, views.CreateListView)

    def test_watch_list_url_resolves(self):
        url = reverse('auctions:watch_list')
        self.assertTrue(resolve(url).func.view_class, views.WatchListView)

    def test_categories_url_resolves(self):
        url = reverse('auctions:categories')
        self.assertTrue(resolve(url).func.view_class, views.CategoriesView)

    def test_close_list_url_resolves(self):
        url = reverse('auctions:close_list')
        self.assertTrue(resolve(url).func.view_class, views.CloseListView)

    def test_lists_by_category_url_resolves(self):
        url = reverse('auctions:lists_by_category', args=['some-category'])
        self.assertTrue(resolve(url).func.view_class, views.ListsByCategoryView)

    def test_view_list_url_resolves(self):
        url = reverse('auctions:view_list', args=['example-list-id-1'])
        self.assertTrue(resolve(url).func.view_class, views.ListView)

    def test_add_comment_url_resolves(self):
        url = reverse('auctions:add_comment', args=['example-list-id-1'])
        self.assertTrue(resolve(url).func.view_class, views.AddCommentView)

    def test_offer_bid_url_resolves(self):
        url = reverse('auctions:offer_bid', args=['example-list-id-1'])
        self.assertTrue(resolve(url).func.view_class, views.OfferBidView)
