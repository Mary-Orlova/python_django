"""
В этом модуле лежат различные представления.

Разные view для интернет-магазина: по товарам, заказам и тд.
"""
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from blogapp.models import Article


class ArticleDetailsView(DetailView):
    template_name = "blogapp/article_details.html"
    queryset = (
        Article
        .objects
        .prefetch_related('author')
        .all()
    )
    context_object_name = "article"


class ArticleListView(ListView):
    template_name = 'blogapp/article_list.html'
    context_object_name = 'article'
    queryset = (
        Article
        .objects
        .select_related('category')
        .select_related('author')
        .defer('content')
        .all()
    )


class ArticleCreateView(CreateView):
    template_name = 'blogapp/article_create.html'
    model = Article
    fields = 'title', 'content', 'author', 'category', 'tags'
    success_url = reverse_lazy("blogapp:article_list")


class ArticleUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_superuser or (self.request.user == self.get_object().created_by)
    permission_required = 'blogapp.change_article'
    model = Article
    fields = 'title', 'content', 'author', 'category', 'tags'
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "blogapp:article_details",
            kwargs={"pk": self.object.pk},
        )


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy("blogapp:article_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)



