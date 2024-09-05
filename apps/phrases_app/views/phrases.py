# apps/phrases_app/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from apps.phrases_app.models import Phrases
from apps.phrases_app.serializers import PhrasesSerializer
import random
from django.db.models import Count

class PhrasesViewSet(viewsets.ModelViewSet):
    serializer_class = PhrasesSerializer

    def get_queryset(self):
        user = self.request.user
        sort_option = self.request.query_params.get('sort', 'date')
        queryset = Phrases.objects.all()

        if not user.is_staff:
            queryset = queryset.filter(approved=True)

        # Sortiranje prema sort opciji
        if sort_option == 'likes':
            queryset = queryset.annotate(like_count=Count('likes')).order_by('-like_count')
        elif sort_option == 'date':
            queryset = queryset.order_by('-created_at')
        elif sort_option == 'alphabetical':
            queryset = queryset.order_by('phrase')
        else:
            queryset = queryset.order_by('-created_at')  #

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def random(self, request):
        approved_phrases = self.get_queryset()
        if not approved_phrases.exists():
            return Response({'detail': 'No approved phrases found.'}, status=404)

        random_phrase = random.choice(approved_phrases)
        serializer = self.get_serializer(random_phrase)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trivia(self, request):
        approved_phrases = list(self.get_queryset())
        if not approved_phrases:
            return Response({'detail': 'No approved phrases found.'}, status=status.HTTP_404_NOT_FOUND)

        random_phrase = random.choice(approved_phrases)
        other_phrases = random.sample([phrase for phrase in approved_phrases if phrase != random_phrase], 3)

        answers = [
            {'text': random_phrase.phrase_meaning, 'is_correct': True},
            {'text': other_phrases[0].phrase_meaning, 'is_correct': False},
            {'text': other_phrases[1].phrase_meaning, 'is_correct': False},
            {'text': other_phrases[2].phrase_meaning, 'is_correct': False},
        ]

        return Response({
            'phrase': random_phrase.phrase,
            'answers': answers
        })

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        phrase = self.get_object()
        user = request.user

        if user.is_authenticated:
            if phrase.likes.filter(id=user.id).exists():
                phrase.likes.remove(user)
                return Response({'status': 'Unliked'}, status=status.HTTP_200_OK)
            else:
                phrase.likes.add(user)
                return Response({'status': 'Liked'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def top10(self, request):
        # Koristi annotate za brojanje lajkova
        top_phrases = Phrases.objects.filter(approved=True).annotate(like_count=Count('likes')).order_by('-like_count')[:10]
        serializer = self.get_serializer(top_phrases, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('search', '')
        phrases = Phrases.objects.filter(approved=True, phrase__icontains=query)
        serializer = self.get_serializer(phrases, many=True)
        return Response(serializer.data)
