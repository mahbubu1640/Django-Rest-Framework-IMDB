from rest_framework import serializers
from imdb_app.models import WatchList,StreamPlatForm,Review




class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review 
        exclude = ('watchlist',)
        #fields = "__all__"
    

class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"

# from rest_framework.serializers import SerializerMethodField
# from django.urls import reverse
# from rest_framework import serializers

class StreamPlatFormSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # url = serializers.SerializerMethodField()

    class Meta:
        model = StreamPlatForm 
        fields = "__all__"

    
# class StreamPlatFormSerializer(serializers.HyperlinkedModelSerializer):
#     watchlist = WatchListSerializer(many=True, read_only=True)
#     url = serializers.SerializerMethodField()

#     class Meta:
#         model = StreamPlatForm 
#         fields = "__all__"

#     def get_url(self, obj):
#         request = self.context.get('request')
#         if request:
#             view_name = 'streamplatform-detail'  # Replace with your actual detail view name
#             url = reverse(view_name, args=[str(obj.pk)])
#             return request.build_absolute_uri(url)
#         return None
