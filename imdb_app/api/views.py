
from rest_framework import status
#from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from imdb_app.models import WatchList,StreamPlatForm,Review
from imdb_app.api.serializers import (ReviewSerializer,WatchListSerializer,
                                      StreamPlatFormSerializer)
#from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly 

from imdb_app.api.permissions import IsAdminOrReadOnly
from imdb_app.api.permissions import  IsReviewOrReadOnly
from rest_framework.permissions import IsAuthenticated


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        movies= WatchList.objects.all()
        serializer=WatchListSerializer(movies,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        if request.method =='GET':
            try :
                movie=WatchList.objects.get(pk=pk)
                serializer = WatchListSerializer(movie)
                return Response(serializer.data) 
            
            except WatchList.DoesNotExist:
                return Response({'Error':'Movie does not found or Movie has been deleted from the site'},status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response({"Movie ":"deleted Successfully"},status=status.HTTP_204_NO_CONTENT)


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist,review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already review this movie!")    
        if watchlist.avg_rating == 0:
            watchlist.avg_rating =serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating+ serializer.validated_data['rating'])/2
        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
           
        serializer.save(watchlist=watchlist,review_user=review_user)
    def get_queryset(self):
        # You can return an empty queryset here as it's not needed for creation
        return Review.objects.none()

class ReviewList(generics.ListCreateAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    #permission_classes = [AdminOrReadOnly]
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    

class RevieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewOrReadOnly]
    



# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView)    :
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
    
# class RevieDetail(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset= Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class StreamPlatFormVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatForm.objects.all()
#         serializer = StreamPlatFormSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatForm.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatFormSerializer(watchlist, context={'request': request})
#         return Response(serializer.data)
    
#     def create(self,request):
#         serializer = StreamPlatFormSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        

class StreamPlatFormVS(viewsets.ModelViewSet):
    queryset = StreamPlatForm.objects.all()
    serializer_class = StreamPlatFormSerializer

# class StreamPlatFormVS(viewsets.ReadOnlyModelViewSet):
#     queryset = StreamPlatForm.objects.all()
#     serializer_class = StreamPlatFormSerializer
    
    
class SteamPlatFormAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        platform=StreamPlatForm.objects.all()
        serializer = StreamPlatFormSerializer(platform,many=True,context={'request': request})
        return Response(serializer.data)
    
    def post(self,request):
        serializer = StreamPlatFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
        
class StreamPlatFormDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        try:
            platform=StreamPlatForm.objects.get(pk=pk)
            
        except StreamPlatForm.DoesNotExist:
            return Response({'Error':'Not Found'},status=status.HTTP_404_NOT_FOUND)            
        
        serializer = StreamPlatFormSerializer(platform,context={'request': request})
        return Response(serializer.data)
            
    
    def put(self,request,pk):
        platform=StreamPlatForm.objects.get(pk=pk)
        serializer = StreamPlatFormSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        
    def delete(self,request,pk):
        platform=StreamPlatForm.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            
 