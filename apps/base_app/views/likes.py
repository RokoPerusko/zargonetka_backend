from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth.models import User
from apps.words_app.models import Words
from apps.phrases_app.models import Phrases  # Pretpostavljamo da postoji model "Phrases"
from apps.words_app.serializers import WordsSerializer
from apps.phrases_app.serializers import PhrasesSerializer# Pretpostavljamo da postoji serializer "PhrasesSerializer"

class WordLikesViewSet(viewsets.ViewSet):
    def list(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        liked_words = user.liked_words.values_list('id', flat=True)
        return Response({'likes': list(liked_words)})

class PhraseLikesViewSet(viewsets.ViewSet):

    def list(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        liked_phrases = user.liked_phrases.values_list('id', flat=True)  # Pretpostavljamo da postoji relacija "liked_phrases"
        return Response({'phrase_likes': list(liked_phrases)})
