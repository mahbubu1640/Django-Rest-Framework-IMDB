
from django.db import models

from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User


class StreamPlatForm(models.Model):
    name = models.CharField(max_length=64)
    about = models.CharField(max_length=164)
    website = models.URLField(max_length=100)
    def __str__(self):
        return self.name

    
class WatchList(models.Model):
    title = models.CharField(max_length=64)
    storyline = models.CharField(max_length=256)
    platform = models.ForeignKey(StreamPlatForm,on_delete=models.CASCADE,related_name="watchlist")
    active = models.BooleanField(default=False)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    

class Review(models.Model):
    review_user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=124)
    watchlist = models.ForeignKey(WatchList,on_delete=models.CASCADE,related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + " - "+ self.watchlist.title + str(self.review_user)