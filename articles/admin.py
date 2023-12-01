from django.contrib import admin
from django.template.defaultfilters import truncatewords

from articles.models import Article, Category, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["author", "category", "title", "status"]
    raw_id_fields = ["author", "category"]
    list_select_related = ["author", "category"]
    list_per_page = 50
    search_fields = ["title", "author__first_name", "author__email", "category__name"]
    ordering = ["-created_at", "-name"]
    list_filter = ["status", "created_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["article", "user", "trunc_text"]
    raw_id_fields = ["article", "user"]
    list_filter = ["created_at"]
    search_fields = ["article__name"]

    def trunc_text(self, obj):
        return truncatewords(obj.text, 10)

    trunc_text.short_description = "truncated text"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    list_filter = ["created_at"]
