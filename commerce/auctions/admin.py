from django.contrib import admin
from .models import User, Bid, Comment, Listing, Category


class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "username")


class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "price")


class BidAdmin(admin.ModelAdmin):
    list_display = ("amount", "user", "listing")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'item',)


# Register your models here.
admin.site.register(User, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
