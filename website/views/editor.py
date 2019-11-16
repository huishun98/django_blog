from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from website.models import Article, Category

from .db_wrappers import save_article, delete_article, delete_category


@login_required(login_url='/login/')
def main_editor_view(request):

    if request.method == 'POST':
        slug = request.POST.get('slug')
        delete_article(slug=slug)

    template_name = 'editor/main_editor.html'
    articles = Article.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('name')

    return render(request, template_name, {
        'articles': articles,
        'categories': categories,
        'category': 'All'
    })


@login_required(login_url='/login/')
def category_main_editor_view(request, category):

    if request.method == 'POST':
        slug = request.POST.get('slug')
        delete_article(slug=slug)

    template_name = 'editor/main_editor.html'
    articles = Article.objects.all().order_by('-created_at')
    categories = Category.objects.all().order_by('name')

    return render(request, template_name, {
        'articles': articles,
        'categories': categories,
        'category': category
    })


@login_required(login_url='/login/')
def category_editor_view(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        delete_category(name=name)

    template_name = 'editor/category_editor.html'
    categories = Category.objects.all().order_by('name')
    return render(request, template_name, {'categories': categories})


@login_required(login_url='/login/')
def article_editor_view(request, slug):
    template_name = 'editor/content_editor.html'

    if request.method == 'POST':
        form_data = request.POST

        if form_data.get('delete') is not None:
            delete_article(slug=slug)
            return redirect('main_editor')

        article_object = save_article(slug, form_data)

        if form_data.get("publish") is not None:
            return redirect('main_editor')

        if form_data.get("view") is not None:
            return redirect('article_detail', slug=article_object.slug)

        if form_data.get("save") is not None:
            return redirect('article_editor', slug=article_object.slug)

    # request method is GET

    if slug == 'new-post':
        return render(request, template_name, {
            'query': {}
        })

    return render(request, template_name, {
        'query': get_object_or_404(Article, slug=slug)
    })


@login_required(login_url='/login/')
def settings_view(request):
    template_name = 'editor/settings.html'
    return render(request, template_name)
