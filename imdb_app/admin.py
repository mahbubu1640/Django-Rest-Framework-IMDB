from django.contrib import admin

# Register your models here.

from imdb_app.models import WatchList,StreamPlatForm,Review

admin.site.register(WatchList)
admin.site.register(StreamPlatForm)
admin.site.register(Review)
