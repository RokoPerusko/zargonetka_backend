from django.contrib import admin
from apps.phrases_app.models import Phrases


class PhrasesAdmin(admin.ModelAdmin):
    list_display = ('phrase', 'approved', 'created_by')
    list_filter = ('approved',)
    actions = ['approve_phrases']

    def approve_phrases(self, request, queryset):
        queryset.update(approved=True)

    approve_phrases.short_description = 'Odobri odabrane fraze'


admin.site.register(Phrases, PhrasesAdmin)
