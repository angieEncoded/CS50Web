from django.shortcuts import render, redirect
from django import forms
from . import util
from django.utils.html import strip_tags
from random import randrange
from markdown2 import Markdown
markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):

    # Get the entry and if there is no entry send back a 404 page
    entry = util.get_entry(title)

    if entry == None:
        return render(request, "encyclopedia/404.html", {
            "title": title
        })
    
    # convert it to html
    htmlEntry = markdowner.convert(entry)

    # Send back the entry found
    return render(request, "encyclopedia/entry.html", {
        "entry": htmlEntry,
        "title": title
    })

def search(request):

    if request.method == "POST":
        # Get the user's search string
        query = strip_tags(request.POST.get('q'))
        
        # check if it matches an entry and if it does, redirect to the page with the search string
        if util.get_entry(query):
            page = util.get_entry(query)
            return redirect("title", query)

        # get the list of current entries
        currentEntries = util.list_entries()
        filteredList = []
        for item in currentEntries:
            if query in item:
                filteredList.append(item)
        
        # check and see if there is anything in the filtered list and send back to the home page if there isn't
        if len(filteredList) == 0:
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries(),
                    "empty": f"No entries match the search: {query} "
                })

        # Send that list through to a new page
        return render(request, "encyclopedia/partials.html", {
            "partials": filteredList 
        })
       
    # In case the user happens to just type in /search at the end, send them to the main home page
    return redirect("index")

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")

    if request.method == "POST":

        # get data from the form
        title = strip_tags(request.POST.get("title"))
        content = request.POST.get("content")

        # Sanitize Markdown data


        # Check if the title exists
        entry = util.get_entry(title)
        if entry != None:
            return render(request, "encyclopedia/new.html", {
                "error": "An entry with the name exists.",
                "title": title, 
                "content": content
            })

        # if it doesn't exist then we get to save the new entry and send the user there
        util.save_entry(title, content)
        return redirect("title", title)

def edit(request, title):

    # If we are getting the page, send the editing template
    if request.method == "GET":

        # get the entry data and render the template with the data
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title, 
            "content": content
        })


    # going to handle th post request in here - maybe we'll learn how Django handles RESTful patterns later? 
    if request.method == "POST":

        # get data from the form
        content = request.POST.get("content")

        # Sanitize Markdown data

        # Save the data
        util.save_entry(title, content)
        return redirect("title", title)


def random(request):
    # print("hit the route")

    # Get the entries
    entries = util.list_entries()

    # figure out how many there are
    # figure out the equivelent of Math.floor(Math.random() * whatever.length))
    randomNumber = randrange(len(entries))

    # render that random page
    return redirect("title", entries[randomNumber])
    # print(entries[randomNumber])












