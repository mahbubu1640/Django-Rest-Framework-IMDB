import keyword
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from imdb_app.api import serializers
from imdb_app import models 

class StreamPlatFormTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example",password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token'+ self.token.key)
        
        self.stream = models.StreamPlatForm.objects.create(name="Netflix",about="Platform",website = "http://www.netflix.com")
        
        
    def tset_streamform_create(self):
        data = {
            "name" : "Netflix",
            "about": " Streaming Platform",
            "website" : "https://www.netflix.com"
        }
        response = self.client.post(reverse('streamplatform-list',data))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
    def test_streamplatform_list(self):
        response = self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_streamplatform_ind(self):
        response = self.client.get(reverse('streamplatform-detail',args = (self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        


class WatchListTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="example",password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token'+ self.token.key)
        
        self.stream = models.StreamPlatForm.objects.create(name="Netflix",about="Platform",website = "http://www.netflix.com")
        
        self.watchlist = models.Watchlist.objects.create(platform=self.stream,title="Example Movie",storyline = "Example Movie",active=True)
        
    
    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "Example Movie",
            "storyline": "Example Story",
            "active":True
        }
        
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
     
     
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie-detail',args=(self.watchlist.id)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.Watchlist.objects.get().title, 'Example Movie')
    


class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example",password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token'+ self.token.key)
        
        self.stream = models.StreamPlatForm.objects.create(name="Netflix",about="Platform",website = "http://www.netflix.com")
        
        self.watchlist = models.Watchlist.objects.create(platform=self.stream,title="Example Movie",storyline = "Example Movie",active=True)
        self.watchlist2 = models.Watchlist.objects.create(platform=self.stream,title="Example Movie",storyline = "Example Movie",active=True)
        
        self.review = models.Review.objects.create(review_user=self.user,rating=5,description="Great Movie", watchlist =self.watchlist2,active=True)
                
         
    def  test_review_create(self):
        data={
            "review_user":self.user,
            "rating":5,
            "description":"Greate Movie",
            "watchlist":self.watchlist,
            "active":True
        }
        response = self.client.post(reverse('review-create',args = (self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        self.assertEqual(models.Review.objects.get().rating,5)
        response = self.client.post(reverse('review-create',args = (self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    
    def test_review_create_unauth(self):
        data={
            "review_user":self.user,
            "rating":5,
            "description":"Greate Movie",
            "watchlist":self.watchlist,
            "active":True
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create',args = (self.watchlist.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_review_update(self):
        data={
            "review_user":self.user,
            "rating":4,
            "description":"Greate Movie",
            "watchlist":self.watchlist,
            "active":False
        }
        response = self.client.put(reverse('review-detail',args = (self.review.id,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_review_list(self):
        response = self.client.get(reverse('review-detail',args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username'+self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
            
        
        
        
        
        
        




class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "NewPassword@123",
            "password2": "NewPassword@123"
        }  
        response = self.client.post(reverse('register'), data)  # Fix the reverse call
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="NewPassword@123")
        
    def test_login(self):
        data = {
            "username": "example",
            "password": "NewPassword@123"  # Fix the password
        }
        response = self.client.post(reverse('login'), data)  # Fix the reverse call
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_logout(self):
        self.token = Token.objects.get(user_username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token'+ self.token+keyword)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code,status=status.HTTP_200_OK)
        
        