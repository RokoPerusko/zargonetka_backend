from django.contrib import admin
from apps.words_app.models import Words

class WordsAdmin(admin.ModelAdmin):
    list_display = ('word', 'approved', 'created_by')
    list_filter = ('approved',)
    actions = ['approve_words']

    def approve_words(self, request, queryset):
        queryset.update(approved=True)
    approve_words.short_description = 'Odobri odabrane riječi'

admin.site.register(Words, WordsAdmin)
