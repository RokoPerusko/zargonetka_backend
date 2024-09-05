from django.db import models
from django.contrib.auth.models import User

class Phrases(models.Model):
    phrase = models.CharField(max_length=255, unique=True)
    phrase_meaning = models.TextField(blank=False, null=False)
    phrase_example = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_phrases', blank=True)  # New field
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.phrase

    def like_count(self):
        return self.likes.count()

