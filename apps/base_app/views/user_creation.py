from rest_framework import generics, permissions
from apps.words_app.models import Words
from apps.phrases_app.models import Phrases  # Pretpostavljamo da postoji model "Phrases"
from apps.words_app.serializers import WordsSerializer
from apps.phrases_app.serializers import PhrasesSerializer  # Pretpostavljamo da postoji serializer "PhrasesSerializer"

class UserCreatedWordsView(generics.ListAPIView):
    serializer_class = WordsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtriraj samo riječi koje je kreirao korisnik i koje su odobrene
        return Words.objects.filter(created_by=self.request.user, approved=True)

class UserCreatedPhrasesView(generics.ListAPIView):
    serializer_class = PhrasesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtriraj samo fraze koje je kreirao korisnik i koje su odobrene
        return Phrases.objects.filter(created_by=self.request.user, approved=True)
