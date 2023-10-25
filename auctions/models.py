from django.contrib.auth.models import AbstractUser
from django.db import models


class Bid(models.Model):
    amount = models.FloatField()
    user = models.CharField(max_length=100)
    
    
    def __str__(self):
        return f"{self.amount}"

class Category(models.Model):
    name = models.CharField(max_length=50)
    url_image = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name



class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)


 
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    start_bid = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    bids = models.ManyToManyField(Bid,blank=True, null=True)
    status = models.BooleanField()    
    created_date=models.DateField(auto_now=True)
    image_url = models.URLField(blank=True, null=True)
    user = models.CharField(max_length=100,blank=True,null=True)
    winner_user = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return f"{self.title}"
   
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing)  

    def __str__(self):
        return f"Watchlist of {self.user}"  
    
class Comment(models.Model):
    comment = models.TextField(max_length=500)    
    user = models.CharField(max_length=100,blank=True,null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,blank=True,null=True)