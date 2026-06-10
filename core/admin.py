from django.contrib import admin

from .models import Category, Video, Suggestion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel_name', 'category', 'recommended', 'embed_disabled', 'date_added')
    list_filter = ('category', 'recommended',)
    search_fields = ('title', 'channel_name')
    readonly_fields = ('date_added', 'thumbnail_preview',)

    def thumbnail_preview(self, obj):
        if obj.youtube_id:
            url = f"https://img.youtube.com/vi/{obj.youtube_id}/hqdefault.jpg"
            return f'<img src="{url}" style="width:320px; border-radius:8px;">'
        return "No thumbnail yet"
    thumbnail_preview.allow_tags = True
    thumbnail_preview.short_description = "Thumbnail Preview"

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'status', 'submitted_at')
    list_filter = ('status',)
    readonly_fields = ('submitted_at',)  

