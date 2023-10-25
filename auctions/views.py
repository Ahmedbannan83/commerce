from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Max

class HiddenSelectMultipleWidget(forms.SelectMultiple):
    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['hidden'] = True
        return attrs

class ListingForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                     widget=forms.Select(attrs=
                                    {'class': 'form-control'}))    
    bids = forms.ModelMultipleChoiceField(
                    queryset=Bid.objects.all(),
                    widget=HiddenSelectMultipleWidget,
                    required=False
            )
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ['bids','user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'start_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
                         
        }

def index(request):        
    return render(request, "auctions/index.html",{
        'listings' : Listing.objects.all(),
        'message':'Active Listings',
        'closed_listings':Listing.objects.filter(status=False),
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
        phone_number = request.POST.get("phone_number")

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
            user.phone_number = phone_number                
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login/")
def create_listing(request):
    if request.method=='POST':
        form = ListingForm(request.POST)
        if form.is_valid():            
            listing = form.save(commit=False)  # Create a Listing instance without saving to the database yet
            listing.user = request.user.username
            listing.save()  # Save the Listing instance with the user association
            return redirect('index')  # Use redirect for a cleaner URL
        else:
            form=ListingForm(request.POST)
    return render(request,"auctions/create_listing.html",{
        "form":ListingForm()
    })

@login_required(login_url="/login/")
def listing(request, id_listing):
    listing = Listing.objects.get(pk=id_listing)

    # Find the maximum bid amount for the current listing
    max_bid = listing.bids.aggregate(Max('amount'))['amount__max']

    # Find the user of the highest bid, if it exists
    max_bid_user = None
    if max_bid is not None:
        max_bid_user = Bid.objects.filter(listing=listing, amount=max_bid).values('user').first()
        if max_bid_user:
            max_bid_user = max_bid_user['user']

    if max_bid is None:
        max_bid = listing.start_bid
        max_bid_user = listing.user
    bid_message = ""

    if request.method == 'POST':
        new_bid_amount = float(request.POST.get('bid'))
        
        if new_bid_amount >max_bid:
            new_bid = Bid.objects.create(user=request.user, amount=new_bid_amount)
            listing.bids.add(new_bid)            
            max_bid = new_bid_amount
            max_bid_user = request.user
        else:
            bid_message = "Your bid is not the highest bid and was not accepted."

    return render(request, "auctions/listing.html", {
        "listing": listing,
        'max_bid': max_bid,
        "max_bid_user": max_bid_user,
        "bid_message": bid_message,
        "comments":Comment.objects.filter(listing=Listing.objects.get(pk=id_listing))
    })

@login_required(login_url="/login/")
def watchlist(request):
    message = ""
    try:
        user_watchlist = Watchlist.objects.get(user=request.user)
        watchlist = user_watchlist.listings.all()
    except Watchlist.DoesNotExist:
        # If Watchlist matching query does not exist, set watchlist to an empty list
        user_watchlist = None  # Set user_watchlist to None
        watchlist = []

    if request.method == 'POST':
        listing_id = request.POST.get("id_listing")
        listing = Listing.objects.get(pk=listing_id)

        if user_watchlist and listing in user_watchlist.listings.all():
            message = "Watchlist already exists"

        # Get or create the user's watchlist
        if user_watchlist is None:
            user_watchlist, created = Watchlist.objects.get_or_create(user=request.user)

        # Add the selected listing to the watchlist
        user_watchlist.listings.add(listing)
        watchlist = user_watchlist.listings.all()

    return render(request, 'auctions/watchlist.html', {
        'watchlist': watchlist,
        'message': message,
    })

@login_required(login_url="/login/")
def delete_from_watchlist(request , id_listing):
    user = request.user
    listing_to_delete = Listing.objects.get(pk=id_listing)
    user_watchlist = Watchlist.objects.get(user=user)
    user_watchlist.listings.remove(listing_to_delete)
    return redirect('watchlist') 

def categories(request):    
    posts = {}
    for cat in Category.objects.all():
        posts[cat]=len(Listing.objects.filter(category=cat,status=True))               
    return render(request,'auctions/categories.html',{
        'categories':Category.objects.all(),
        'posts':posts
    })

def category(request ,cat): 
    return render(request,'auctions/index.html',{
        'listings':Listing.objects.filter(category=Category.objects.get(pk=cat)),
        'message':Category.objects.get(pk=cat)        
    })

def change_status(request,id_listing):
    listing = get_object_or_404(Listing,pk=id_listing)
    listing.status = not listing.status    
    listing.save()
    if request.method == 'POST':
        listing.winner_user=request.POST["winner_user"]
        listing.save()
    return redirect('listing',id_listing=listing.id)

def add_comment(request,listing_id):
    listing = get_object_or_404(Listing,pk=listing_id)    
    if request.method == 'POST':
        Comment.objects.create(comment=request.POST['comment'],user=request.user.username,listing=listing)
    return redirect('listing',id_listing=listing_id)


