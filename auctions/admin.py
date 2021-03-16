from django.contrib import admin
from .models import Category, List, ListComment, Bid

# Register your models here.
admin.site.register(Category)
admin.site.register(List)
admin.site.register(ListComment)
admin.site.register(Bid)
