# apps/words_app/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from apps.words_app.models import Words
from apps.words_app.serializers import WordsSerializer
import random
from django.db.models import Count

class WordsViewSet(viewsets.ModelViewSet):
    serializer_class = WordsSerializer

    def get_queryset(self):
        user = self.request.user
        sort_option = self.request.query_params.get('sort', 'date')  # Dodajte sort opciju
        queryset = Words.objects.all()

        if user.is_staff:
            queryset = Words.objects.all()
        else:
            queryset = Words.objects.filter(approved=True)

        # Sortiranje prema sort opciji
        if sort_option == 'likes':
            queryset = queryset.annotate(like_count=Count('likes')).order_by('-like_count')
        elif sort_option == 'date':
            queryset = queryset.order_by('-created_at')  # Sortiraj po datumu kreiranja
        elif sort_option == 'alphabetical':
            queryset = queryset.order_by('word')  # Sortiranje abecedno
        else:
            queryset = queryset.order_by('-created_at')  # Defaultno sortiranje

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def random(self, request):
        approved_words = self.get_queryset()
        if not approved_words.exists():
            return Response({'detail': 'No approved words found.'}, status=404)

        random_word = random.choice(approved_words)
        serializer = self.get_serializer(random_word)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def trivia(self, request):
        approved_words = list(self.get_queryset())
        if not approved_words:
            return Response({'detail': 'No approved words found.'}, status=status.HTTP_404_NOT_FOUND)

        random_word = random.choice(approved_words)
        other_words = random.sample([word for word in approved_words if word != random_word], 3)

        answers = [
            {'text': random_word.word_meaning, 'is_correct': True},
            {'text': other_words[0].word_meaning, 'is_correct': False},
            {'text': other_words[1].word_meaning, 'is_correct': False},
            {'text': other_words[2].word_meaning, 'is_correct': False},
        ]

        return Response({
            'word': random_word.word,
            'answers': answers
        })

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        word = self.get_object()
        user = request.user

        if user.is_authenticated:
            if word.likes.filter(id=user.id).exists():
                word.likes.remove(user)
                return Response({'status': 'Unliked'}, status=status.HTTP_200_OK)
            else:
                word.likes.add(user)
                return Response({'status': 'Liked'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)


    @action(detail=False, methods=['get'])
    def top10(self, request):
        top_words = Words.objects.filter(approved=True).annotate(like_count=Count('likes')).order_by('-like_count')[:10]
        serializer = self.get_serializer(top_words, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('search', '')
        words = Words.objects.filter(approved=True, word__icontains=query)
        serializer = self.get_serializer(words, many=True)
        return Response(serializer.data)
