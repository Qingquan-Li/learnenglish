from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views import generic
from django.db.models import Q

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
    template_name = 'writing/article-list.html'
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
    return render(
        request,
        'writing/article-detail.html',
        {'article': article}
    )


# def search(request):
#     # The empty string handles an empty "request"
#     query = request.GET.get('q', '')
#     if query:
#         # https://docs.djangoproject.com/en/3.2/topics/db/queries/
#         # Entry.objects.get(headline__icontains='Lennon')
#         # SQL equivalent: SELECT ... WHERE headline ILIKE '%Lennon%';
#         queryset = (Q(title__icontains=query))
#         results = Article.objects.filter(queryset)
#     else:
#         results = []
#     context = {'results': results, 'query': query}
#     return render(request, 'writing/search.html', context)


# TODO: Use PostgreSQL’s full text search.
# https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/
