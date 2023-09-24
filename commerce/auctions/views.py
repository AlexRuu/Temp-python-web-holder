from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Bid, Comment, Category
from django.db.models import Max, FloatField


from .models import User


class CreateNewListing(forms.Form):
    title = forms.CharField(label="Title", max_length=20)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(min_value=0.01, decimal_places=2)
    image = forms.CharField(label="Image", required=False, max_length=200)
    category = forms.ModelChoiceField(
        queryset=Category.objects.values_list('category', flat=True),
        to_field_name="category",
        required=True,
        widget=forms.Select,
        initial="Clothing"
    )


class BidForm(forms.Form):
    amount = forms.DecimalField(label="Bid Amount", decimal_places=2)


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


def index(request):
    """
    Landing page
    """
    listings = Listing.objects.all()
    if "watchlist" not in request.session:
        request.session["watchlist"] = []
    return render(request, "auctions/index.html", {
        "listings": listings
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
        return render(request, "auctions/login.html")


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
        return render(request, "auctions/register.html")


@login_required
def create(request):
    """
    Create new listing page
    """
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        form = CreateNewListing(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            form_category = form.cleaned_data['category']
            category = Category.objects.get(category=form_category)
            if not form.data['image']:
                image = "https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg?20200913095930"
            else:
                image = form.cleaned_data['image']
            listing = Listing(
                title=title, description=description, category=category, image=image, price=price, user=user)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'auctions/create.html', {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form": CreateNewListing(),
    })


def listing(request, listing_id):
    """
    The listing detail page
    """
    listing = Listing.objects.get(pk=listing_id)
    watchlist = request.session['watchlist']
    status = listing.status
    listing_price = Listing.objects.get(pk=listing_id).price
    comments = Comment.objects.filter(item=listing_id)
    bids = listing.item_bid.all()
    highest_bid = bids.aggregate(Max("amount", output_field=FloatField()))[
        "amount__max"]
    owner = ""
    if bids:
        top_bidder = listing.item_bid.all().order_by("-amount")[0].user
    else:
        top_bidder = None
    if request.user == listing.user:
        owner = True
    else:
        owner = False
    if request.method == "POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            amount = bid_form.cleaned_data['amount']
            if len(bids) > 0:
                if amount > highest_bid:
                    bid = Bid(amount=amount, user=request.user,
                              listing=listing)
                    bid.save()
                    return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
            else:
                if amount > listing_price:
                    bid = Bid(amount=amount, user=request.user,
                              listing=listing)
                    bid.save()
                    return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
        else:
            return render(request, "auctions/listing.html", {
                "bid_form": bid_form
            })
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "highest_bid": highest_bid,
        "bid_form": BidForm(),
        "owner": owner,
        "top_bidder": top_bidder,
        "user": request.user,
        "status": status,
        "watchlist": watchlist,
        "comment_form": CommentForm(),
        "comments": comments
    })


def close_listing(request, listing_id):
    """
    Let's listing owner close auction of their listing
    """
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    owner = listing.user
    if request.method == "POST":
        if user == owner:
            listing.status = True
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
    return render(request, "auctions/listing.html", {
        "listing": listing
    })


@login_required
def watchlist(request):
    """
    Retrieve user's watchlist
    """
    items = []
    wishlist = request.session['watchlist']
    if wishlist:
        for listing in wishlist:
            item = Listing.objects.get(pk=listing)
            items.append(item)
    return render(request, "auctions/watchlist.html", {
        'watchlist': items
    })


@login_required
def add_watchlist(request, listing_id):
    """
    Add a listing to the user's watchlist
    """
    listing = Listing.objects.get(pk=listing_id)
    wishlist = request.session['watchlist']
    if request.POST:
        if listing.id not in wishlist:
            request.session['watchlist'] += [listing.id]
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
        else:
            location = wishlist.index(listing_id)
            wishlist = wishlist.pop(location)
            request.session.modified = True
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
    return render(request, "auctions/listing.html", {
        "listing": listing
    })


def categories(request):
    """
    Retrieve list of categories 
    """
    categories = Category.objects.all()
    return render(request, 'auctions/category.html', {
        "categories": categories
    })


def category(request, category_id):
    """
    Display all products from the selected category
    """
    listings = Listing.objects.filter(category=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'auctions/category_list.html', {
        "listings": listings,
        "category": category
    })


def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data['comment']
            user_comment = Comment(comment=comment, user=user, item=listing)
            user_comment.save()
            return HttpResponseRedirect(reverse('listing', args=(listing.id,)))
        else:
            return render(request, 'auctions/listing.html', {
                "comment_form": comment_form
            })
