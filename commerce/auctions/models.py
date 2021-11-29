from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related

# AbstractUser apparantly has some default settings already
# At least three models - auction listing, bids, comments on auction listing
# Auctions - would have an id, an item name, a current bid, a minimum bid, created_by
# id is automatically created by Django


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

# I discovered that there is no function prototyping, forward declarations, etc in Python
# but it seems that Django has a way around it by using a string instead of the class name
# https://stackoverflow.com/questions/524714/does-python-have-class-prototypes-or-forward-declarations

# Ran into a contraint issue as well - this stack overflow thread helped track down where it was, I needed to set null on a delete
# instead of do nothing - https://stackoverflow.com/questions/47620487/django-2-0-sqlite-integrityerror-foreign-key-constraint-failed

# And I ran into an issue with django admin not allowing me to set things to NULL in the database. I even had some trouble in HeidiSQL managing it. This thread helped 
# to track down THAT problem - https://stackoverflow.com/questions/32057210/django-modelform-wont-allow-null-value-for-required-field
# I guess this needs blank=True, null=True is not quite good enough and django admin likes strings.

class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.FloatField(null=True)
    url = models.CharField(blank=True, null=True, max_length=254)
    high_bid = models.ForeignKey(
        "Bid", on_delete=models.SET_NULL, related_name="current_high_bid", null=True, blank=True)
    category = models.CharField(max_length=100)
    listed_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_auctions")
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="auction_winner", null=True, blank=True)
    ended = models.BooleanField(default=False)


    def __str__(this):
        return f"id: {this.id} title: {this.title} description: {this.description} starting_bid:{this.starting_bid} url:{this.url} high_bid: {this.high_bid} category{this.category} listed_by: {this.listed_by} winner: {this.winner} ended:{this.ended}"


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid_amount = models.FloatField()
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bidder_name")
    # related name lets us access things in the opposite
    item_id = models.IntegerField()

    def __str__(this):
        return f"High Bid: {this.bid_amount} bidder: {this.bidder} item_id: {this.item_id}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    item_id = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="item_comments")
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(this):
        return f"id: {this.id} |  item_id: {this.item_id}  | content: {this.content} | user: {this.user}"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(this):
        return f"{this.name}"


class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="item_watching")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_watching")
