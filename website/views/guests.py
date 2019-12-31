from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings

from website.models import Article, Category

from django.views.generic import ListView, DetailView


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article_list')
    form = AuthenticationForm()
    return render(request, 'login.html', {
        'form': form
    })


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('article_list')


class ArticleListView(ListView):
    model = Article
    template_name = 'guests/article_list.html'
    ordering = ['-published_at']
    paginate_by = settings.PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = 'All Posts'
        return context
        
class CategoryArticleListView(ListView):
    model = Article
    template_name = 'guests/article_list.html'
    paginate_by = settings.PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super(CategoryArticleListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.kwargs.get('category')
        return context

    def get_queryset(self):
        category = get_object_or_404(
            Category, name=self.kwargs.get('category'))
        return Article.objects.filter(category=category).order_by('-published_at')


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'guests/article_detail.html'
