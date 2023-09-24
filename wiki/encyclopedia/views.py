from django.shortcuts import render

from . import util
from markdown2 import Markdown
from random import randrange
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect


markdowner = Markdown()


class CreateNewWikiForm(forms.Form):
    title = forms.CharField(label="Title", max_length=20)
    content = forms.CharField(widget=forms.Textarea, label="Description")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, page):
    convert = util.get_entry(page)
    if convert:
        converted = markdowner.convert(convert)
        return render(request, "encyclopedia/entry.html", {
            "page": converted,
            "title": page
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "page": "<h1>The page you are looking for does not exist...</h1>",
            "title": "Error"
        })


def random(request):
    entries = util.list_entries()
    index = randrange(0, len(entries))
    return HttpResponseRedirect(f"wiki/{entries[index]}")


def edit(request, page):
    entry = util.get_entry(page)
    form = CreateNewWikiForm(request.POST)
    form.content = entry
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    return render(request, "encyclopedia/edit.html", {
        "page": page,
        "form": CreateNewWikiForm(initial={"title": page, "content": entry})
    })


def create(request):
    if request.method == "POST":
        form = CreateNewWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": CreateNewWikiForm()
    })
