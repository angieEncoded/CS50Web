from django.contrib import admin
from .models import User, Auction, Bid, Comment, Category, Watchlist
# Import this to allow us to adjust the user passwords in the admin module
from django.contrib.auth.admin import UserAdmin

# Make it a little nicer
class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid", "url", "high_bid", "category", "listed_by", "winner", "ended")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "bid_amount", "bidder", "item_id")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "item_id", "content", "user")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "user")



# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
