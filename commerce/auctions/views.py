from .models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms.widgets import Select
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Category, Auction, Watchlist, Bid, Comment
# looks like this is the express equivelent to flash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# some refactoring, and some utility things to make my life more comfortable
from . import angie
from . import forms

# my alias to print()
console = angie.Console()


def index(request):
    # Get all the active listing from the database
    results = Auction.objects.filter(ended=0)
    return render(request, "auctions/index.html", {
        "results": results,
        "navlistings":True
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html", {"navlogin":True})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {"navregister": True})

def listing(request, id):

    # Get database record of the listing if it exists and deal with it if the user requests something that doesn't exist
    try: 
        listing = Auction.objects.get(id=id)
    except:
        messages.add_message(
            request, messages.ERROR, 'That item does not exist.')
        return redirect("index")
       

    # get the current high bid, if any
    high_bid = listing.high_bid
    # console.log(high_bid)
    if listing.high_bid != None:
        high_bid = Bid.objects.get(id=listing.high_bid.id)

    # get watchlist record for the user, if logged in
    watchlist = None
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(
            item=id).filter(user=request.user)
    else:
        watchlist = None

    # create a form for the comments
    commentForm = forms.commentForm()
    bidForm = forms.bidForm()
    # get any existing comments
    currentComments = Comment.objects.filter(item_id=listing)
    # console.log(currentComments)

    # Render the listing with necessary records
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "high_bid": high_bid,
        "watchlist": watchlist,
        "commentform": commentForm,
        "bidForm": bidForm,
        "comments": currentComments
    })
    # console.log("hit the route")


def categories(request):
    # Get all the categories from the database
    categories = Category.objects.all()

    # render the page
    return render(request, "auctions/categories.html", {
        "categories": categories,
        "navcategories": True
    })


def category_listings(request, id):
    
    # get the incoming id and then select the items that match that catergory
    category = Category.objects.filter(id = id)
    # console.log(category[0].name)

    # If for some reason the user selected a category that doesn't exist
    if not category:
        messages.add_message(
            request, messages.ERROR, 'That is not a valid catetory. Please select from the categories below:')
        return redirect('categories')

    results = Auction.objects.filter(category = category[0].name)
    # console.log(results)
    return render(request, "auctions/category_listings.html", {
        "results": results,
    })



@login_required(login_url='login')
def new(request):
    # Set up a Django form up top to take advantage of it dealing with all the stuff for us
    if request.method == "GET":
        form = forms.NewListingForm()
        return render(request, "auctions/new.html", {
            "form": form,
            "navnewlisting": True
        })

    # if the method is post, we need to do something else
    if request.method == "POST":
        # get the form
        form = forms.NewListingForm(request.POST)

        # short circuit if bad form
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Malformed request')
            return render(request, "auctions/new.html", {
                "form": form
            })

        # Get all the fields in the form

        # I want to make sure they are giving me a value that can be converted to a float
        try:
            starting_bid = float(form.cleaned_data["starting_bid"])
        except ValueError as error:
            messages.add_message(request, messages.ERROR, 'That starting bid is not a valid value. Please try again.')
            return render(request, "auctions/new.html", {
                "form": form
            })
        # all other fields can be whatever string the user wants
        category = form.cleaned_data["categories"]
        listed_by = request.user
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        url = form.cleaned_data["url"]

        # Add the details to the database
        auction = Auction(title=title, starting_bid=starting_bid,
                          category=category, listed_by=listed_by, url=url, description=description)
        auction.save()

        # Send the user back to the index page
        return HttpResponseRedirect(reverse("index"))



@login_required(login_url='login')
def watchlist(request, id):

    if request.method == "POST":
        # Get the id of the item from the form
        form = forms.simpleListForm(request.POST)
        # console.log(form)
        if form.is_valid():
            listing_id = form.cleaned_data["listing"]
            # console.log(listing_id)
            # See if there is a current object
            watchlist = Watchlist.objects.filter(
                item=listing_id).filter(user=request.user)
            auction = Auction.objects.get(id=listing_id)
            # console.log(watchlist)
            # console.log(auction)
            if watchlist.exists():
                watchlist.delete()
            else:
                watchlist = Watchlist(item=auction, user=request.user)
                watchlist.save()

            return redirect('listing', id)
        else:
            messages.add_message(
                request, messages.ERROR, 'Malformed request')
            return redirect("listing", id)
    # catch all redirect
    return redirect("listing", id)


