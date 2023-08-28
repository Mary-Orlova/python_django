from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    """
    Модель автора статьи:

    ::name - имя автора;
    ::bio - биография автора.
    """
    class Meta:
        ordering = ["name"]
        verbose_name = _('Author')
        verbose_name_plural = _('Autors')
    name = models.CharField(max_length=100, verbose_name='author')
    bio = models.TextField(null=True, blank=True, verbose_name='bio')

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель категории статьи:

    ::name - название статьи.
    """
    class Meta:
        ordering = ["name"]
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Модель категории тэга:

    ::name - название тэга.
    """
    class Meta:
        ordering = ["name"]
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Модель статьи:

    ::title - заголовок статьи.
    ::content - содержимое статьи.
    ::pub_date - дата публикации статьи.
    ::author - автор статьи.
    ::category - категория статьи.
    ::tags - теги статьи.
    """
    class Meta:
        ordering = ['pub_date']
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="tags")

    def __str__(self):
        return self.title
