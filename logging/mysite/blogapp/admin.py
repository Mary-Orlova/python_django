from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from blogapp.models import Article, Author, Category, Tag


class AuthorInline(admin.TabularInline):
    model = Author


class ArticleInline(admin.TabularInline):
    model = Article


@admin.action(description="Archive article")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive article")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    model = Author


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # actions = [
    #     mark_archived,
    #     mark_unarchived,
    # ]
    # inlines = [
    #    ArticleInline,
    # ]
    # list_display = 'title', 'content', 'author', 'pub_date', 'category'
    # ordering = "-author", 'pub_date'
    # search_fields = "author", "tag", 'category'
    # fieldsets = [
    #     (None, {
    #        "fields": ("name", "description"),
    #     }),
    # ]

    def get_queryset(self, request):
        return Article.objects.select_related("author")

    def user_verbose(self, obj: Article) -> str:
        return obj.author

