from django.urls import path,include
from rest_framework.routers import DefaultRouter
#from imdb_app.api.views import movie_list,movie_detail
from imdb_app.api.views import WatchListAV,WatchDetailAV,RevieDetail
from imdb_app.api.views import (#SteamPlatFormAV,StreamPlatFormDetailAV,
                                ReviewList,ReviewCreate,StreamPlatFormVS)

router = DefaultRouter()
router.register('stream',StreamPlatFormVS,basename='streamplatform')

urlpatterns = [
    path('list/', WatchListAV.as_view(),name="movie-list"),
    path('<int:pk>/', WatchDetailAV.as_view(),name="movie-detail"),
    path('',include(router.urls)),
    #path('stream/',SteamPlatFormAV.as_view(),name="stream-platform"),
    
    #path('stream/<int:pk>/',StreamPlatFormDetailAV.as_view(),name="streamplatform-detail"),
    # path('review/',ReviewList.as_view(),name="review-list"),
    # path('review/<int:pk>/',RevieDetail.as_view(),name="review-detail")
    
    #path('stream/<int:pk>/review/',ReviewList.as_view(),name="review-list"),
    path('<int:pk>/reviews/',ReviewList.as_view(),name="review-list"),
    path('<int:pk>/review-create/',ReviewCreate.as_view(),name="review-create"),
    path('review/<int:pk>/',RevieDetail.as_view(),name="review-detail"),
    
    
]
