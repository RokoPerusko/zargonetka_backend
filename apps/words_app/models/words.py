from django.db import models
from django.contrib.auth.models import User

class Words(models.Model):
    word = models.CharField(max_length=50, unique=True)
    word_meaning = models.TextField(blank=False, null=False)
    word_example = models.TextField(blank=False, null=False)
    approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_words', blank=True)  # New field
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.word

    def like_count(self):
        return self.likes.count()
