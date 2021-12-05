from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.urls import reverse
from .models import Follower, User, Post, Like
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import math   
import json
import re
from . import forms
from django.core.paginator import Paginator
ITEMS_PER_PAGE = 10
# some refactoring, and some utility things to make my life more comfortable
from . import angie

# my alias to print()
console = angie.Console()

contentValidator = re.compile('^[a-zA-Z0-9.,!\"\'?:;\s@#$%^&*()[\]_+={}\-]{5,75}$')

def index(request):

    if request.method == "GET":

        # PAGINATION
        # I didn't use the built in stuff - I knew how to do pagination from some NodeJS projects so I translated my solutions from
        # that into python
        pageNumber = request.GET.get('page', 1) # get the page number the user requested

        # check it can be converted to an integer
        try:
            pageNumber = int(pageNumber)
        except ValueError:
            messages.add_message(request, messages.ERROR, "That page doesn't exist.")
            return redirect("index")


        recordsCount = Post.objects.all().count() # get the number of total records
        totalNumberOfPages = math.ceil(recordsCount / 10)

        if totalNumberOfPages < 1:
            totalNumberOfPages = 1

        if pageNumber > totalNumberOfPages:
            messages.add_message(request, messages.ERROR, "That page doesn't exist.")
            return redirect("index")

        if pageNumber < 1:
            # console.log("got in here")
            messages.add_message(request, messages.ERROR, "That page doesn't exist.")
            return redirect("index")

        # REMEMBER DJANGO TAKES THIS AS [OFFSET:OFFSET+LIMIT] - NOT LIKE THE QUERY YOU WROTE FOR TAXWEB
        posts = Post.objects.all().order_by("-posted_on")[(pageNumber - 1 ) * ITEMS_PER_PAGE: (pageNumber - 1 ) * ITEMS_PER_PAGE + ITEMS_PER_PAGE] # get the specific records from the db
        # console.log(pageNumber)
        # console.log((pageNumber - 1 ) * ITEMS_PER_PAGE)
        # console.log(ITEMS_PER_PAGE)
        # console.log(results)
        # console.log(recordsCount)


        # Process data so that the like buttons can be handled
        processedata = []
        for post in posts:
            if request.user.is_authenticated:
                # check if the user liked it
                userLiked = Like.objects.filter(user = request.user, post = post)
                if userLiked:
                    # if there is a like, put it in
                    processedata.append({"post":post, "liked": True})
                    # console.log(userLiked)
                else:
                    # if there isn't a like, dont
                    processedata.append({"post":post, "liked": False})
                    # console.log("not found")
            else:
                processedata.append({"post":post})

        return render(request, "network/index.html", {
            "posts": processedata,
            "totalItems": recordsCount,
            "currentPage": pageNumber,
            "hasNextPage": ITEMS_PER_PAGE * pageNumber < recordsCount,
            "hasPreviousPage": pageNumber > 1,
            "nextPage": pageNumber + 1,
            "previousPage": pageNumber - 1,
            "lastPage": math.ceil(recordsCount / ITEMS_PER_PAGE),
            })


