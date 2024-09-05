from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ZargonetkaProjekt.urls import schema_view
from .views import RegisterView, WordLikesViewSet, PhraseLikesViewSet, UserCreatedWordsView, UserCreatedPhrasesView
router = DefaultRouter()
router.register(r'user/word-likes', WordLikesViewSet, basename='word-likes')
router.register(r'user/phrase-likes', PhraseLikesViewSet, basename='phrase-likes')



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Registration endpoint
    path('', include(router.urls)),  # Include router-generated URLs
    path('user/created-words/', UserCreatedWordsView.as_view(), name='user-created-words'),
    path('user/created-phrases/', UserCreatedPhrasesView.as_view(), name='user-created-phrases'),
]
