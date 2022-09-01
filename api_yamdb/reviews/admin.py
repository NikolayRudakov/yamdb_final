from django.contrib import admin

from .models import Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "score", "title", "pub_date")
    search_fields = ("score", "title")
    list_filter = ("pub_date",)
    empty_value_field = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "pub_date")
    search_fields = ("review",)
    list_filter = ("pub_date",)
    empty_value_field = "-пусто-"


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