@login_required(login_url='/login/')
def following(request):

    # get all the users being followed
    following = Follower.objects.filter(user = request.user)

    # Get all the users the current user is following
    followedUsers = []
    for item in following:
        followedUser = User.objects.get(id = item.following.id)
        followedUsers.append(followedUser)

    # PAGINATION
    # I didn't use the built in stuff - I knew how to do pagination from some NodeJS projects so I translated my solutions from
    # that into python
    pageNumber = request.GET.get('page', 1) # get the page number the user requested


    # check it can be converted to an integer
    try:
        pageNumber = int(pageNumber)
    except ValueError:
        messages.add_message(request, messages.ERROR, "That page doesn't exist.")
        return redirect("following")

    recordsCount = Post.objects.filter(posted_by__in = followedUsers).count() # get the number of total records
    # console.log(f"records count {recordsCount}")
    # REMEMBER DJANGO TAKES THIS AS [OFFSET:OFFSET+LIMIT] - NOT LIKE THE QUERY YOU WROTE FOR TAXWEB

    # figure out the total number of pages
    totalNumberOfPages = math.ceil(recordsCount / 10)
    if totalNumberOfPages < 1:
        totalNumberOfPages = 1

    if pageNumber > totalNumberOfPages:
        messages.add_message(request, messages.ERROR, "That page doesn't exist.")
        return redirect("following")

    if pageNumber < 1:
        # console.log("got in here")
        messages.add_message(request, messages.ERROR, "That page doesn't exist.")
        return redirect("following")

    # Now handle the users the same way as in the index
    results = Post.objects.filter(posted_by__in = followedUsers)[(pageNumber - 1 ) * ITEMS_PER_PAGE: (pageNumber - 1 ) * ITEMS_PER_PAGE + ITEMS_PER_PAGE] # get the specific records from the db


    # Process data so that the like buttons can be handled
    processedata = []
    for post in results:
        if request.user.is_authenticated:
            # check if the user liked it
            userLiked = Like.objects.filter(user = request.user, post = post)
            if userLiked:
                # if there is a like, put it in
                processedata.append({"post":post, "liked": True})
                # console.log(userLiked)
            else:
                # if there isn't a like, dont
                processedata.append({"post":post, "liked": False})
                # console.log("not found")
        else:
            processedata.append({"post":post})



    return render(request, "network/following.html", {
        "posts": processedata,
        "totalItems": recordsCount,
        "currentPage": pageNumber,
        "hasNextPage": ITEMS_PER_PAGE * pageNumber < recordsCount,
        "hasPreviousPage": pageNumber > 1,
        "nextPage": pageNumber + 1,
        "previousPage": pageNumber - 1,
        "lastPage": math.ceil(recordsCount / ITEMS_PER_PAGE)
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def newpost(request):

    # Show the page to add a new post
    if request.method == "GET": 
        form = forms.NewPostForm()
        return render(request , "network/newpost.html", {
            "form": form,
            "navnewpost": True
        })

    if request.method == "POST":
        # console.log("hit the right route")
        form = forms.NewPostForm(request.POST)
        # short circuit if bad form
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, 'Malformed request')
            return render(request, "network/newpost.html", {
                "form": form
            })

        content = form.cleaned_data["content"]
        postContent = Post(content=content, posted_by = request.user)
        postContent.save()

        messages.add_message(request, messages.SUCCESS, 'Successfully saved your post!')
        return redirect("index")


def profile(request, id):
    if request.method == "GET":


        userDetails = User.objects.get(pk=id)
        pageNumber = request.GET.get('page', 1) # get the page number the user requested
        # check it can be converted to an integer
        try:
            pageNumber = int(pageNumber)
        except ValueError:
            messages.add_message(request, messages.ERROR, "That page doesn't exist.")
            return redirect("profile", id)






        recordsCount = Post.objects.filter(posted_by = id).count() # get the number of total records
        # REMEMBER DJANGO TAKES THIS AS [OFFSET:OFFSET+LIMIT] - NOT LIKE THE QUERY YOU WROTE FOR TAXWEB
        userPosts = Post.objects.filter(posted_by = id).order_by("-id")[(pageNumber - 1 ) * ITEMS_PER_PAGE: (pageNumber - 1 ) * ITEMS_PER_PAGE + ITEMS_PER_PAGE] # get the specific records from the db


        
        # figure out the total number of pages
        totalNumberOfPages = math.ceil(recordsCount / 10)
        if totalNumberOfPages < 1:
            totalNumberOfPages = 1

        if pageNumber > totalNumberOfPages:
            messages.add_message(request, messages.ERROR, "That page doesn't exist.")
            return redirect("profile", id)

        if pageNumber < 1:
            # console.log("got in here")
            messages.add_message(request, messages.ERROR, "That page doesn't exist.")
            return redirect("profile", id)


        amIFollowing = False
        if request.user.is_authenticated:
            amIFollowing = Follower.objects.filter(user = request.user, following = id)

        return render(request, "network/profile.html", {
            "details": userDetails,
            "posts": userPosts,
            "amifollowing": amIFollowing,
            "totalItems": recordsCount,
            "currentPage": pageNumber,
            "hasNextPage": ITEMS_PER_PAGE * pageNumber < recordsCount,
            "hasPreviousPage": pageNumber > 1,
            "nextPage": pageNumber + 1,
            "previousPage": pageNumber - 1,
            "lastPage": math.ceil(recordsCount / ITEMS_PER_PAGE),
        })
 

@login_required
def follow(request, id):

    # make sure the user isn't following themselves
    targetUser = User.objects.get(id = id)
    if targetUser == request.user:
        messages.add_message(request, messages.ERROR, "You can't follow yourself.")
        return redirect("profile", id)


    if request.method == "POST":

        # check if there is a record of following this user
        amIFollowing = Follower.objects.filter(user = request.user, following = id)
        if amIFollowing:
            messages.add_message(request, messages.ERROR, "You are already following that user.")
            return redirect("profile", id)

        # If all is good let's follow the user
        follow = Follower(user = request.user, following = targetUser)
        follow.save()

        # update the follower count for the user being followed
        allUserFollowers = Follower.objects.filter(following = targetUser).count()
        targetUser.number_of_followers = allUserFollowers
        targetUser.save()


        # update the followed count for the user who is following
        allFollowing = Follower.objects.filter(user = request.user).count()
        requestor = User.objects.get(id = request.user.id)
        requestor.number_of_following = allFollowing
        requestor.save()

        messages.add_message(request, messages.SUCCESS, "You are now following that user.")
        return redirect("profile", id)
  

@login_required
def unfollow(request, id):


    # make sure the user isn't unfollowing themselves
    targetUser = User.objects.get(id = id)
    if targetUser == request.user:
        messages.add_message(request, messages.ERROR, "You can't unfollow yourself.")
        return redirect("profile", id)

    if request.method == "POST":

        # check if there is a record of following this user
        amIFollowing = Follower.objects.filter(user = request.user, following = id)
        if not amIFollowing:
            messages.add_message(request, messages.ERROR, "You aren't following that user.")
            return redirect("profile", id)


        # If all is good, we need to unfollow the user


        # If all is good let's unfollow the user
        amIFollowing = Follower.objects.filter(user = request.user, following = targetUser)
        amIFollowing.delete()


        # update the follower count for the user being followed
        allUserFollowers = Follower.objects.filter(following = targetUser).count()
        targetUser.number_of_followers = allUserFollowers
        targetUser.save()

        # update the followed count for the user who is following
        allFollowing = Follower.objects.filter(user = request.user).count()
        requestor = User.objects.get(id = request.user.id)
        requestor.number_of_following = allFollowing
        requestor.save()

        messages.add_message(request, messages.SUCCESS, "You are no longer following that user.")
        return redirect("profile", id)


@login_required
def editpost(request, id):
    
    if request.method == "POST":
        # fetch the item from the databas
        post = Post.objects.get(id = id)

        # Reject the user if the user does not own the post
        if not post.posted_by == request.user:
            return JsonResponse({"error": "That is not your post. You are not allowed to do that (Server response)"})
        
        # Get the content from the json object
        data = json.loads(request.body)
        content = data['content']

        # validate it and send back if it fails
        if not contentValidator.match(content):
            return JsonResponse({"error": "There is something wrong with that input. Please check it. (server response)"})
 
        # save the item to the database if we got here and send data back to the front end
        post.content = content
        post.save()
        return JsonResponse({"success" :"Successfully saved your changes!", "content": content})
 
@login_required
def like(request, id):

    if request.method == "POST":
        
        # Make sure that the user doesn't own the post and short circuit if they do
        post = Post.objects.get(id = id)
        if post.posted_by == request.user:
            return JsonResponse({"error": "You can't like your own post. (Server response)"})

        # Make sure the user doesn't already have a record of liking that post
        currently_liked = Like.objects.filter(user = request.user, post = post)

        # console.log(currently_liked)
        if currently_liked:
            return JsonResponse({"error": "There is already a record of you liking that post. (Server response)"})

        # we can continue with adding to the database
        data = json.loads(request.body) # Get the content from the json object
        purpose = data['addlike'] 
        
        if int(purpose) != 1:
            return JsonResponse({"error": "I don't recognize that input. (Server response)"})

        # add the like to the database
        addLike = Like(post = post, user = request.user )
        addLike.save()
       
        # read all the likes from the database and update the post
        allLikes = Like.objects.filter(post = post).count()
        post.number_of_likes = allLikes
        post.save()

        return  JsonResponse({"success": "Successfully liked that post! (Server response)"})

@login_required
def unlike(request, id):

    if request.method == "POST":
        
        # Make sure that the user doesn't own the post and short circuit if they do
        post = Post.objects.get(id = id)
        if post.posted_by == request.user:
            return JsonResponse({"error": "You can't unlike your own post. (Server response)"})

        # Make sure the user doesn't already have a record of liking that post
        currently_liked = Like.objects.filter(user = request.user, post = post)

        if not currently_liked:
            return JsonResponse({"error": "There is no record of you liking that post. (Server response)"})

        # we can continue with removing from the database
        data = json.loads(request.body) # Get the content from the json object
        purpose = data['removelike'] 
        
        if int(purpose) != 1:
            return JsonResponse({"error": "I don't recognize that input. (Server response)"})

        # remove the item from the database
        currently_liked.delete()

        # read all the likes from the database and update the post
        allLikes = Like.objects.filter(post = post).count()
        post.number_of_likes = allLikes
        post.save()

        return  JsonResponse({"success": "Successfully unliked that post! (Server response)"})

@login_required
def get_likes(request, id):
    if request.method == "GET":
        post = Post.objects.get(id = id)
        return JsonResponse({"likes": post.number_of_likes})
    








