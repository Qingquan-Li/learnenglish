from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views import generic
# from django.db.models import Q
from django.contrib.postgres.search import (SearchQuery, SearchVector,
                                            SearchRank, SearchHeadline)

from .models import Article, Tag


# Django pagination:
# https://docs.djangoproject.com/en/3.2/topics/pagination/
# https://docs.djangoproject.com/en/3.2/ref/paginator/
# Example:
# https://simpleisbetterthancomplex.com/tutorial/2016/08/03/how-to-paginate-with-django.html
# Bootstrap3 pagination:
# https://v3.bootcss.com/components/#pagination
class ArticleList(generic.ListView):
    model = Article
    template_name = 'speech/article-list.html'
    context_object_name = 'article_list'
    paginate_by = 10

    # queryset = Article.objects.all()

    # docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/#dynamic-filtering
    def get_queryset(self):
        query = self.request.GET.get('tag')
        if query:
            return Article.objects.filter(tags__name=query)
        return Article.objects.all()

    # docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/#adding-extra-context
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the tags
        context['tag_list'] = Tag.objects.all().order_by('name')
        return context


def article_detail(request, pk, slug=None):
    # article = Article.objects.get(pk=pk)
    article = get_object_or_404(Article, pk=pk)
    # stackoverflow.com/questions/31003934
    if slug != article.slug:
        # Either slug is wrong or None
        return redirect(article.get_absolute_url())
    return render(request, 'speech/article-detail.html', {'article': article})


# Use PostgreSQL’s full text search.
# https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/
def search(request):
    # The empty string handles an empty "request"
    query = request.GET.get('q', '')
    if query:
        search_query = SearchQuery(query)
        # search_vector = SearchVector('title', 'summary', 'body')
        search_vector = SearchVector('title', weight='A') + SearchVector(
            'summary', weight='B') + SearchVector('body', weight='B')
        search_rank = SearchRank(search_vector, search_query)
        search_headline = SearchHeadline('body', search_query)
        results = Article.objects.annotate(rank=search_rank).annotate(
            headline=search_headline).filter(rank__gte=0.001).order_by('-rank')
    else:
        results = []
    context = {'results': results, 'query': query}
    return render(request, 'speech/search.html', context)