@login_required(login_url='login')
def bid(request, id):
    
    if request.method == "POST":
        
        # Get the bid form and run through the validator
        form = forms.bidForm(request.POST)

        # Short circuit if something is wrong with the form
        if not form.is_valid():
            messages.add_message(
                request, messages.ERROR, 'Something is not right about the form')
            return redirect('listing', id)

        # get the record from the database
        auction = Auction.objects.get(id=id)
        
        # Make sure the auction is active - in case someone tries to be cute
        if auction.ended:
            messages.add_message(
                request, messages.ERROR, 'That auction has already ended')
            return redirect("listing", id)

        # Make sure that the user isn't bidding on their own item
        if auction.listed_by == request.user:
            console.log("Got here")
            messages.add_message(
                request, messages.ERROR, 'You listed this auction. You cannot bid on it')
            return redirect("listing", id)

        # get the bid amount from the form and convert it to a float
        bid_amount = float(form.cleaned_data["bid_amount"])
        # console.log("Didnt hit the user bidding on own item")
        # check if there is a high bid - interestingly Django is already doing a join
        # I didn't need to get the value from the database again manually
        if auction.high_bid:
            if bid_amount > auction.high_bid.bid_amount and bid_amount > auction.starting_bid:
                # Save it to the database (bid_amount, bidder, item_id)
                bid = Bid(bid_amount=bid_amount,
                            bidder=request.user, item_id=auction.id)
                bid.save()

                # Update the Auction record with the current high bid
                auction.high_bid = bid
                auction.save()
            else:
                messages.add_message(
                    request, messages.ERROR, 'Bid not higher than starting\current bid. Please check your bid.')
                return redirect('listing', id)

        # If there is no high bid we only check the starting bid logic
        if not auction.high_bid:
            if bid_amount >= auction.starting_bid:
                # Save it to the database (bid_amount, bidder, item_id)
                bid = Bid(bid_amount=bid_amount,
                            bidder=request.user, item_id=auction.id)
                bid.save()

                # Update the Auction record with the current high bid
                auction.high_bid = bid
                auction.save()
            else:
                messages.add_message(
                    request, messages.ERROR, 'Bid not higher than starting\current bid. Please check your bid.')
                return redirect('listing', id)

        # If we didn't hit any errors upstairs, we can return true to the user
        messages.add_message(
            request, messages.SUCCESS, 'Congratulations, you are the high bidder')
        return redirect('listing', id)
       

    # catch all redirect
    return redirect('listing', id)

@login_required(login_url='login')
def end_auction(request, id):

    if request.method == "POST":
        # get the details from the form to be sure we have the right item
        form = forms.simpleListForm(request.POST)

        # short circuit if bad form
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Malformed request')
            return redirect("listing", id)

        auction_id = form.cleaned_data["listing"]

        # get the auction listing
        auction = Auction.objects.get(id=auction_id)

        # check and make sure the user is the owner of the auction
        if request.user != auction.listed_by:
            messages.add_message(request, messages.ERROR,
                                 "You cannot end another user's auction")
            return redirect("listing", id)

        # end the auction if we made it here
        auction.ended = True
        if auction.high_bid:
            auction.winner = auction.high_bid.bidder
            auction.save()
            message = f"Success! {auction.winner} has won the auction"
        else:
            auction.save()
            message = "Auction ended with no bids."

        messages.add_message(request, messages.SUCCESS, message)
        return redirect("listing", id)

    # catch all redirect
    return redirect("listing", id)

@login_required(login_url='login')
def add_comment(request, id):
    if request.method == "POST":
        form = forms.commentForm(request.POST)

        # short circuit if bad form
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Malformed request')
            return redirect("listing", id)

        comment = form.cleaned_data["comment"]
        auction = Auction.objects.get(id=id)
        newComment = Comment(
            item_id=auction, content=comment, user=request.user)
        newComment.save()

        messages.add_message(request, messages.SUCCESS, 'Saved your comment!')
        return redirect("listing", id)

    pass

@login_required(login_url='login')
def mywatcheditems(request, id):

    # Check that the user is allowed to see this watchpage
    if id != request.user.id:
        messages.add_message(request, messages.ERROR, 'You are not allowed to view that page')
        return redirect("index")

    watchlist = Watchlist.objects.filter(user=request.user)
    # for item in watchlist:
        # console.log(item.item)

    return render(request, "auctions/mywatcheditems.html", {
        "watchlist": watchlist,
        "navwatchlist": True
    })

@login_required(login_url='login')
def won_auctions(request, id):
    # Check that the user is allowed to see this page
    if id != request.user.id:
        messages.add_message(request, messages.ERROR, 'You are not allowed to view that page')
        return redirect("index")

    won_auctions = Auction.objects.filter(winner=request.user)
    # for item in won_auctions:
    #     console.log(item)
    return render(request, "auctions/won_auctions.html", {
        "won_auctions": won_auctions,
        "navwonitems": True
    })

   
@login_required(login_url='login')
def my_listings(request, id):
    # Check that the user is allowed to see this page
    if id != request.user.id:
        messages.add_message(request, messages.ERROR, 'You are not allowed to view that page')
        return redirect("index")

    listings = Auction.objects.filter(listed_by=request.user)
    return render(request, "auctions/my_listings.html", {
        "listings": listings,
        "navmylistings": True
    })
  