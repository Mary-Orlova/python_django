"""
Различные классы Администратора
"""


from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from blogapp.models import Article, Author, Category, Tag
from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin


class OrderInline(admin.TabularInline):
    model = Product.orders.through


class ProductInline(admin.StackedInline):
    model = ProductImage


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
class ArticleAdmin(admin.ModelAdmin, ExportAsCSVMixin):
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


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
        ProductInline,
    ]

    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name"
    ordering = "-name", "pk"
    search_fields = "name", "description"
    fieldsets = [
        (None, {
           "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse"),
        }),
        ('Images', {
            'fields': ('preview',),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": "Extra options. Field 'archived' is for soft delete",
        })
    ]


    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
