from rest_framework import serializers
from apps.words_app.models import Words

class WordsSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Words
        fields = ['id', 'word', 'word_meaning', 'word_example', 'approved', 'created_by', 'like_count', 'is_liked_by_user', 'created_at']  # Dodano polje 'created_at'

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        return user.is_authenticated and obj.likes.filter(id=user.id).exists()

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        validated_data['created_by'] = user
        validated_data['approved'] = False
        return super().create(validated_data)
